#!/usr/bin/env python3
"""Build a HubSpot CMS theme from the static site.

The static site (index.html, css/, js/, assets/) stays the single source of truth.
This script turns it into a HubSpot theme in build/hubspot/the-animesy-magazine/:

    theme.json, fields.json
    templates/magazine.html   <- index.html with HubL asset URLs + HubSpot includes
    css/  js/  assets/        <- copied; url(...) in CSS rewritten to get_asset_url

PDFs are not allowed in HubSpot's Design Manager, so the issues in assets/issues/
are uploaded to the File Manager (folder the-animesy-magazine/issues) by the
GitHub workflow and linked as /hubfs/the-animesy-magazine/issues/<file>.pdf,
which HubSpot serves on every domain connected to the account (theanimesy.com).

Usage:  python3 scripts/build_hubspot_theme.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME_NAME = "the-animesy-magazine"
OUT = ROOT / "build" / "hubspot" / THEME_NAME
FILE_MANAGER_ISSUES = f"/hubfs/{THEME_NAME}/issues/"

TEMPLATE_ANNOTATION = """<!--
  templateType: page
  label: The Animesy Magazine
  isAvailableForNewContent: true
-->
"""


def asset_url(rel_from_template: str) -> str:
    return "{{ get_asset_url('" + rel_from_template + "') }}"


def build_template(html: str) -> str:
    # 1. PDFs -> File Manager (keep #page=N fragments)
    html = re.sub(r'(["\'])assets/issues/', r"\1" + FILE_MANAGER_ISSUES, html)

    # 2. Every other local asset/css/js reference -> theme asset URL.
    #    The template lives in templates/, so paths are relative to that folder.
    def repl(m):
        quote, path = m.group(1), m.group(2)
        return quote + asset_url("../" + path)

    html = re.sub(r'(["\'])((?:assets|css|js)/[^"\'#?]+)(?=["\'#?])', repl, html)

    # 3. Required HubSpot includes (tracking code, forms, cookie banner, etc.)
    if "standard_header_includes" not in html:
        html = html.replace("</head>", "{{ standard_header_includes }}\n</head>", 1)
    if "standard_footer_includes" not in html:
        html = html.replace("</body>", "{{ standard_footer_includes }}\n</body>", 1)

    return TEMPLATE_ANNOTATION + html


def build_css(css: str) -> str:
    # CSS lives in css/, so '../assets/...' is already relative to the CSS file.
    def repl(m):
        path = m.group(2)
        return "url(" + asset_url(path) + ")"

    return re.sub(r"url\((['\"]?)(\.\./assets/[^'\")]+)\1\)", repl, css)


def check_no_hubl(name: str, text: str) -> None:
    # HubSpot parses templates and CSS as HubL; stray delimiters would break the build.
    for token in ("{{", "{%", "{#"):
        if token in text:
            raise SystemExit(f"{name} contains '{token}' — escape it with {{% raw %}} before deploying.")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "templates").mkdir(parents=True)

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    check_no_hubl("index.html", index)
    (OUT / "templates" / "magazine.html").write_text(build_template(index), encoding="utf-8")

    (OUT / "css").mkdir()
    for css_file in (ROOT / "css").glob("*.css"):
        css = css_file.read_text(encoding="utf-8")
        check_no_hubl(css_file.name, css)
        (OUT / "css" / css_file.name).write_text(build_css(css), encoding="utf-8")

    shutil.copytree(ROOT / "js", OUT / "js")
    shutil.copytree(ROOT / "assets", OUT / "assets", ignore=shutil.ignore_patterns("issues"))

    (OUT / "theme.json").write_text(json.dumps({
        "label": "The Animesy Magazine",
        "preview_path": "./templates/magazine.html",
        "screenshot_path": "./assets/covers/issue-02-may-2026.jpg",
        "enable_domain_stylesheets": False,
        "version": "1",
        "author": {"name": "The Animesy", "email": "support@theanimesy.com",
                   "url": "https://theanimesy.com"},
    }, indent=2) + "\n", encoding="utf-8")
    (OUT / "fields.json").write_text("[]\n", encoding="utf-8")

    files = sum(1 for p in OUT.rglob("*") if p.is_file())
    print(f"Built HubSpot theme in {OUT.relative_to(ROOT)} ({files} files)")


if __name__ == "__main__":
    main()
