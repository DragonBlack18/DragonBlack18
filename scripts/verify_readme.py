#!/usr/bin/env python3
"""Validate the Citadel profile README using only the Python standard library."""
from __future__ import annotations
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
REQUIRED_GIFS = ('iron-vow.gif', 'templar-cathedral-watch.gif', 'crimson-eclipse.gif', 'ashen-citadel.gif', 'crimson-gate.gif')
REQUIRED_PROJECTS = ('deploycraft', 'omniforge', 'vyrnode', 'vitality', 'atlas', 'iiad')
FORBIDDEN_SVG_TAGS = {'script', 'foreignObject', 'iframe', 'animate', 'animateTransform', 'set'}

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.images = []
        self.anchors = []
        self.fragments = []
        self.details = 0
        self.detail_closes = 0
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'img':
            self.images.append(attributes)
        if tag == 'a' and attributes.get('name'):
            self.anchors.append(attributes['name'])
        if tag == 'a' and (attributes.get('href') or '').startswith('#'):
            self.fragments.append(attributes['href'][1:])
        if tag == 'details':
            self.details += 1
    def handle_endtag(self, tag):
        if tag == 'details':
            self.detail_closes += 1

def check() -> list[str]:
    issues = []
    if not README.is_file():
        return [f'missing {README}']
    source = README.read_text(encoding='utf-8')
    html = Scan()
    html.feed(source)
    if html.details != html.detail_closes:
        issues.append(f'unbalanced details elements: {html.details}/{html.detail_closes}')
    if len(html.anchors) != len(set(html.anchors)):
        issues.append('duplicate named anchors')
    issues.extend(f'broken anchor #{anchor}' for anchor in html.fragments if anchor not in html.anchors)
    if source.count('```') % 2:
        issues.append('unbalanced fenced code blocks')
    for image in html.images:
        if image.get('alt') is None:
            issues.append(f'image without alt: {image.get("src", "")[:90]}')
    refs = re.findall(r'(?:src|href)="\./(assets/[^"#?]+)', source)
    refs += re.findall(r'!\[[^\]]*\]\(\./(assets/[^)]+)\)', source)
    for rel in sorted(set(refs)):
        path = (ROOT / rel).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            issues.append(f'missing or unsafe local asset {rel}')
    for gif in REQUIRED_GIFS:
        if not (ROOT / 'assets' / gif).is_file() or gif not in source:
            issues.append(f'historical GIF lost: {gif}')
    for key in REQUIRED_PROJECTS:
        if f'assets/citadel-v4/project-{key}.svg' not in source:
            issues.append(f'missing V4 portfolio reference: {key}')
    if not (ROOT / 'assets' / 'citadel-v4').is_dir():
        issues.append('assets/citadel-v4 not found')
    else:
        for svg_path in sorted((ROOT / 'assets' / 'citadel-v4').glob('*.svg')):
            try:
                svg = ET.parse(svg_path).getroot()
                if svg.tag != '{http://www.w3.org/2000/svg}svg':
                    issues.append(f'not a root SVG: {svg_path.name}')
                if not svg.attrib.get('viewBox'):
                    issues.append(f'viewBox missing: {svg_path.name}')
                for node in svg.iter():
                    if node.tag.rsplit('}', 1)[-1] in FORBIDDEN_SVG_TAGS:
                        issues.append(f'forbidden SVG tag in {svg_path.name}')
                    for attr, val in node.attrib.items():
                        key = attr.rsplit('}', 1)[-1].lower()
                        if key.startswith('on') or ('href' in key and (val.startswith('http') or val.startswith('data:'))):
                            issues.append(f'unsafe SVG attribute in {svg_path.name}')
            except ET.ParseError as exc:
                issues.append(f'invalid SVG {svg_path.name}: {exc}')
    return issues

if __name__ == '__main__':
    errors = check()
    for error in errors:
        print('[FAIL]', error)
    if errors:
        print(f'[FAIL] README integrity: {len(errors)} issue(s)')
        sys.exit(1)
    print('[PASS] README integrity: local images, SVGs, links, anchors, historic GIFs and accessibility checks')
