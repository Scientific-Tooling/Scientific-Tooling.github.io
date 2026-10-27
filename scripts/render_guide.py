"""Render the quick start and compatibility pages; --check rejects stale files."""

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
DESCRIPTION = "Read papers under one research question, collect selected evidence, and create a project brief with links to the original passages."
MANUAL_URL = "https://github.com/Scientific-Tooling/structured-intelligence/blob/main/workflows/research/manual-operations/"
LEGACY_PAGES = {
    "rks-apw": ("README.md", "Advanced manual operations"),
    "rks-apw-windows": ("windows.md", "Advanced manual operations: Windows / PowerShell"),
    "rks-apw-linux-macos": ("unix.md", "Advanced manual operations: Linux / macOS"),
}


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
    Guide("paper-to-brief", "Quick start", "text", "Command", "Windows · Linux · macOS"),
)


def document(title: str, description: str, url: str, body: str, header_links: str, *, article: bool, legacy: bool = False) -> str:
    script = '  <script src="../guide.js" defer></script>' if article else ""
    kind = "article" if article else "website"
    robots = '  <meta name="robots" content="noindex, follow" />' if legacy else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description, quote=True)}" />
  <meta name="theme-color" content="#ffffff" />
  <meta name="color-scheme" content="light only" />
  <link rel="canonical" href="{url}" />
{robots}
  <link rel="icon" href="../../logo.svg" type="image/svg+xml" />
  <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin />
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
  <a class="skip-link" href="#walkthrough">Skip to content</a>
  <div class="page-shell">
    <header class="guide-header">
      <nav class="topbar" aria-label="Primary">
        <a class="brand" href="../../"><img src="../../logo.svg" alt="" width="40" height="40" /><span>Scientific Tooling</span></a>
        <div class="topbar-links"><a href="../../#workflows">Explore</a>{header_links}</div>
      </nav>
    </header>
    {body}
    <p class="copy-status" role="status" aria-live="polite"></p>
    <footer class="footer"><p><a href="../../">Scientific Tooling</a></p><p>Built for curious minds. Open to everyone.</p></footer>
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
    # Keep the source heading IDs and command text intact while adding visual steps.
    content = re.sub(r'(<h2 id="[^"]+">)([1-3])\. (.*?)</h2>',
                     r'\1<span class="step-number">\2</span> \3</h2>', content)
    overview = '<nav class="guide-overview" aria-label="Workflow overview">' + "".join(
        f'<a href="#{escape(step["id"], quote=True)}"><span aria-hidden="true">0{number}</span>{label}</a>'
        for number, (step, label) in enumerate(zip(converter.toc_tokens, ("Install once", "Open a PDF", "Keep evidence")), 1)
    ) + '</nav>\n'
    content = content.replace('<h2 ', overview + '<h2 ', 1)
    fingerprint = hashlib.sha256(source.encode("utf-8")).hexdigest()
    body = f'''<!-- Generated from guides/{guide.slug}.md. SHA-256: {fingerprint} -->
    <main class="guide-layout" id="walkthrough">
      <aside class="guide-sidebar">
        <p class="eyebrow">Quick start</p>
        <nav aria-label="Quick start steps">{converter.toc}</nav>
        <div class="guide-summary"><strong>One PDF. One evidence trail.</strong><p>Open your paper, keep the passages that matter, and return to the source from your brief.</p><span class="guide-badge">{escape(guide.badge)}</span></div>
      </aside>
      <article class="guide-content">
        <p class="eyebrow">PDF to brief · Quick start</p>
        <details class="mobile-toc"><summary>On this page</summary><nav aria-label="Mobile quick start steps">{converter.toc}</nav></details>
        {content}
      </article>
    </main>'''
    header = f'<a href="../{guide.slug}.md">Markdown source</a><button type="button" class="print-button">Print guide</button>'
    return document("Paper to brief: quick start | Scientific Tooling",
                    DESCRIPTION, guide.url, body, header, article=True)


def legacy_markdown(slug: str) -> str:
    filename, label = LEGACY_PAGES[slug]
    return f'''# Looking for the walkthrough?

Start with the [PDF-to-brief quick start]({GUIDES[0].url}). The same `sci`
commands work on Windows, Linux and macOS.

For debugging or developing integrations, the individual tool commands are in
[{label}]({MANUAL_URL}{filename}).
'''


def render_legacy(slug: str) -> str:
    filename, label = LEGACY_PAGES[slug]
    body = f'''<main class="guide-landing" id="walkthrough">
      <p class="eyebrow">PDF to brief</p>
      <h1>Looking for the walkthrough?</h1>
      <p class="lede">The quick start handles setup, reading and evidence import with the same commands on Windows, Linux and macOS.</p>
      <p><a class="button button-primary" href="../paper-to-brief/">Open the quick start →</a></p>
      <p class="manual-reference">For debugging or developing integrations, see <a href="{MANUAL_URL}{filename}">{escape(label)}</a>.</p>
    </main>'''
    return document("Find the PDF-to-brief quick start | Scientific Tooling", DESCRIPTION,
                    GUIDES[0].url, body, '<a href="../paper-to-brief/">Quick start</a>', article=False, legacy=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    pages = [(guide.output, render(guide)) for guide in GUIDES]
    for slug in LEGACY_PAGES:
        pages.append((ROOT / "guides" / slug / "index.html", render_legacy(slug)))
        if slug != "rks-apw":
            pages.append((ROOT / "guides" / f"{slug}.md", legacy_markdown(slug)))
    for output, expected in pages:
        if args.check:
            if not output.exists() or output.read_text(encoding="utf-8") != expected:
                parser.exit(1, f"Stale page: {output.relative_to(ROOT)}. Run python scripts/render_guide.py\n")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(expected, encoding="utf-8", newline="\n")
            print(output.relative_to(ROOT))
    if args.check:
        print("The quick start and compatibility pages match their sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
