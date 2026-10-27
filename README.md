# Scientific Tooling

Organization homepage for https://scientifictooling.org/.

This repository holds the public-facing Scientific Tooling landing page, shared
brand assets, and domain-level Pages metadata. Project implementation details
and manuscript web pages live in project repositories such as
Scientific-Tooling/structured-intelligence.

`theme.css` is the source of truth for shared page typography tokens and hero
title classes. Downstream project repositories should sync this file instead of
copy-editing page-title styles independently.

The site uses locally served Manrope, with bundled Source Serif 4 retained for
downstream compatibility. Their licenses are under `assets/fonts/`.
Shared colors, spacing, navigation and
responsive layouts live in `site.css`; reading-specific styles live in
`guides/guide.css`. The homepage leads with research tasks and a progressively
enhanced three-stage paper-to-brief example. The example is illustrative, with an attributed,
page-checked excerpt and an explicitly unreviewed interpretation; its downloadable
brief is in `examples/single-cell-brief.md`.
The guide's current-section indicator enhances ordinary anchor navigation.
Fonts, layout, navigation and content remain usable without JavaScript or
external font services; print and reduced-motion preferences are respected.

## PDF-to-brief quick start

The [quick start](guides/paper-to-brief.md) is the single onboarding guide for
Windows, Linux and macOS. Homepage navigation, the main action and the paper
workflow link directly to it. The CLI handles setup and the reader;
the bundled agent skill can coordinate the same workflow.

Detailed individual-tool instructions and their native shell/workflow tests live
in Structured Intelligence's
[advanced manual operations](https://github.com/Scientific-Tooling/structured-intelligence/blob/main/workflows/research/manual-operations/README.md).
The previous `/guides/rks-apw/`, `/guides/rks-apw-windows/` and
`/guides/rks-apw-linux-macos/` URLs remain as lightweight landing pages with a
quick-start link and the appropriate advanced reference. Old Markdown URLs also
remain available. The legacy pages point their canonical metadata at the quick
start and are excluded from the sitemap.

Use Python 3.14 for the documentation build (`.python-version`); CI also checks
3.12 and 3.15. Edit `guides/paper-to-brief.md`, then regenerate:

```text
python -m pip install -r requirements-docs.txt
python scripts/render_guide.py
python -m unittest discover -s tests -v
```

The renderer owns the generated HTML and the two legacy Markdown stubs.
`python scripts/render_guide.py --check` rejects stale output. Site checks cover
command copy fidelity, direct homepage discovery, legacy destinations,
site-owned links/assets/anchors and canonical sitemap entries. Pages deploys on
push to `main` after these checks pass. Copy/print controls are progressive
enhancements; the content and navigation work without JavaScript.

Structured Intelligence CI retains the native PowerShell/Bash/zsh syntax checks
and the manual CLI/HTTP workflow on Ubuntu Bash and macOS Bash/zsh, alongside
its installed `sci` and real browser workflow tests. These engineering checks do
not establish scientific answer accuracy or independent expert review.
