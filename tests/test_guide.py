from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from render_guide import OUTPUT, ROOT, SOURCE, URL, render


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
        if tag == "code" and attrs.get("class") == "language-powershell":
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
        self.assertEqual(OUTPUT.read_text(encoding="utf-8"), render())

    def test_every_copyable_command_matches_the_source_exactly(self):
        blocks = re.findall(r"```powershell\n(.*?)\n```", SOURCE.read_text(encoding="utf-8"), re.S)
        page = Page(OUTPUT)
        self.assertGreater(len(blocks), 0)
        self.assertEqual([block.rstrip("\n") for block in page.blocks], blocks)
        self.assertEqual(page.buttons, len(blocks))

    def test_walkthrough_is_discoverable_and_has_one_canonical_url(self):
        self.assertGreaterEqual(Page(ROOT / "index.html").links.count("./guides/rks-apw-windows/"), 4)
        self.assertEqual(Page(OUTPUT).canonicals, [URL])
        urls = ET.parse(ROOT / "sitemap.xml").findall("{*}url/{*}loc")
        self.assertIn(URL, [node.text for node in urls])

    def test_owned_links_assets_and_fragments_resolve(self):
        for path in (ROOT / "index.html", OUTPUT):
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

    @unittest.skipUnless(shutil.which("powershell.exe"), "Windows PowerShell 5.1 syntax check")
    def test_windows_powershell_parses_every_documented_block(self):
        blocks = re.findall(r"```powershell\n(.*?)\n```", SOURCE.read_text(encoding="utf-8"), re.S)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "walkthrough.ps1"
            path.write_text("\n".join(blocks), encoding="utf-8-sig")
            command = "$tokens=$null; $errors=$null; [void][System.Management.Automation.Language.Parser]::ParseFile($args[0],[ref]$tokens,[ref]$errors); if($errors.Count){$errors | Out-String | Write-Error; exit 1}"
            checker = Path(temporary) / "check.ps1"
            checker.write_text(command, encoding="utf-8-sig")
            result = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(checker), str(path)], capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
