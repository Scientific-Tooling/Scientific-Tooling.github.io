from __future__ import annotations

import re
import sys
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from render_guide import GUIDES, LEGACY_PAGES, MANUAL_URL, ROOT, legacy_markdown, render, render_legacy


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.blocks = [], set(), []
        self.buttons, self.canonicals = 0, []
        self.in_code = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if attrs.get("href"):
            self.links.append(attrs["href"])
        if attrs.get("src"):
            self.links.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs["href"])
        if tag == "button" and attrs.get("class") == "copy-button":
            self.buttons += 1
        if tag == "code" and attrs.get("class") in {"language-powershell", "language-bash", "language-text"}:
            self.in_code = True
            self.blocks.append("")

    def handle_endtag(self, tag):
        if tag == "code":
            self.in_code = False

    def handle_data(self, data):
        if self.in_code:
            self.blocks[-1] += data


class GuideTest(unittest.TestCase):
    def test_generated_page_is_current(self):
        for guide in GUIDES:
            with self.subTest(guide=guide.name):
                self.assertEqual(guide.output.read_text(encoding="utf-8"), render(guide))
        for slug in LEGACY_PAGES:
            with self.subTest(legacy=slug):
                output = ROOT / "guides" / slug / "index.html"
                self.assertEqual(output.read_text(encoding="utf-8"), render_legacy(slug))
                if slug != "rks-apw":
                    self.assertEqual((ROOT / "guides" / f"{slug}.md").read_text(encoding="utf-8"), legacy_markdown(slug))

    def test_every_copyable_command_matches_the_source_exactly(self):
        for guide in GUIDES:
            with self.subTest(guide=guide.name):
                blocks = re.findall(fr"```{guide.language}\n(.*?)\n```", guide.source.read_text(encoding="utf-8"), re.S)
                page = Page(guide.output)
                self.assertGreater(len(blocks), 0)
                self.assertEqual([block.rstrip("\n") for block in page.blocks], blocks)
                self.assertEqual(page.buttons, len(blocks))

    def test_quick_start_is_the_only_onboarding_destination(self):
        home = Page(ROOT / "index.html")
        urls = [node.text for node in ET.parse(ROOT / "sitemap.xml").findall("{*}url/{*}loc")]
        guide = GUIDES[0]
        self.assertGreaterEqual(home.links.count(f"./guides/{guide.slug}/"), 4)
        self.assertEqual(Page(guide.output).canonicals, [guide.url])
        self.assertIn(guide.url, urls)
        self.assertNotIn('class="platform-switch"', guide.output.read_text(encoding="utf-8"))
        self.assertIn(MANUAL_URL + "README.md", Page(guide.output).links)
        for slug in LEGACY_PAGES:
            with self.subTest(legacy=slug):
                self.assertNotIn(f"./guides/{slug}/", home.links)
                self.assertNotIn(f"https://scientifictooling.org/guides/{slug}/", urls)
                page = Page(ROOT / "guides" / slug / "index.html")
                self.assertIn(f"../{guide.slug}/", page.links)
                self.assertIn(MANUAL_URL + LEGACY_PAGES[slug][0], page.links)
                self.assertEqual(page.canonicals, [guide.url])

    def test_owned_links_assets_and_fragments_resolve(self):
        for path in (ROOT / "index.html", *(guide.output for guide in GUIDES),
                     *(ROOT / "guides" / slug / "index.html" for slug in LEGACY_PAGES)):
            for link in Page(path).links:
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc:
                    continue
                target = ((ROOT if parsed.path.startswith("/") else path.parent) / unquote(parsed.path.lstrip("/"))).resolve() if parsed.path else path
                relative = target.relative_to(ROOT).as_posix()
                # The project website is deployed by its own repository.
                if relative == "structured-intelligence" or relative.startswith("structured-intelligence/"):
                    continue
                if target.is_dir():
                    target = target / "index.html"
                with self.subTest(page=path.name, link=link):
                    self.assertTrue(target.is_file(), target)
                    if parsed.fragment and target.suffix == ".html":
                        self.assertIn(unquote(parsed.fragment), Page(target).ids)

if __name__ == "__main__":
    unittest.main()
