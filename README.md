# Scientific Tooling

Organization homepage for https://scientifictooling.org/.

This repository holds the public-facing Scientific Tooling landing page, shared
brand assets, and domain-level Pages metadata. Project implementation details
and manuscript web pages live in project repositories such as
Scientific-Tooling/structured-intelligence.

`theme.css` is the source of truth for shared page typography tokens and hero
title classes. Downstream project repositories should sync this file instead of
copy-editing page-title styles independently.

## RKS + APW walkthroughs

Start with the [guided PDF-to-brief workflow](guides/paper-to-brief.md), which uses
one installable CLI, an optional agent skill and the reader's evidence controls.
The [walkthrough start page](guides/rks-apw/index.html) recommends this path.
For the individual tools, read the
[Windows/PowerShell source](guides/rks-apw-windows.md) and
[Linux/macOS Bash/zsh source](guides/rks-apw-linux-macos.md). Both cover source
installation, reading one PDF, selected evidence preview/import, a source-linked
brief, and safe replay/backup. The homepage navigation and main action link to
the chooser; RKS/APW project cards link directly to both platform versions.

The Markdown is the source of truth. After editing it:

```powershell
python -m pip install -r requirements-docs.txt
python scripts/render_guide.py
python -m unittest discover -s tests -v
```

`python scripts/render_guide.py --check` rejects stale generated HTML for all
three guides and the start page. CI checks command fidelity, site-owned links/assets/anchors,
sitemap discovery and native PowerShell/Bash/zsh syntax. The pages share `theme.css` and `site.css`,
with guide-only styles and optional copy/print controls. No server-side runtime
is needed. GitHub Pages deploys the generated HTML on a push to `main` after
validation and the native Unix walkthrough jobs succeed.

The Unix job executes all documented shell blocks in fresh public HTTPS clones
and a new Python environment on Ubuntu Bash and macOS Bash/zsh. It supplies the
manual highlight as an unreviewed fixture through APW's HTTP API, then checks the
real preview/import, generated citation, replay counts and viewer shutdown. It
does not automate the browser UI. To reproduce on Linux/macOS, with Python 3.10–3.12
and venv available:

```bash
python3 tests/verify_unix_walkthrough.py --shell bash
# Or, where zsh is installed:
python3 tests/verify_unix_walkthrough.py --shell zsh
```

Logs and receipts remain under ignored `.preview/unix-*/` directories. CI retains
only the logs, receipt and generated shell script on failure, not installed
environments or cloned repositories.

The required RKS/APW/Structured Intelligence source commits must be available
publicly before publishing the guides. The guided package pins its RKS/APW Git
dependencies; its native installed-wheel and browser journey tests live in
Structured Intelligence, including interrupted ingestion/import and viewer resume.

Initial Windows-guide verification on October 27, 2026 covered fresh source clones and Python
3.12 environments in Windows PowerShell 5.1 and PowerShell 7, including paths
containing spaces and Unicode. A generated PDF fixture was highlighted through
the real viewer; preview/import/brief generation and passage navigation passed,
and replay returned one unchanged item with no additions. These runs used local
clones of the required feature commits, not the older public branches.

Desktop (1440 px) and mobile (390 px) Chromium checks covered homepage discovery,
navigation, copied command text, fragment links, overflow and print styles.
The current six site checks pass on Windows and Ubuntu, with the other platform's
native syntax check skipped on each. Native Unix jobs additionally run the
documented CLI/HTTP workflow on Ubuntu Bash and macOS Bash/zsh. These engineering checks
do not establish scientific answer accuracy or independent expert review.
