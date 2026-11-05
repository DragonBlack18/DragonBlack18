#!/usr/bin/env python3
"""Audit the actually published GitHub profile with a browser on a CI runner.

This complements (and does not replace) scripts/verify_readme.py.
The screenshots and audit.json are uploaded as a GitHub Actions artifact.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = os.environ.get("PROFILE_URL", "https://github.com/DragonBlack18")
OUT = Path(os.environ.get("AUDIT_OUT", "artifacts/profile-live-audit"))
OUT.mkdir(parents=True, exist_ok=True)
WIDTHS = (360, 390, 768, 1440)
THEMES = ("dark", "light")
EXPECTED_PROJECTS = (
    "project-deploycraft.svg", "project-omniforge.svg",
    "project-vyrnode.svg", "project-vitality.svg",
    "project-atlas.svg", "project-iiad.svg",
)
CHAPTER_ANCHORS = (
    "codex-whoami", "codex-orders", "codex-armory",
    "codex-projects", "codex-oath", "codex-archive",
)


def audit_case(browser, width: int, scheme: str) -> dict:
    context = browser.new_context(
        viewport={"width": width, "height": 900},
        device_scale_factor=1,
        color_scheme=scheme,
        reduced_motion="reduce",
        locale="pt-BR",
        is_mobile=width < 600,
        has_touch=width < 600,
    )
    page = context.new_page()
    result = {
        "width": width, "theme": scheme, "url": PROFILE,
        "status": None, "errors": [], "warnings": [], "metrics": {},
    }
    try:
        response = page.goto(PROFILE, wait_until="domcontentloaded", timeout=60000)
        result["status"] = response.status if response else None

        # GitHub profile README generally sits inside an article.markdown-body.
        try:
            page.wait_for_selector(".markdown-body", timeout=30000)
        except Exception:
            result["errors"].append("Public profile README markdown-body not found")
        page.wait_for_timeout(1200)

        metrics = page.evaluate(
            """() => {
              const candidates = [...document.querySelectorAll('.markdown-body')];
              const article = candidates.find(el => /CAPÍTULO I|THE CRIMSON CODEX/.test(el.innerText || ''))
                || candidates[0] || null;
              const images = article ? [...article.querySelectorAll('img')] : [];
              const projectImages = images.filter(img => (img.getAttribute('src') || '').includes('citadel-v4/project-'));
              const imageState = images
                .filter(img => img.getClientRects().length > 0)
                .map(img => ({
                   src: img.getAttribute('src') || '',
                   alt: img.getAttribute('alt'),
                   complete: img.complete,
                   naturalWidth: img.naturalWidth,
                   clientWidth: Math.round(img.getBoundingClientRect().width)
                }));
              const links = article ? [...article.querySelectorAll('a[href]')] : [];
              const navLinks = links.filter(a => /codex-(whoami|orders|armory|projects|oath|archive)/.test(a.getAttribute('href') || ''));
              const navigation = navLinks.map(a => {
                const h = a.getAttribute('href') || '';
                const fragment = decodeURIComponent(h.split('#').slice(1).join('#'));
                return {href:h, targetExists: !!(
                  document.getElementById(fragment) ||
                  document.getElementById('user-content-' + fragment) ||
                  document.getElementById(fragment.replace(/^user-content-/, '')) ||
                  document.querySelector('[name="' + CSS.escape(fragment) + '"]') ||
                  document.querySelector('[name="' + CSS.escape('user-content-' + fragment) + '"]') ||
                  document.querySelector('[name="' + CSS.escape(fragment.replace(/^user-content-/, '')) + '"]')
                )};
              });
              const anchorMarkers = [...document.querySelectorAll('[id], [name]')]
                .filter(el => /codex|cap[ií]tulo/i.test((el.id || '') + ' ' + (el.getAttribute('name') || '')))
                .slice(0, 50).map(el => ({tag:el.tagName, id:el.id, name:el.getAttribute('name')}));
              const titleSections = article ? [...article.querySelectorAll('h2')].map(x => x.innerText) : [];
              const topImgs = images.filter(img => img.getClientRects().length > 0);
              const contentWidth = Math.round(article?.getBoundingClientRect().width || 0);
              const documentWidth = document.documentElement.scrollWidth;
              const viewportWidth = document.documentElement.clientWidth;
              const projectTitles = projectImages.map(img => ({
                src: img.getAttribute('src'),
                clickable: !!img.closest('a[href]'),
                alt: img.getAttribute('alt') || '',
                width: Math.round(img.getBoundingClientRect().width)
              }));
              return {
                hasArticle: !!article,
                bodyTextIncludesCodex: !!article && /THE CRIMSON CODEX/.test(article.innerText),
                sectionCount: titleSections.length,
                sectionHeadings: titleSections,
                articleWidth: contentWidth,
                documentWidth, viewportWidth,
                horizontalOverflow: Math.max(0, documentWidth - viewportWidth),
                imageCount: images.length,
                visibleImageCount: topImgs.length,
                imageState,
                projects: projectTitles,
                navigation,
                anchorMarkers,
                htmlMode: document.documentElement.getAttribute('data-color-mode'),
                resolvedTheme: document.documentElement.getAttribute('data-dark-theme') || document.documentElement.getAttribute('data-light-theme')
              };
            }"""
        )
        result["metrics"] = metrics
        if result["status"] is not None and result["status"] >= 400:
            result["errors"].append(f"HTTP status: {result['status']}")
        if not metrics["hasArticle"]:
            result["errors"].append("Profile README article not rendered")
        if not metrics["bodyTextIncludesCodex"]:
            result["errors"].append("Expected Crimson Codex text not found")
        if metrics["horizontalOverflow"] > 2:
            result["errors"].append(f"Horizontal overflow: {metrics['horizontalOverflow']} px")
        if metrics["sectionCount"] < 6:
            result["errors"].append(f"Expected >=6 section headings, found {metrics['sectionCount']}")
        projects = metrics["projects"]
        if len(projects) != 6:
            result["errors"].append(f"Expected 6 V4 project images, found {len(projects)}")
        if any(not p["clickable"] for p in projects):
            result["errors"].append("A V4 portfolio image has no clickable link")
        if any(not p["alt"] for p in projects):
            result["errors"].append("A V4 portfolio image has no accessible name")
        if len(metrics["navigation"]) < 6:
            result["warnings"].append(f"Only {len(metrics['navigation'])} chapter navigation links detected")
        if any(not a["targetExists"] for a in metrics["navigation"]):
            result["errors"].append("Chapter navigation link has no in-page destination")
            print("  NAVIGATION DEBUG:", json.dumps(metrics["navigation"], ensure_ascii=False), flush=True)
            print("  ANCHOR MARKERS:", json.dumps(metrics["anchorMarkers"], ensure_ascii=False), flush=True)
        # Functional navigation test: the raw fragment must actually move the viewport.
        # GitHub namespaces explicit Markdown anchors as "user-content-*".
        try:
            page.locator('.markdown-body a[href="#codex-projects"]').first.click(timeout=10000)
            page.wait_for_timeout(500)
            nav_motion = page.evaluate("""() => {
                const target = document.querySelector('a[name="user-content-codex-projects"]');
                return {
                    scrollY: Math.round(window.scrollY),
                    targetTop: target ? Math.round(target.getBoundingClientRect().top) : null,
                    hash: window.location.hash
                };
            }""")
            result["metrics"]["navigationClick"] = nav_motion
            if nav_motion["targetTop"] is None or abs(nav_motion["targetTop"]) > 700 or nav_motion["scrollY"] < 300:
                result["errors"].append("Clicking PROJECTS did not scroll to its chapter")
                print("  CLICK DEBUG:", nav_motion, flush=True)
        except Exception as exc:
            result["errors"].append(f"Could not test PROJECTS navigation click: {type(exc).__name__}: {exc}")
        broken = [img["src"] for img in metrics["imageState"] if img["complete"] and img["naturalWidth"] == 0]
        unloaded = [img["src"] for img in metrics["imageState"] if not img["complete"]]
        if broken:
            result["errors"].append(f"{len(broken)} visible image(s) failed to load")
            result["metrics"]["brokenVisibleImages"] = broken
        if unloaded:
            result["warnings"].append(f"{len(unloaded)} visible image(s) not loaded when inspected")
            result["metrics"]["unloadedVisibleImages"] = unloaded
        # Screenshot actual GitHub page (including UI chrome) at this viewport.
        page.screenshot(path=str(OUT / f"github-profile-{scheme}-{width}.png"), full_page=True, animations="disabled", timeout=60000)
    except Exception as exc:
        result["errors"].append(f"Browser audit exception: {type(exc).__name__}: {exc}")
        try:
            page.screenshot(path=str(OUT / f"github-profile-{scheme}-{width}-error.png"), full_page=True, timeout=15000)
        except Exception:
            pass
    finally:
        context.close()
    result["passed"] = not result["errors"]
    return result


def main() -> int:
    started = time.time()
    checks = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        try:
            for theme in THEMES:
                for width in WIDTHS:
                    check = audit_case(browser, width, theme)
                    checks.append(check)
                    headline = (f"{theme:5s} {width:4d}px  "
                                f"HTTP={check['status']}  "
                                f"overflow={check['metrics'].get('horizontalOverflow', 'n/a')}  "
                                f"projects={len(check['metrics'].get('projects', []))}")
                    print(f"[{'PASS' if check['passed'] else 'FAIL'}] {headline}", flush=True)
                    for error in check["errors"]:
                        print("  ERROR:", error, flush=True)
                    for warning in check["warnings"]:
                        print("  WARN: ", warning, flush=True)
        finally:
            browser.close()
    document = {
        "tested_url": PROFILE,
        "testing_mode": "GitHub-hosted runner / live public GitHub page / Chromium",
        "cases": checks,
        "passed": all(x["passed"] for x in checks),
        "duration_seconds": round(time.time() - started, 1),
        "limitations": [
            "Screenshots are made in GitHub Actions Chromium, not on the user's physical phone",
            "External badge and GIF performance are not benchmarked",
            "This tests the live GitHub site at execution time, not a synthetic GitHub-like mockup",
        ],
    }
    (OUT / "audit.json").write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TOTAL: {sum(x['passed'] for x in checks)}/{len(checks)} passed", flush=True)
    return 0 if document["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
