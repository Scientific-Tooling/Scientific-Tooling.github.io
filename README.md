# Scientific Tooling

Organization homepage for https://scientifictooling.org/.

This repository holds the public-facing Scientific Tooling landing page, shared
brand assets, and domain-level Pages metadata. Project implementation details
and manuscript web pages live in project repositories such as
Scientific-Tooling/structured-intelligence.

`theme.css` is the source of truth for shared page typography tokens and hero
title classes. Downstream project repositories should sync this file instead of
copy-editing page-title styles independently.

## RKS + APW walkthrough

The [Windows/PowerShell walkthrough](guides/rks-apw-windows.md) covers source
installation, reading one PDF, selecting an annotation, previewing/applying its
RKS import, and generating a brief with a verified passage link. Its dedicated
page is [guides/rks-apw-windows/index.html](guides/rks-apw-windows/index.html),
linked from the homepage navigation, main action and RKS/APW project cards.

The Markdown is the source of truth. After editing it:

```powershell
python -m pip install -r requirements-docs.txt
python scripts/render_guide.py
python -m unittest discover -s tests -v
```

`python scripts/render_guide.py --check` rejects stale generated HTML. CI checks
command fidelity, site-owned links/assets/anchors, sitemap discovery and, on
Windows, PowerShell syntax. The page uses the shared `theme.css` and `site.css`,
with guide-only styles and optional copy/print controls. No server-side runtime
is needed. GitHub Pages deploys the generated HTML on a push to `main`.

The required RKS/APW/Structured Intelligence source commits must be available
publicly before publishing this guide; its three clone commands depend on them.

Local verification on October 27, 2026 covered fresh source clones and Python
3.12 environments in Windows PowerShell 5.1 and PowerShell 7, including paths
containing spaces and Unicode. A generated PDF fixture was highlighted through
the real viewer; preview/import/brief generation and passage navigation passed,
and replay returned one unchanged item with no additions. These runs used local
clones of the required feature commits, not the older public branches.

Desktop (1440 px) and mobile (390 px) Chromium checks covered homepage discovery,
navigation, copied command text, fragment links, overflow and print styles.
Five site checks passed on Windows; four passed on Ubuntu Python 3.10 with the
Windows-only PowerShell syntax check skipped there. These engineering checks
do not establish scientific answer accuracy or independent expert review.
