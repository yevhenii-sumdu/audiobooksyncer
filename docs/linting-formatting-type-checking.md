# Which linter

This project uses ruff, which is an extremely fast Python linter and code formatter, written in Rust.

Ruff is designed to replace Flake8 (plus dozens of plugins), Black, isort, pydocstyle, pyupgrade, autoflake, and more, all while executing tens or hundreds of times faster than any individual tool.

Execution speed and versatility is why I chose this tool for my project.

# Settings

This tool has very good default settings and the only option that I decided to change is quote style, which I set to single quotes.

# How to use it

You can use it from the terminal by installing the `ruff` package using pip.

To simply check for linting errors run `ruff check` and to fix any fixable errors run `ruff check --fix`.

To check for formatting errors run `ruff format --check` and to actually format the files run `ruff format`.

There is also a VS Code extension called `Ruff`, you can configure it to format, fix, and organize imports on-save via the following `settings.json`:

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

# Git hooks

There is a pre-commit hook for ruff configured in `.pre-commit-config.yaml`. This hook checks for linting and formatting issues.

To use hooks:

```bash
pip install pre-commit  # install
pre-commit install  # set up hooks
```

# Static type checking

I use MyPy for static type checking. To run the check use `mypy .`.

# GitHub Actions

To automatically run all the checks I've added a GitHub Actions workflow.
