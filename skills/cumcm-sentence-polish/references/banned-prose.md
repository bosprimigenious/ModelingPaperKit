# Banned Prose (write-time, not only polish-time)

Load this file **before drafting or rewriting any paper body section**.
Machine gate: `python3 scripts/check_prose_style.py` (rules in `scripts/prose_rules.json`).

These phrases are banned in **正文** (abstract, sections, captions).
They may appear in skills, agent notes, checklists — never in `.tex` body.

---

## 1. Hollow inference (根据…可知 / 由此可见)

| Ban | Why | Prefer |
|-----|-----|--------|
| 根据…可知 / 根据…可以知道 | 空衔接，不写证据 | 直接写：由表2，MAE=0.12 |
| 由…可知 / 由…可得 | 同上 | 在验证窗内，主模型 MAE 低于基线 18%（表2） |
| 由此可见 / 由此可得 / 据此可知 | 假装推理 | 用具体对象：该参数扰动下指标变化不超过… |
| 我们得出结论 / 不难发现 / 显而易见 | 评论腔 | 陈述事实与范围 |
| It can be seen that / As can be seen | 英文空壳 | State the measurement |
| Therefore, / Thus, / Hence, 起句 | 无前提的连接词 | 用具体条件领起 |
| However, 起句 | 假转折 | 写清对比对象与数值差 |
| 孤立英文 ever | 口语/填充 | 删或改成具体时间/条件 |
| 句首「然而，」「但是，」 | 空转折 | 写：与基线相比 / 在参数 λ=… 时 |

**Rewrite pattern**

```text
BAD:  根据上述分析可知，模型效果较好。
GOOD: 在附件1验证集上，主模型 MAE 为 0.12，相对基线下降 18%（表2）。
```

```text
BAD:  由此可见，该方法具有较好的稳定性。
GOOD: 当平滑系数在 [0.2, 0.8] 内变化时，MAE 波动不超过 0.03（图5）。
```

---

## 2. AI filler / empty praise

近年来；随着…的发展；具有重要意义；进行了一定研究；
效果较好；较为合理；众所周知；赋能；助力；深度融合；
在一定程度上；发挥着重要作用；广阔的应用前景；提供参考意义；
值得注意的是；需要指出的是；综上所述（空套）；总而言之；简而言之。

---

## 3. Meta / instructional leakage

不要…；请勿…；禁止…；Do not…；You should not…；
作为 AI / 助手；我将帮你；根据你的要求；this skill；Guardrails。

---

## 4. Write-time hard rules (for the drafting agent)

1. **Every claim sentence** must name at least one of: 表/图/式/附录/数据字段/参数范围.
2. **No connector-only openers**: do not start a paragraph with 然而/但是/综上所述/Therefore/However/Thus.
3. **No “可知” scaffolding**: if you need inference, write `由式(3)与表2，…` with the actual objects, not `根据分析可知`.
4. **No praise without metric**: delete 较好/合理/显著 unless a number and baseline sit in the same sentence.
5. After any body edit, run:
   ```bash
   python3 scripts/check_prose_style.py --path <edited.tex> --strict-prose
   ```
   Fix until exit code 0.

---

## 5. Allowed technical “根据/由”

These are OK when the object is a **named artifact**, not vague “分析/上述”:

- 由式 (3) 得 …
- 由表 2 得 …
- 根据附件 1 的字段定义，…
- 由假设 H2，…

If the checker false-flags a legitimate line, add `%# prose:allow` on that line only.
