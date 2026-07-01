---
title: "5 VS Code Extensions That Actually Speed Up Python Development"
date: "2026-07-01"
category: "Coding IDEs"
---

Most "must-have VS Code extension" lists are popularity contests — they recommend Pylance, GitLens, and five themes you'll try once. Here are five extensions that genuinely save time when you're writing Python, with specifics on what they do that the defaults don't.

## 1. Ruff

Not a linter. Not a formatter. Both, simultaneously, and 10–100x faster than the alternatives.

Ruff replaces flake8, isort, pyupgrade, pydocstyle, and pylint (for style rules) with a single Rust binary. It runs in under 10ms on most projects where flake8 takes 200–2000ms. The difference is noticeable: save a file and the diagnostics appear instantly, not after a perceptible delay.

**Setup:** Install the "Ruff" extension (publisher: charliermarsh). It auto-detects `pyproject.toml` or `ruff.toml` in your project root. That's all — no extra config needed for basic use.

**What it replaces:**

| Tool | What Ruff covers |
|------|-----------------|
| flake8 | All rules, 10–100x faster |
| isort | Import sorting |
| Black | Formatting (via `ruff format`) |
| pyupgrade | Modern syntax adoption |
| pydocstyle | Docstring style |
| pylint | Subset of rules (style only) |

**Real pyproject.toml setup:**

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4", "SIM"]
ignore = ["E501"]  # line-too-long handled by formatter

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

The `E501` ignore is critical — Ruff's formatter handles line length, so the linter doesn't need to duplicate that check. Run `ruff format` instead of `black` in your pre-commit or CI.

**The one gotcha:** Ruff doesn't do type checking. Pylance is still worth keeping for its semantic analysis (unused imports, type errors, autocomplete quality). Ruff and Pylance complement each other — Ruff catches style issues at machine speed, Pylance catches actual bugs.

## 2. Python Test Explorer

The built-in test runner works. The Test Explorer makes it visual and removes friction.

Without it: you open the terminal, type `pytest tests/test_foo.py::test_bar -v`, interpret the output, switch back to the editor. With it: you see a tree of all tests, click one, it runs, the failure appears inline with a diff. The friction between "write test" and "run test" is the difference between running tests once a day and running them ten times a day.

**Extension ID:** `littlefoxteam.vscode-python-test-adapter`

**Setup:** Install it. It auto-discovers pytest, unittest, and pytest-bdd test suites. Open the Testing sidebar (icon on the left) and you'll see your tests grouped by file.

**Real workflow:**
1. Write a failing test: `def test_bar_returns_baz_when_given_qux():`
2. Click the run button next to the test name in the Testing sidebar
3. See the failure with a real diff: `assert actual == expected` with actual highlighted red
4. Fix the code, click the run button again (or set it to auto-run on save)
5. Watch it turn green

**Auto-run on save config:**

```json
{
  "python-testing.pytestEnabled": true,
  "python-testing.unittestEnabled": false,
  "python-testing.pytestArgs": ["-v", "--tb=short"],
  "python-test-adapter.autoWatch": true
}
```

The `autoWatch` setting re-runs tests whenever a test file changes. Combine this with TDD and you'll catch regressions before you even switch to the browser.

## 3. Error Lens

VS Code shows diagnostics as squiggly underlines with details on hover. Error Lens inlines the error message directly next to the line that has it.

This sounds trivial. It isn't. The cognitive cost of switching context — read the code, notice the squiggle, hover, wait 200ms for the popup, read the popup, close it, return to the code — sounds small but compounds over hundreds of errors per day. With Error Lens, you see `Undefined name 'foo'` inlined at the end of the line the moment you type it. The fix happens in one glance, one motion.

**What it shows per severity level:**

- Error: red inline text with the full message
- Warning: yellow inline text
- Info: grey inline text
- Hint: grey inline text (for things like unused imports)

**Real configuration:**

```json
{
  "errorLens.enabled": true,
  "errorLens.addAnnotationText": false,
  "errorLens.fontStyle": "italic",
  "errorLens.messageBackgroundMode": "line",
  "errorLens.showUnnecessaryAnnotations": false
}
```

