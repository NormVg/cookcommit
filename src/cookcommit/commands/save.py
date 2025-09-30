"""
Save command implementation.
"""

import typer
from typing import Optional

from ..services.git_service import GitService
from ..utils.file_utils import save_to_file
from ..utils.output_utils import print_error, print_success, print_info
from ..config import DEFAULT_DIFF_FILE


def save_command(
    output: str = typer.Option(DEFAULT_DIFF_FILE, "--output", "-o", help="Output file name"),
) -> None:
    """
    Save git diff --cached output to a text file.
    """
    # Check if we're in a git repository
    if not GitService.is_git_repository():
        print_error("Not in a git repository")
        raise typer.Exit(1)

    # Get staged diff
    diff_content, success = GitService.get_staged_diff()

    if not success:
        print_error(diff_content)  # diff_content contains error message
        raise typer.Exit(1)

    if not diff_content.strip():
        print_info("No staged changes found")
        print_info("Use 'git add <files>' to stage changes first")
        return

    # Save to file
    if save_to_file(diff_content, output):
        print_success(f"Saved git diff --cached to: {output}")
    else:
        print_error(f"Failed to save to file: {output}")
        raise typer.Exit(1)
