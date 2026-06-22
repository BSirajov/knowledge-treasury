#!/usr/bin/env python3
"""Knowledge Treasury favicon assets and HTML link snippets."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image

from _paths import ROOT

IMAGES = ROOT / "images"
SOURCE_CANDIDATES = [
    Path(
        r"C:\Users\BSira\.cursor\projects\c-Users-BSira-Documents-GitHub-knowledge-treasury\assets"
        r"\c__Users_BSira_AppData_Roaming_Cursor_User_workspaceStorage_5081ded2094c44aff111dd8dd64d1789_images_kt-logo-769dc738-b3ae-45a1-afcb-69d60b2ed989.png"
    ),
    IMAGES / "kt-logo.png",
]

FAVICON_SIZES = {
    "kt-favicon.png": 32,
    "apple-touch-icon.png": 180,
    "kt-logo-192.png": 192,
}

ICON_LINK_RE = re.compile(
    r'<link rel="(?:icon|apple-touch-icon)"[^>]*>\s*',
    re.IGNORECASE,
)


def resolve_source() -> Path:
    for candidate in SOURCE_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("Knowledge Treasury logo source image not found")


def build_assets(source: Path | None = None) -> None:
    source = source or resolve_source()
    IMAGES.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as img:
        logo = img.convert("RGBA")
        shutil.copy2(source, IMAGES / "kt-logo.png")
        for name, size in FAVICON_SIZES.items():
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(IMAGES / name, format="PNG", optimize=True)


def favicon_links(asset_root: str) -> str:
    """asset_root is relative prefix to /images, e.g. '../' or '../../../'."""
    base = f"{asset_root}images/"
    return (
        f'<link rel="icon" href="{base}kt-favicon.png" type="image/png" sizes="32x32"/>\n'
        f'<link rel="icon" href="{base}kt-logo.png" type="image/png" sizes="512x512"/>\n'
        f'<link rel="apple-touch-icon" href="{base}apple-touch-icon.png"/>'
    )


def asset_root_for_html(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else "./"


def inject_favicon_links(html: str, asset_root: str) -> str:
    cleaned = ICON_LINK_RE.sub("", html)
    block = favicon_links(asset_root)
    if "<!-- kt-seo -->" in cleaned:
        return cleaned.replace("<!-- kt-seo -->", f"<!-- kt-seo -->\n{block}", 1)
    if '<meta name="viewport"' in cleaned:
        return cleaned.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>\n'
            + block,
            1,
        )
    return cleaned.replace("<head>", f"<head>\n{block}", 1)


def apply_to_html_tree() -> int:
    count = 0
    for path in ROOT.rglob("*.html"):
        if any(part in {".git", "preview", "documents"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        updated = inject_favicon_links(text, asset_root_for_html(path))
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            count += 1
    return count


def main() -> None:
    build_assets()
    updated = apply_to_html_tree()
    print(f"Favicon assets written to {IMAGES.relative_to(ROOT)}")
    print(f"Updated favicon links in {updated} HTML files")


if __name__ == "__main__":
    main()
