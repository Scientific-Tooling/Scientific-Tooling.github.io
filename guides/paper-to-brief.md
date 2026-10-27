# One paper. One question. A source-linked brief.

Open a PDF, choose the passages worth keeping, and download a brief that links
back to the source. Scientific Tooling handles the workspace and reader setup.
The same commands work on Windows, Linux and macOS.

## 1. Install once

You need Git and Python 3.10–3.12 with pip in your chosen Python environment.
Your agent can do this setup for you. Install the workflow package:

```text
python -m pip install --upgrade "git+https://github.com/Scientific-Tooling/structured-intelligence.git"
```

Use `python3` if that is your interpreter's name. The installation includes
compatible RKS and APW versions and the built PDF reader. No Node.js, model API
key or MCP connection is needed. This is a Git source installation; no new PyPI
release is required. If your system Python disallows package installation, use
a virtual environment rather than overriding its protection.

The short command is **`sci`** (version 0.1.1 or later). The original
`scientific-tooling` command also works. The installation command above upgrades
an existing installation while preserving your saved workspaces.

## 2. Open your paper

Replace the PDF path and question with your own:

```text
sci start "paper.pdf" --question "What evidence addresses my question?" --workspace "my-review"
```

The reader opens automatically. **One workspace holds one paper and question.**
The command creates the workspace, preserves the PDF revision, and starts the
reader. You do not need a second terminal or any paper/session IDs.

If your environment does not put the command on PATH, use
`python -m scientific_tooling` instead of `sci`.

## 3. Keep evidence and get your brief

1. Highlight a passage in the PDF; add a comment if useful.
2. In **Evidence & brief**, check the highlights or notes you want to keep.
3. Click **Preview selected evidence** and inspect the quotes and comments.
4. Click **Import evidence & create brief**, then **Download brief**.

The brief includes original quotes, page references and links back to the
highlighted passages. Importing an observation preserves its review status;
it does not establish scientific agreement or human review.

## Prefer to ask your agent?

Install the bundled skill into your agent's skills directory. For example:

```text
sci skill --dest "~/.codex/skills"
```

Use `~/.claude/skills` for a host using that directory, or provide its actual
skills directory. Reload skills in your agent, then ask:

> Use paper-to-brief to read this PDF and collect evidence relevant to my question.

The agent reads the source with its available tools, proposes passages, and
coordinates the same workflow. You can inspect its selections in the PDF reader.
Agent-created interpretations stay unreviewed. The CLI itself makes no model
calls; your agent host supplies the reasoning and governs any model data sharing.

## Stop and continue later

```text
sci stop --workspace "my-review"
sci resume --workspace "my-review"
```

Resume restores the saved workspace and reader. Passage links work while the
reader is running. Repeating an import does not duplicate its evidence. If a
selection changes after preview, the workflow asks for a fresh preview.

For installation diagnostics, run `sci doctor`. For saved progress,
run `sci status --workspace "my-review"`. Back up the entire
workspace after stopping all writers; restore it at the same absolute location
in this first version.

See the [CLI and recovery reference](https://github.com/Scientific-Tooling/structured-intelligence/blob/main/workflows/research/quickstart.md)
for agent JSON output, revision updates and SSH usage. For debugging or developing
integrations, see [advanced manual operations](https://github.com/Scientific-Tooling/structured-intelligence/blob/main/workflows/research/manual-operations/README.md).
