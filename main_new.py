#!/usr/bin/env python3
"""
CookCommit - CLI tool for AI-powered commit and PR message generation.
"""

import typer
from src.cookcommit.commands.save import save_command
from src.cookcommit.commands.commit import generate_commit_command
from src.cookcommit.commands.pr import generate_pr_command

app = typer.Typer(
    name="cookcommit",
    help="AI-powered git commit and PR message generator",
    add_completion=False
)

# Register commands
app.command("save", help="Save git diff --cached to a text file")(save_command)
app.command("commit", help="Generate commit message from staged changes")(generate_commit_command)
app.command("pr", help="Generate PR message from staged changes")(generate_pr_command)


if __name__ == "__main__":
    app()
