
# Contributing

## Linting

You can lint using `ruff check` (assuming you've activated the virtual environment; otherwise `.venv/bin/ruff check`). You can also use `ruff check --fix` to attempt to fix the issues.

### Lint on Save

If you want to automatically lint your Python files on save, you can install the `Run on Save` extension by `emeraldwalk` and add the following configuration to a file called `.vscode/settings.json` in the project directory:

```json
{
    "emeraldwalk.runonsave": {
        "commands": [
            {
                "match": ".*\\.py$",
                "cmd": "${workspaceFolder}/.venv/bin/ruff check --fix ${file}",
                "isAsync": true
            }
        ]
    }
}
```

### Pre-commit Hook

You can also do this as a pre-commit hook (so that a lint check happens when you commit rather than when you save the file). To do this, add the following to a file called `.git/hooks/pre-commit` in the project directory:

```bash
#!/bin/sh

.venv/bin/ruff check $(git diff --cached --name-only --diff-filter=d | grep '\.py$')
```

Then do `chmod +x .git/hooks/pre-commit` to make the file executable.

Then if you attempt to make a commit with a Python file that doesn't pass the linting checks, the commit will be rejected. You can then do `ruff check --fix` to attempt to fix the issues.