# Your papers. One question. A source-linked brief.

Open a PDF, choose the passages worth keeping, and download a brief that links
back to the source. Scientific Tooling handles the workspace and reader setup.
The same commands work on Windows, Linux and macOS.

## 1. Install once

You need Git and Python 3.12 or newer with pip. **Python 3.14 is recommended**
for new environments.
Your agent can do this setup for you. Install the workflow package:

```text
python -m pip install --upgrade "git+https://github.com/Scientific-Tooling/structured-intelligence.git"
```

Use `python3` if that is your interpreter's name. The installation includes
compatible RKS and APW versions and the built PDF reader. No Node.js, model API
key or MCP connection is needed. This is a Git source installation; no new PyPI
release is required. If your system Python disallows package installation, use
a virtual environment rather than overriding its protection.

The short command is **`sci`** (version 0.3.1 or later for the reader shown here). The original
`scientific-tooling` command also works. The installation command above upgrades
an existing installation while preserving your saved workspaces. If you are
moving from Python 3.10 or 3.11, follow the
[Python upgrade steps](https://github.com/Scientific-Tooling/structured-intelligence/blob/main/workflows/research/quickstart.md#upgrading-from-python-310-or-311)
to continue with your saved workspace.

## 2. Open your paper

Replace the PDF path and question with your own:

```text
sci start "paper.pdf" --question "What evidence addresses my question?" --workspace "my-review"
```

The reader opens automatically. **A project holds your papers and one question.**
The command creates the workspace, preserves the PDF revision, and starts the
reader. You do not need a second terminal or any paper/session IDs.

If your environment does not put the command on PATH, use
`python -m scientific_tooling` instead of `sci`.

## 3. Keep evidence and get your brief

1. Highlight a passage in the PDF; add a comment if useful.
2. In the **Evidence** tab, check the highlights or saved notes you want to keep.
3. Click **Preview selected evidence** and inspect the quotes and comments.
4. Click **Import evidence & create brief**. Open **Brief**, then **Download brief**.

Use **Notes** to connect your thoughts to supporting highlights. Resize the
sidebars or choose **Focus on paper** for more reading space. On a phone, use
the Papers and Workspace buttons to open one panel at a time.

The brief includes original quotes, page references and links back to the
highlighted passages. Importing an observation preserves its review status;
it does not establish scientific agreement or human review.

## Bring several papers together

Start with several PDFs, or add one to your existing project:

```text
sci start "paper-a.pdf" "paper-b.pdf" --question "Which methods fit my dataset?" --workspace "methods"
sci add "paper-c.pdf" --workspace "methods"
```

Switch between them under **Project papers** in the reader. Use **Refresh project**
after adding papers. Each paper keeps its own highlights and progress. The shared
brief groups evidence by paper, preserves source links, and shows which papers
still lack imported evidence. Identical PDFs are reused automatically.

To open a particular paper or create the combined brief from the terminal:

```text
sci papers --workspace "methods"
sci open p2 --workspace "methods"
sci brief --workspace "methods"
```

The brief provides material for comparison; it does not invent a scientific
conclusion. Your agent can propose a synthesis from the source-linked evidence.

## Prefer to ask your agent?

Install the bundled skill into your agent's skills directory. For example:

```text
sci skill --dest "~/.codex/skills"
```

Use `~/.claude/skills` for a host using that directory, or provide its actual
skills directory. Reload skills in your agent, then ask:

> Use paper-to-brief to read these PDFs and collect evidence relevant to my question.

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
when restoring. Before upgrading, stop any active reader with the old installation.
Existing single-paper workspaces continue to work; the upgrade preserves their
sessions, evidence and links, and saves the original workspace manifest.

See the [CLI and recovery reference](https://github.com/Scientific-Tooling/structured-intelligence/blob/main/workflows/research/quickstart.md)
for agent JSON output, revision updates and SSH usage. For debugging or developing
integrations, see [advanced manual operations](https://github.com/Scientific-Tooling/structured-intelligence/blob/main/workflows/research/manual-operations/README.md).
