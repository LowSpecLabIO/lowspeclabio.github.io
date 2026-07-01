---
title: "5 VS Code Extensions That Actually Speed Up Python Development"
date: "2026-07-01"
category: "Coding IDEs"
---

Most "must-have VS Code extension" lists are popularity contests — they recommend Pylance, GitLens, and five themes you'll try once. Here are five extensions that genuinely save time when you're writing Python, with specifics on what they do that the defaults don't.

## 1. Ruff

Not a linter. Not a formatter. Both, simultaneously, and 10-100x faster than the alternatives.

Ruff replaces flake8, isort, pyupgrade, and half a dozen other tools with a single Rust binary. It runs in under 10ms on most projects, which means it actually runs on save without you noticing the delay.

**Setup:** Install the "Ruff" extension (charliermarsh.ruff). That's it. It auto-detects your pyproject.toml ruff config, handles linting and formatting, and shows inline warnings.

**What it replaces:** Flake8, isort, Black, pylint (for style rules), pyupgrade, pydocstyle.

**Why the defaults aren't enough:** Pylance catches type errors but doesn't enforce style. The built-in Python extension uses slower tools. Ruff gives you instant feedback on both.

## 2. Python Test Explorer

The built-in test runner works. The Test Explorer makes it visual.

See a tree of all your tests, run individual tests or suites with one click, see failures inline with diffs. If you write tests (you should), this removes the friction between "write test" and "run test."

**Setup:** Install "Python Test Explorer" (littlefoxteam.vscode-python-test-adapter). Works with pytest and unittest out of the box.

## 3. Error Lens

VS Code shows diagnostics as squiggly underlines with details on hover. Error Lens inlines the error message directly next to the line that has it.

This sounds trivial. It isn't. When you're iterating fast, the difference between "see error → hover → read popup → fix" and "see error right next to the code → fix" adds up to real time savings over a day.

No config needed. Install it, it works.

## 4. Even Better TOML

If your project uses pyproject.toml (it should in 2026 — setup.py is legacy), you need syntax highlighting and validation for TOML files. This extension provides both, plus auto-completion for known pyproject.toml keys.

It also catches TOML syntax errors before you waste a `pip install` cycle wondering why your config isn't being picked up.

## 5. Shellcheck

Not Python-specific, but if you're writing shell scripts for deployment, Docker entrypoints, or CI pipelines (and you are), Shellcheck catches bugs that would silently fail at runtime:

- Unquoted variables that break on paths with spaces
- `[[ ]]` vs `[ ]` confusion
- Common command argument mistakes

Install it, enable it, and stop shipping shell scripts with latent bugs.

## What Not to Install

Skip these — they slow down VS Code or add noise:

- **GitLens (full install)**: The free tier's useful features are now in the paid tier. The remaining free features aren't worth the extension load time. Use VS Code's built-in Git view instead.
- **Auto-import on every extension**: Pick one (Ruff handles this) and disable it in everything else. Multiple import sources fighting each other creates chaos.
- **AI completion extensions you're not actively using**: Every AI extension you have enabled is parsing your code on every keystroke for context. If you're not using it, disable it. Your CPU will thank you.

Five extensions, not twenty. Less is faster.
