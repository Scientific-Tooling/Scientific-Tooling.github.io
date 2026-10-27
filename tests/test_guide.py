from __future__ import annotations

import re
import os
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
from render_guide import GUIDES, INDEX_OUTPUT, INDEX_URL, ROOT, render, render_index


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
        if tag == "code" and attrs.get("class") in {"language-powershell", "language-bash"}:
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
        self.assertEqual(INDEX_OUTPUT.read_text(encoding="utf-8"), render_index())

    def test_every_copyable_command_matches_the_source_exactly(self):
        for guide in GUIDES:
            with self.subTest(guide=guide.name):
                blocks = re.findall(fr"```{guide.language}\n(.*?)\n```", guide.source.read_text(encoding="utf-8"), re.S)
                page = Page(guide.output)
                self.assertGreater(len(blocks), 0)
                self.assertEqual([block.rstrip("\n") for block in page.blocks], blocks)
                self.assertEqual(page.buttons, len(blocks))

    def test_walkthrough_is_discoverable_and_has_one_canonical_url(self):
        home = Page(ROOT / "index.html")
        self.assertGreaterEqual(home.links.count("./guides/rks-apw/"), 2)
        urls = ET.parse(ROOT / "sitemap.xml").findall("{*}url/{*}loc")
        self.assertEqual(Page(INDEX_OUTPUT).canonicals, [INDEX_URL])
        self.assertIn(INDEX_URL, [node.text for node in urls])
        for guide in GUIDES:
            with self.subTest(guide=guide.name):
                self.assertGreaterEqual(home.links.count(f"./guides/{guide.slug}/"), 2)
                self.assertIn(f"../{guide.slug}/", Page(INDEX_OUTPUT).links)
                self.assertEqual(Page(guide.output).canonicals, [guide.url])
                self.assertIn(guide.url, [node.text for node in urls])

    def test_owned_links_assets_and_fragments_resolve(self):
        for path in (ROOT / "index.html", INDEX_OUTPUT, *(guide.output for guide in GUIDES)):
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
        blocks = re.findall(r"```powershell\n(.*?)\n```", GUIDES[0].source.read_text(encoding="utf-8"), re.S)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "walkthrough.ps1"
            path.write_text("\n".join(blocks), encoding="utf-8-sig")
            command = "$tokens=$null; $errors=$null; [void][System.Management.Automation.Language.Parser]::ParseFile($args[0],[ref]$tokens,[ref]$errors); if($errors.Count){$errors | Out-String | Write-Error; exit 1}"
            checker = Path(temporary) / "check.ps1"
            checker.write_text(command, encoding="utf-8-sig")
            result = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(checker), str(path)], capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.name == "posix", "Native Bash/zsh syntax checks")
    def test_unix_shells_parse_every_documented_block(self):
        blocks = re.findall(r"```bash\n(.*?)\n```", GUIDES[1].source.read_text(encoding="utf-8"), re.S)
        with tempfile.TemporaryDirectory() as temporary:
            script = Path(temporary) / "walkthrough.sh"
            script.write_text("\n".join(blocks), encoding="utf-8", newline="\n")
            for shell in ("bash", "zsh"):
                if shutil.which(shell):
                    with self.subTest(shell=shell):
                        result = subprocess.run([shell, "-n", str(script)], capture_output=True, text=True, timeout=30)
                        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