`showUnnecessaryAnnotations: false` is important — it'll hide the `unused import` annotations that you already have a fixer for (that's what Ruff's `I` rules do).

**The one situation where it backfires:** On large legacy codebases with hundreds of warnings, Error Lens can make the screen unreadable. It's a signal-to-noise problem — useful when you control the codebase and most warnings are fixable, noisy when you're reading someone else's mess.

## 4. Even Better TOML

If your project uses `pyproject.toml`, you need this. TOML is not intuitive — the difference between a table and an array of tables, between dotted keys and nested tables, between strings with and without escaping — and VS Code's built-in TOML support is bare syntax highlighting at best.

Even Better TOML gives you:

- **Syntax validation**: it catches the `foo = "bar"` when you meant `foo = "bar"` inside a table, which will silently fail in ways that waste an hour of debugging a tool that claims it can't find your config
- **Schema-aware completion**: `pyproject.toml` has a [standard schema](https://toml.io/en/schema). It will autocomplete `tool.ruff.lint.select` and validate that the values are actual Ruff rule codes, not typos
- **Hover docs**: hover over `line-length` in a Ruff config and see the documentation

**Extension ID:** `bungcip.better-toml`

**Real example of what it catches:**

```toml
[tool.ruff.lint
# Missing ] — this is a syntax error, will silently be ignored
select = ["E", "F", "W"]
```

VS Code won't tell you that's broken. Even Better TOML underlines it red on save.

**Setup:** Install it. That's it. It activates automatically for any `.toml` file. No configuration needed.

## 5. Shellcheck

Not Python-specific, but if you're writing shell scripts for deployment, Docker entrypoints, or CI pipelines — and you are, even if you think you're not — Shellcheck catches bugs that would silently fail at runtime.

**Three real bugs it catches:**

**Bug 1: unquoted variables**

```bash
#!/bin/bash
file="My Document.txt"
rm $file   # breaks on spaces — tries to remove "My" and "Document.txt"
rm "$file" # correct
```

Shellcheck warns: `SC2086: Double quote to prevent globbing.`

**Bug 2: `[[ ]]` vs `[ ]`**

```bash
#!/bin/bash
if [ -z "$VAR" ]; then   # works for strings, breaks on empty unquoted vars
    echo "empty"
fi
if [[ -z $VAR ]]; then   # correct for this use case
    echo "empty"
fi
```

Shellcheck warns: `SC2236: Don't use -n to test if parameter is set. Use [-n "$var"] or [[ -n $var ]].`

**Bug 3: failing silently in pipes**

```bash
#!/bin/bash
cat huge_log_file.txt | grep "ERROR" | head -5
```

If `grep` finds nothing, this exits 1 silently. Shellcheck warns: `SC2181: Check exit code directly with e.g. 'if mycmd;', not indirectly with $?.`

**Setup:** Install the "Shellcheck" extension (publisher: mads-hartmann). It requires Shellcheck to be installed on your system:

```bash
# Ubuntu/Debian
sudo apt install shellcheck

# macOS
brew install shellcheck

# CachyOS/Arch
sudo pacman -S shellcheck
```

Shellcheck the extension also runs automatically on any `.sh` file you open.

## What NOT to Install

Skip these. They either cost money for what you need, add noise, or slow VS Code down without benefit.

**GitLens (full install):** The free tier had useful features (blame annotations, history in the gutter). As of 2025, those features moved to paid. The free tier shows you a "GitLens+ trial" popup every time you open a file. Use VS Code's built-in Source Control panel instead — it has everything most people actually need.

**Multiple AI completion extensions at once:** If you have Copilot, Continue.dev, and Codeium all running, they're all parsing your code on every keystroke. That adds real latency and CPU load. Pick one. If you're using Continue.dev with local Ollama for free completions, uninstall Copilot entirely.

**Auto-formatters you don't understand:** If Ruff handles formatting (`ruff format`), don't also have Black installed. They will fight. Ruff is 20x faster and produces output that's functionally identical.

**Theme packs that include 15 extensions:** You need syntax highlighting and a readable UI. A "100+ themes bundle" doesn't make you faster.

Five extensions, not twenty. Less is faster.