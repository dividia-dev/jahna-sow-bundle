#!/usr/bin/env python3
"""Render the Phase 2 + Phase 3 budgetary quote mockups to PDF."""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent.resolve()
DOCS = ["phase2", "phase3"]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for name in DOCS:
            html = HERE / f"{name}.html"
            pdf = HERE / f"{name}.pdf"
            if not html.exists():
                print(f"  SKIP {name}: {html.name} missing")
                continue
            page.goto(f"file://{html}", wait_until="networkidle")
            page.wait_for_timeout(500)
            page.pdf(
                path=str(pdf),
                format="Letter",
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                print_background=True,
                prefer_css_page_size=True,
            )
            size_kb = pdf.stat().st_size / 1024
            print(f"  OK   {pdf.name}  ({size_kb:.1f} KB)")
        browser.close()


if __name__ == "__main__":
    main()
