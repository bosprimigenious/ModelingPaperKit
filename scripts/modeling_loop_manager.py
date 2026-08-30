#!/usr/bin/env python3
"""Math-modeling loop manager: fonts → ai_use → writing → prose → model → lock → paper.

One slice per wake. Do not guess the next cut — always call `next`.

Exit codes (aligned with Paper loop):
  0  ok / next slice emitted
  2  STOP present
  3  lock held
  4  queue empty
  5  verify failed
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("MATH_MODELING_ROOT", Path(__file__).resolve().parents[1]))
ITER = ROOT / "iterator"
QUEUE = ITER / "queue.json"
STATE = ITER / "state.json"
LOCK = ITER / "lock.json"
STOP = ITER / "STOP"
CATALOG = ITER / "catalog.json"
LOOP_STATE = ITER / "loop_state.json"
RUNS = ROOT / "runs" / "loop"
LOCK_SECONDS = 12 * 60

PY = ROOT / ".venv" / "bin" / "python"
if not PY.exists():
    PY = Path(sys.executable)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_cmd(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def lock_held() -> dict | None:
    lock = load_json(LOCK, None)
    if not isinstance(lock, dict) or not lock.get("started_at"):
        return None
    try:
        started = datetime.strptime(lock["started_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None
    age = (datetime.now(timezone.utc) - started).total_seconds()
    if age < LOCK_SECONDS:
        return {"skip": "lock", "age_s": int(age), "slice_id": lock.get("slice_id")}
    return None


def pending_items(queue: dict, state: dict):
    completed = set(state.get("completed") or [])
    for index, item in enumerate(queue.get("items") or []):
        if item.get("id") in completed:
            continue
        yield index, item


def enrich(item: dict, index: int, catalog: dict) -> dict:
    ws = str(item.get("workspace") or "")
    meta = (catalog.get("workspaces") or {}).get(ws) or {}
    track = str(item.get("track") or "")
    track_meta = (catalog.get("tracks") or {}).get(track) or {}
    return {
        "index": index,
        "id": item.get("id"),
        "workspace": ws,
        "dir": meta.get("dir"),
        "contest": meta.get("contest"),
        "track": track,
        "goal": item.get("goal"),
        "done_when": item.get("done_when"),
        "manual": bool(item.get("manual")),
        "auto_verify": bool(track_meta.get("auto_verify")) and not bool(item.get("manual")),
        "what": track_meta.get("what"),
        "not": track_meta.get("not"),
        "paper_subdir": meta.get("paper_subdir"),
    }


def slice_dir(slice_id: str) -> Path:
    d = RUNS / slice_id
    d.mkdir(parents=True, exist_ok=True)
    return d


# ------------------------- verify implementations -------------------------


def verify_fonts(item: dict, out: Path) -> dict:
    paper = ROOT / "51" / "mcm_paper_package" / "01_paper" / "main.tex"
    text = paper.read_text(encoding="utf-8") if paper.exists() else ""
    checks = {
        "has_songti_fallback": "Songti SC" in text,
        "has_simsun_preferred": "SimSun" in text,
        "has_times": "Times New Roman" in text,
        "zihao_body_minus4": "zihao=-4" in text or r"\zihao{-4}" in text,
        "stretch_1": r"\setstretch{1.0}" in text,
        "no_header_plain": r"\pagestyle{plain}" in text,
        "section_heiti_zihao4": r"\zihao{4}" in text and r"\heiti" in text,
        "title_zihao3": r"\zihao{3}" in text,
    }
    # probe fonts via tectonic one-file
    probe = out / "font_probe.tex"
    probe.write_text(
        r"""\documentclass{article}
