#!/usr/bin/env python3
import json
from _build_inventions_page import parse_docx

data = parse_docx()
refs = []
for g in data["references"]["groups"]:
    for ii, item in enumerate(g["items"]):
        if item.startswith("Note on Sources"):
            continue
        refs.append({"id": f"{g['slug']}:{ii}", "group": g["title"], "text": item})
print(json.dumps(refs, indent=2, ensure_ascii=False))
