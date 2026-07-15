# Source Log Schema

Use a source log during preparation and contest work.

```text
source_id:
type: paper | book | dataset | website | software | official_notice | ai_tool
title:
authors_or_provider:
url_or_identifier:
publish_date:
access_date:
used_for:
paper_citation_key:
notes:
```

Rules:

- Official notices should include exact URL and access date.
- Datasets should include original filename and transformation notes.
- Software should include package name and version when relevant.
- A source used only for inspiration still needs a note if it shapes the model.