\usepackage{fontspec}
\begin{document}
SimSun=\IfFontExistsTF{SimSun}{YES}{NO}
SongtiSC=\IfFontExistsTF{Songti SC}{YES}{NO}
SimHei=\IfFontExistsTF{SimHei}{YES}{NO}
HeitiSC=\IfFontExistsTF{Heiti SC}{YES}{NO}
TNR=\IfFontExistsTF{Times New Roman}{YES}{NO}
\end{document}
""",
        encoding="utf-8",
    )
    font_probe = {"ran": False}
    if shutil.which("tectonic"):
        r = run_cmd(["tectonic", str(probe.name)], cwd=out)
        font_probe = {
            "ran": True,
            "exit": r.returncode,
            "stderr_tail": (r.stderr or r.stdout)[-1200:],
            "used_songti_in_log": "Songti" in (r.stderr + r.stdout),
            "used_heiti_in_log": "Heiti" in (r.stderr + r.stdout) or "STHeiti" in (r.stderr + r.stdout),
        }
    status = "ok" if all(checks.values()) else "accept_with_fallback"
    if not checks["has_times"] or not checks["stretch_1"]:
        status = "fail"
    report = {
        "track": "fonts",
        "status": status,
        "checks": checks,
        "font_probe": font_probe,
        "note": "mac 无 SimSun 时 Songti SC/Heiti SC 回退可接受；交 Windows 评阅机建议装 SimSun/SimHei 或重编",
    }
    write_json(out / "fonts_report.json", report)
    return report


def verify_ai_use(item: dict, out: Path) -> dict:
    typ = ROOT / "docs" / "ai-use" / "AI工具使用详情.typ"
    pdf = ROOT / "docs" / "ai-use" / "AI工具使用详情.pdf"
    pdf_space = ROOT / "docs" / "ai-use" / "AI 工具使用详情.pdf"
    compile_log = ""
    if typ.exists() and shutil.which("typst"):
        r = run_cmd(
            ["typst", "compile", str(typ.name), str(pdf.name)],
            cwd=typ.parent,
        )
        compile_log = (r.stderr or r.stdout)[-1500:]
        if r.returncode == 0 and pdf.exists():
            shutil.copyfile(pdf, pdf_space)
    pages = None
    if pdf.exists():
        r = run_cmd(["mdls", "-name", "kMDItemNumberOfPages", "-raw", str(pdf)])
        try:
            pages = int((r.stdout or "").strip())
        except ValueError:
            pages = None
    placeholders = 0
    if typ.exists():
        placeholders = len(re.findall(r"【[^】]*】", typ.read_text(encoding="utf-8")))
    status = "ok"
    if not pdf.exists():
        status = "fail"
    elif pages is not None and pages < 20:
        status = "partial"
    report = {
        "track": "ai_use",
        "status": status,
        "pages": pages,
        "pdf_bytes": pdf.stat().st_size if pdf.exists() else 0,
        "has_spaced_filename": pdf_space.exists(),
        "placeholder_count": placeholders,
        "compile_log_tail": compile_log,
        "note": "空模板≥20页为结构目标；实填后冲 20–30；placeholder_count 高说明尚未真实填写",
    }
    write_json(out / "ai_use_report.json", report)
    return report


def verify_writing(item: dict, out: Path) -> dict:
    ws = ROOT / "writing-skills"
    broken = []
    ok = []
    weak = []
    if not ws.exists():
        report = {"track": "writing", "status": "fail", "reason": "writing-skills missing"}
        write_json(out / "writing_report.json", report)
        return report
    for link in sorted(ws.glob("[HZA]-*")):
        if not link.exists():
            broken.append(link.name)
            continue
        skills = list(Path(link).resolve().rglob("SKILL.md"))
        alts = list(Path(link).resolve().glob("system.md"))
        if skills or alts:
            ok.append(link.name)
        else:
            weak.append(link.name)
    grok = Path.home() / ".grok" / "skills"
    grok_want = [
        "blader-humanizer",
        "stop-slop",
        "humanizer-zh",
        "shuorenhua",
        "academic-humanizer",
        "humanize-paper",
    ]
    grok_ok = [n for n in grok_want if (grok / n / "SKILL.md").is_file()]
    grok_miss = [n for n in grok_want if n not in grok_ok]
    status = "ok" if not broken and not weak else ("partial" if not broken else "fail")
    report = {
        "track": "writing",
        "status": status,
        "ok": len(ok),
        "weak": weak,
        "broken": broken,
        "grok_ok": grok_ok,
        "grok_miss": grok_miss,
    }
    write_json(out / "writing_report.json", report)
    return report


def verify_prose(item: dict, out: Path) -> dict:
    ws = str(item.get("workspace") or "51")
    if ws == "cumcm":
        path = ROOT / "templates" / "cumcm"
        # also PaperKit templates if present
        pk = Path.home() / "Projects/FullStack/ModelingPaperKit/templates/cumcm"
        target = path if path.exists() else pk
    else:
        target = ROOT / "51" / "mcm_paper_package" / "01_paper"
    r = run_cmd(
        [str(PY), "scripts/check_prose_style.py", "--path", str(target), "--strict-prose", "--format", "json"]
    )
    try:
        payload = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        payload = {"raw": r.stdout, "stderr": r.stderr, "exit": r.returncode}
    crit = int(((payload.get("summary") or {}).get("critical") or 0))
    status = "ok" if crit == 0 and r.returncode == 0 else "fail"
    # template-only critical on cumcm may be expected until fixed
    if ws == "cumcm" and crit > 0:
        status = "fail"
    report = {"track": "prose", "status": status, "target": str(target), "result": payload}
    write_json(out / "prose_report.json", report)
    return report


def verify_model(item: dict, out: Path) -> dict:
    runs = sorted((ROOT / "51" / "runs").glob("e2e_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    run = runs[0] if runs else None
    fitness = None
    metrics = None
    if run:
        art = run / "artifacts"
        fr = run_cmd([str(PY), "scripts/check_model_fitness.py", "--artifacts", str(art), "--format", "json"])
        cr = run_cmd([str(PY), "scripts/check_claim_coverage.py", "--artifacts", str(art), "--format", "json"])
        try:
            fitness = json.loads(fr.stdout or "{}")
        except json.JSONDecodeError:
            fitness = {"raw": fr.stdout, "stderr": fr.stderr}
        try:
            claim = json.loads(cr.stdout or "{}")
        except json.JSONDecodeError:
            claim = {"raw": cr.stdout, "stderr": cr.stderr}
        mpath = run / "tables" / "q1_main_metrics.csv"
        if mpath.exists():
            metrics = mpath.read_text(encoding="utf-8", errors="replace")
    else:
        claim = None
    cv_risk = False
    if metrics and "cv_R2_mean" in metrics:
        # crude: negative mean in csv
        parts = metrics.strip().splitlines()
        if len(parts) >= 2:
            cols = parts[0].split(",")
            vals = parts[1].split(",")
            if "cv_R2_mean" in cols:
                i = cols.index("cv_R2_mean")
                try:
                    cv_risk = float(vals[i]) < 0
                except (ValueError, IndexError):
                    pass
    status = "ok" if run and fitness else "fail"
    if cv_risk:
        status = "partial"  # honest: runnable but generalization risk
    report = {
        "track": "model",
        "status": status,
        "run_dir": str(run) if run else None,
        "fitness": fitness,
        "claim": claim,
        "metrics_csv": metrics,
        "cv_negative_r2_risk": cv_risk,
        "note": "partial=链路能跑但时间 CV 风险需在论文保守表述；勿把全样本 R² 写成泛化证明",
    }
    write_json(out / "model_report.json", report)
    return report


def verify_lock(item: dict, out: Path) -> dict:
    paper_tex = ROOT / "51" / "mcm_paper_package" / "01_paper" / "sections" / "results_answer.tex"
    paper_vals = []
    if paper_tex.exists():
        m = re.search(
            r"校正后数据 \$y\$\s*&([^\\]+)\\",
            paper_tex.read_text(encoding="utf-8"),
        )
        if m:
            paper_vals = [x.strip() for x in m.group(1).split("&")]
    runs = sorted((ROOT / "51" / "runs").glob("e2e_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    e2e_vals = []
    run = runs[0] if runs else None
    if run:
        t = run / "tables" / "table_1_1_calibration.csv"
        if t.exists():
            lines = t.read_text(encoding="utf-8", errors="replace").strip().splitlines()[1:]
            e2e_vals = [ln.split(",")[1].strip() for ln in lines if "," in ln]
    locked = False
    if paper_vals and e2e_vals and len(paper_vals) == len(e2e_vals):
        try:
            locked = all(abs(float(a) - float(b)) < 1e-3 for a, b in zip(paper_vals, e2e_vals))
        except ValueError:
            locked = False
    status = "ok" if locked else "fail"
    report = {
        "track": "lock",
        "status": status,
        "locked": locked,
        "paper_table_1_1_y": paper_vals,
        "latest_e2e_y": e2e_vals,
        "latest_run": str(run) if run else None,
        "blocker": None
        if locked
        else "论文定稿表1.1与最新 e2e（可能无 CEEMDAN）不一致；需指定锁版 run 并重跑定稿链路，或停止用演示 e2e 覆盖正文",
    }
    write_json(out / "lock_report.json", report)
    return report


def verify_paper(item: dict, out: Path) -> dict:
    r = run_cmd([str(PY), "scripts/compile_paper.py", "--workspace", "51"])
    pdf = ROOT / "51" / "mcm_paper_package" / "01_paper" / "out" / "main.pdf"
    pages = None
    if pdf.exists():
        m = run_cmd(["mdls", "-name", "kMDItemNumberOfPages", "-raw", str(pdf)])
        try:
            pages = int((m.stdout or "").strip())
        except ValueError:
            pages = None
    over_budget = pages is not None and pages > 30
    status = "ok" if r.returncode == 0 and pdf.exists() else "fail"
    if status == "ok" and over_budget:
        status = "partial"
    report = {
        "track": "paper",
        "status": status,
        "compile_exit": r.returncode,
        "pdf": str(pdf) if pdf.exists() else None,
        "bytes": pdf.stat().st_size if pdf.exists() else 0,
        "pages": pages,
        "wuyi_body_budget_30": not over_budget if pages is not None else None,
        "log_tail": ((r.stdout or "") + (r.stderr or ""))[-2000:],
        "note": "partial=编译成功但页数超过五一「尽量≤30」建议",
    }
    write_json(out / "paper_report.json", report)
    return report


VERIFY_FN = {
    "fonts": verify_fonts,
    "ai_use": verify_ai_use,
    "writing": verify_writing,
    "prose": verify_prose,
    "model": verify_model,
    "lock": verify_lock,
    "paper": verify_paper,
}


# ------------------------- commands -------------------------


def cmd_status() -> int:
    catalog = load_json(CATALOG, {})
    queue = load_json(QUEUE, {"items": []})
    state = load_json(STATE, {"completed": []})
    loop = load_json(LOOP_STATE, {})
    nxt = None
    for index, item in pending_items(queue, state):
        nxt = enrich(item, index, catalog)
        break
    payload = {
        "root": str(ROOT),
        "stop": STOP.exists(),
        "lock": lock_held(),
        "rotation": catalog.get("rotation"),
        "queue_remaining": sum(1 for _ in pending_items(queue, state)),
        "completed": state.get("completed") or [],
        "next": nxt,
        "last": {
            "id": state.get("last_slice_id"),
            "status": state.get("last_status"),
            "note": state.get("last_note"),
            "at": state.get("last_finished_at"),
            "loop_track": loop.get("last_track"),
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_next() -> int:
    if STOP.exists():
        print("STOP")
        return 2
    held = lock_held()
    if held is not None:
        print(json.dumps(held, ensure_ascii=False))
        return 3
    catalog = load_json(CATALOG, {})
    queue = load_json(QUEUE, {"items": []})
    state = load_json(STATE, {"completed": []})
    chosen = None
    chosen_index = None
    for index, item in pending_items(queue, state):
        chosen = item
        chosen_index = index
        break
    if chosen is None:
        print(json.dumps({"empty": True, "hint": "queue exhausted; add items to iterator/queue.json"}, ensure_ascii=False))
        return 4
    write_json(
        LOCK,
        {"slice_id": chosen["id"], "started_at": now_iso(), "index": chosen_index, "via": "modeling_loop"},
    )
    payload = enrich(chosen, chosen_index, catalog)
    payload["hint"] = (
        "只做这一刀。可自动验收则: python scripts/modeling_loop_manager.py verify --id "
        f"{chosen['id']} ；然后 finish。"
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_verify(slice_id: str | None) -> int:
    catalog = load_json(CATALOG, {})
    queue = load_json(QUEUE, {"items": []})
    state = load_json(STATE, {"completed": []})
    item = None
    if slice_id:
        for it in queue.get("items") or []:
            if it.get("id") == slice_id:
                item = it
                break
    else:
        lock = load_json(LOCK, {})
        slice_id = lock.get("slice_id") if isinstance(lock, dict) else None
        if slice_id:
            for it in queue.get("items") or []:
                if it.get("id") == slice_id:
                    item = it
                    break
        if item is None:
            for _, it in pending_items(queue, state):
                item = it
                slice_id = it.get("id")
                break
    if item is None:
        print(json.dumps({"error": "no slice to verify"}, ensure_ascii=False))
        return 4
    track = str(item.get("track") or "")
    fn = VERIFY_FN.get(track)
    out = slice_dir(str(slice_id))
    if bool(item.get("manual")):
        report = {
            "track": track,
            "status": "manual",
            "note": "本刀需人工完成；verify 不自动改稿。完成后用 finish --status ok|partial",
        }
        write_json(out / "manual_report.json", report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    if fn is None:
        print(json.dumps({"error": f"no verifier for track={track}"}, ensure_ascii=False))
        return 5
    report = fn(item, out)
    report["slice_id"] = slice_id
    report["out_dir"] = str(out)
    write_json(out / "verify.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("status") in {"ok", "accept_with_fallback", "partial", "manual"} else 5


def cmd_finish(slice_id: str, status: str, note: str) -> int:
    catalog = load_json(CATALOG, {})
    state = load_json(STATE, {"completed": [], "next_index": 0})
    queue = load_json(QUEUE, {"items": []})
    items = queue.get("items") or []
    completed = list(state.get("completed") or [])
    # ok / partial both advance the queue; fail leaves the slice pending for retry
    if status in {"ok", "partial"} and slice_id not in completed:
        completed.append(slice_id)
    track = None
    workspace = None
    index = int(state.get("next_index") or 0)
    for i, item in enumerate(items):
        if item.get("id") == slice_id:
            if status in {"ok", "partial"}:
                index = i + 1
            track = item.get("track")
            workspace = item.get("workspace")
            break
    state.update(
        {
            "next_index": index,
            "completed": completed,
            "last_slice_id": slice_id,
            "last_finished_at": now_iso(),
            "last_status": status,
            "last_note": note,
        }
    )
    write_json(STATE, state)
    loop = load_json(LOOP_STATE, {"version": 1})
    loop.update(
        {
            "version": 1,
            "last_id": slice_id,
            "last_track": track,
            "last_workspace": workspace,
            "last_status": status,
            "last_finished_at": now_iso(),
            "last_note": note,
            "rotation": catalog.get("rotation"),
        }
    )
    write_json(LOOP_STATE, loop)
    log = ROOT / "iterator" / "ITERATION_LOG.md"
    if not log.exists():
        log.write_text("# Modeling Loop Iteration Log\n\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as f:
        f.write(f"- {now_iso()} | `{slice_id}` | {status} | {track} | {note}\n")
    if LOCK.exists():
        LOCK.unlink()
    print(json.dumps({"state": state, "loop": loop}, ensure_ascii=False, indent=2))
    return 0


def cmd_defer(slice_id: str | None, note: str) -> int:
    """Move a blocking slice to the end of the queue without marking it completed."""
    queue = load_json(QUEUE, {"items": []})
    items = list(queue.get("items") or [])
    if not slice_id:
        lock = load_json(LOCK, {})
        slice_id = lock.get("slice_id") if isinstance(lock, dict) else None
    if not slice_id:
        print(json.dumps({"error": "no slice_id to defer"}, ensure_ascii=False))
        return 4
    idx = next((i for i, it in enumerate(items) if it.get("id") == slice_id), None)
    if idx is None:
        print(json.dumps({"error": f"unknown id {slice_id}"}, ensure_ascii=False))
        return 4
    item = items.pop(idx)
    item["deferred_note"] = note or item.get("deferred_note") or "deferred"
    item["deferred_at"] = now_iso()
    items.append(item)
    queue["items"] = items
    write_json(QUEUE, queue)
    if LOCK.exists():
        LOCK.unlink()
    log = ROOT / "iterator" / "ITERATION_LOG.md"
    if not log.exists():
        log.write_text("# Modeling Loop Iteration Log\n\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as f:
        f.write(f"- {now_iso()} | `{slice_id}` | defer | — | {note}\n")
    print(json.dumps({"deferred": slice_id, "note": note, "new_tail": items[-1].get("id")}, ensure_ascii=False, indent=2))
    return 0


def cmd_run_once() -> int:
    """next → verify → finish(auto map status). Manual slices stop after next."""
    code = cmd_next()
    if code != 0:
        return code
    # re-read lock
    lock = load_json(LOCK, {})
    slice_id = lock.get("slice_id")
    queue = load_json(QUEUE, {"items": []})
    item = next((it for it in queue.get("items") or [] if it.get("id") == slice_id), None)
    if item and item.get("manual"):
        print(json.dumps({"paused_manual": True, "id": slice_id, "goal": item.get("goal")}, ensure_ascii=False))
        return 0
    vcode = cmd_verify(slice_id)
    report = load_json(slice_dir(slice_id) / "verify.json", {})
    st = report.get("status") or "fail"
    finish_status = {
        "ok": "ok",
        "accept_with_fallback": "ok",
        "partial": "partial",
        "fail": "fail",
        "manual": "partial",
    }.get(st, "fail")
    note = report.get("note") or report.get("blocker") or st
    cmd_finish(str(slice_id), finish_status, str(note)[:240])
    if finish_status == "fail":
        print(
            json.dumps(
                {
                    "blocked": True,
                    "id": slice_id,
                    "hint": "硬阻塞未过。修好后重跑 verify，或: modeling_loop_manager.py defer --id "
                    f"{slice_id} --note '…' 把该刀挪到队尾继续别的。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0 if vcode == 0 else 5


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="show next slice and queue")
    sub.add_parser("next", help="claim next slice (sets lock)")
    sub.add_parser("catalog")
    sub.add_parser("run-once", help="next + verify + finish one automatable slice")
    v = sub.add_parser("verify", help="run auto verifier for slice")
    v.add_argument("--id", default="")
    d = sub.add_parser("defer", help="move blocking slice to end of queue")
    d.add_argument("--id", default="")
    d.add_argument("--note", default="deferred")
    fin = sub.add_parser("finish")
    fin.add_argument("--id", required=True)
    fin.add_argument("--status", choices=("ok", "partial", "fail"), required=True)
    fin.add_argument("--note", default="")
    args = parser.parse_args()
    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "catalog":
        print(json.dumps(load_json(CATALOG, {}), ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "next":
        return cmd_next()
    if args.cmd == "verify":
        return cmd_verify(args.id or None)
    if args.cmd == "run-once":
        return cmd_run_once()
    if args.cmd == "defer":
        return cmd_defer(args.id or None, args.note)
    return cmd_finish(args.id, args.status, args.note)


if __name__ == "__main__":
    raise SystemExit(main())
