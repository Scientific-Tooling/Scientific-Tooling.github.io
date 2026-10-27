"""Render the Markdown walkthroughs and OS chooser; --check rejects stale HTML."""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from html import escape
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://scientifictooling.org/"
DESCRIPTION = "Read and annotate a PDF, import selected evidence into RKS, and create a brief with links to the original passage."
INDEX_OUTPUT = ROOT / "guides/rks-apw/index.html"
INDEX_URL = BASE_URL + "guides/rks-apw/"


@dataclass(frozen=True)
class Guide:
    slug: str
    name: str
    language: str
    code_label: str
    badge: str

    @property
    def source(self) -> Path:
        return ROOT / "guides" / f"{self.slug}.md"

    @property
    def output(self) -> Path:
        return ROOT / "guides" / self.slug / "index.html"

    @property
    def url(self) -> str:
        return BASE_URL + f"guides/{self.slug}/"


GUIDES = (
    Guide("rks-apw-windows", "Windows", "powershell", "PowerShell", "Windows · PowerShell"),
    Guide("rks-apw-linux-macos", "Linux / macOS", "bash", "Bash / zsh", "Linux / macOS · Bash / zsh"),
)


def document(title: str, description: str, url: str, body: str, header_links: str, *, article: bool) -> str:
    script = '<script src="../guide.js" defer></script>' if article else ""
    kind = "article" if article else "website"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description, quote=True)}" />
  <meta name="theme-color" content="#2563eb" />
  <meta name="color-scheme" content="light only" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="../../logo.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="../../theme.css" />
  <link rel="stylesheet" href="../../site.css" />
  <link rel="stylesheet" href="../guide.css" />
  <meta property="og:type" content="{kind}" />
  <meta property="og:title" content="{escape(title, quote=True)}" />
  <meta property="og:description" content="{escape(description, quote=True)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="https://scientifictooling.org/social-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  {script}
</head>
<body class="guide-page">
  <a class="skip-link" href="#walkthrough">Skip to walkthrough</a>
  <div class="page-shell">
    <header class="guide-header">
      <nav class="topbar" aria-label="Primary">
        <a class="brand" href="../../"><img src="../../logo.svg" alt="" width="40" height="40" /><span>Scientific Tooling</span></a>
        <div class="topbar-links"><a href="../../#projects">Projects</a>{header_links}</div>
      </nav>
    </header>
    {body}
    <p class="copy-status" role="status" aria-live="polite"></p>
    <footer class="footer"><p><a href="../../">Scientific Tooling</a></p><p>Keep the source. Make the next step clear.</p></footer>
  </div>
</body>
</html>
'''


def render(guide: Guide) -> str:
    source = guide.source.read_text(encoding="utf-8")
    converter = markdown.Markdown(extensions=["fenced_code", "tables", "toc"],
                                  extension_configs={"toc": {"toc_depth": "2-2"}})
    content = converter.convert(source)
    block_number = 0

    def code_block(match: re.Match) -> str:
        nonlocal block_number
        block_number += 1
        label = escape(guide.code_label)
        return (
            f'<div class="code-block"><div class="code-toolbar"><span>{label}</span>'
            f'<button type="button" class="copy-button" aria-label="Copy {label} block {block_number}">Copy</button>'
            f'</div><pre tabindex="0" aria-label="{label} block {block_number}"><code class="language-{guide.language}">'
            f'{match.group(1)}</code></pre></div>'
        )

    content = re.sub(fr'<pre><code class="language-{re.escape(guide.language)}">(.*?)</code></pre>', code_block, content, flags=re.S)
    fingerprint = hashlib.sha256(source.encode("utf-8")).hexdigest()
    tabs = "".join(
        f'<a href="../{option.slug}/"' + (' aria-current="page"' if option == guide else '') + f'>{escape(option.name)}</a>'
        for option in GUIDES
    )
    body = f'''<!-- Generated from guides/{guide.slug}.md. SHA-256: {fingerprint} -->
    <main class="guide-layout" id="walkthrough">
      <aside class="guide-sidebar">
        <p class="eyebrow">In this walkthrough</p>
        <nav aria-label="Walkthrough steps">{converter.toc}</nav>
        <div class="guide-summary"><strong>One PDF. One evidence trail.</strong><p>Read in APW, keep selected evidence in RKS, and return to the original passage from your brief.</p><span class="guide-badge">{escape(guide.badge)}</span></div>
      </aside>
      <article class="guide-content">
        <nav class="platform-switch" aria-label="Operating system">{tabs}</nav>
        <p class="eyebrow">RKS + Agent PDF Workbench</p>
        <details class="mobile-toc"><summary>On this page</summary><nav aria-label="Mobile walkthrough steps">{converter.toc}</nav></details>
        {content}
      </article>
    </main>'''
    header = f'<a href="../{guide.slug}.md">Markdown source</a><button type="button" class="print-button">Print guide</button>'
    return document(f"RKS + PDF Workbench: {guide.name} walkthrough | Scientific Tooling",
                    DESCRIPTION + f" A concise {guide.code_label} walkthrough.", guide.url, body, header, article=True)


def render_index() -> str:
    cards = "".join(
        f'<a class="platform-card" href="../{guide.slug}/"><span class="eyebrow">{escape(guide.code_label)}</span>'
        f'<h2>{escape(guide.name)}</h2><p>Install, read, highlight, import selected evidence, and generate a source-linked brief.</p>'
        '<span>Open walkthrough →</span></a>' for guide in GUIDES
    )
    body = f'''<main class="guide-chooser" id="walkthrough">
      <p class="eyebrow">RKS + Agent PDF Workbench</p>
      <h1>Choose your walkthrough.</h1>
      <p class="lede">Take one paper PDF from reading and annotation to a brief that opens the original supporting passage. Choose the commands for your operating system.</p>
      <div class="platform-cards">{cards}</div>
      <p class="chooser-note">Both guides use local source checkouts and an isolated Python environment. No API key or MCP setup is required for this path.</p>
    </main>'''
    return document("RKS + PDF Workbench walkthroughs | Scientific Tooling", DESCRIPTION,
                    INDEX_URL, body, '<a href="https://github.com/Scientific-Tooling">GitHub</a>', article=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    pages = [(guide.output, render(guide)) for guide in GUIDES] + [(INDEX_OUTPUT, render_index())]
    for output, expected in pages:
        if args.check:
            if not output.exists() or output.read_text(encoding="utf-8") != expected:
                parser.exit(1, f"Stale page: {output.relative_to(ROOT)}. Run python scripts/render_guide.py\n")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(expected, encoding="utf-8", newline="\n")
            print(output.relative_to(ROOT))
    if args.check:
        print("Both walkthroughs and the OS chooser match their sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
