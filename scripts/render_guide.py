"""Render the checked-in Markdown walkthrough; --check rejects stale HTML."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "guides/rks-apw-windows.md"
OUTPUT = ROOT / "guides/rks-apw-windows/index.html"
URL = "https://scientifictooling.org/guides/rks-apw-windows/"
TITLE = "RKS + PDF Workbench: Windows walkthrough | Scientific Tooling"
DESCRIPTION = "Read and annotate a PDF, import selected evidence into RKS, and create a brief with links to the original passage. A concise PowerShell walkthrough."


def render() -> str:
    source = SOURCE.read_text(encoding="utf-8")
    converter = markdown.Markdown(extensions=["fenced_code", "tables", "toc"],
                                  extension_configs={"toc": {"toc_depth": "2-2"}})
    content = converter.convert(source)
    block_number = 0

    def code_block(match: re.Match) -> str:
        nonlocal block_number
        block_number += 1
        return (
            '<div class="code-block"><div class="code-toolbar"><span>PowerShell</span>'
            f'<button type="button" class="copy-button" aria-label="Copy PowerShell block {block_number}">Copy</button>'
            f'</div><pre tabindex="0" aria-label="PowerShell block {block_number}"><code class="language-powershell">'
            f'{match.group(1)}</code></pre></div>'
        )

    content = re.sub(r'<pre><code class="language-powershell">(.*?)</code></pre>', code_block, content, flags=re.S)
    fingerprint = hashlib.sha256(source.encode("utf-8")).hexdigest()
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{TITLE}</title>
  <meta name="description" content="{DESCRIPTION}" />
  <meta name="theme-color" content="#2563eb" />
  <meta name="color-scheme" content="light only" />
  <link rel="canonical" href="{URL}" />
  <link rel="icon" href="../../logo.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="../../theme.css" />
  <link rel="stylesheet" href="../../site.css" />
  <link rel="stylesheet" href="../guide.css" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{TITLE}" />
  <meta property="og:description" content="{DESCRIPTION}" />
  <meta property="og:url" content="{URL}" />
  <meta property="og:image" content="https://scientifictooling.org/social-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <script src="../guide.js" defer></script>
</head>
<body class="guide-page">
  <!-- Generated from guides/rks-apw-windows.md. SHA-256: {fingerprint} -->
  <a class="skip-link" href="#walkthrough">Skip to walkthrough</a>
  <div class="page-shell">
    <header class="guide-header">
      <nav class="topbar" aria-label="Primary">
        <a class="brand" href="../../"><img src="../../logo.svg" alt="" width="40" height="40" /><span>Scientific Tooling</span></a>
        <div class="topbar-links"><a href="../../#projects">Projects</a><a href="../rks-apw-windows.md">Markdown source</a><button type="button" class="print-button">Print guide</button></div>
      </nav>
    </header>
    <main class="guide-layout" id="walkthrough">
      <aside class="guide-sidebar">
        <p class="eyebrow">In this walkthrough</p>
        <nav aria-label="Walkthrough steps">{converter.toc}</nav>
        <div class="guide-summary"><strong>One PDF. One evidence trail.</strong><p>Read in APW, keep selected evidence in RKS, and return to the original passage from your brief.</p><span class="guide-badge">Windows · PowerShell</span></div>
      </aside>
      <article class="guide-content">
        <p class="eyebrow">RKS + Agent PDF Workbench</p>
        <details class="mobile-toc"><summary>On this page</summary><nav aria-label="Mobile walkthrough steps">{converter.toc}</nav></details>
        {content}
      </article>
    </main>
    <p class="copy-status" role="status" aria-live="polite"></p>
    <footer class="footer"><p><a href="../../">Scientific Tooling</a></p><p>Keep the source. Make the next step clear.</p></footer>
  </div>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            parser.exit(1, "Guide HTML is stale. Run python scripts/render_guide.py\n")
        print("Guide HTML matches its Markdown source.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
        print(OUTPUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
