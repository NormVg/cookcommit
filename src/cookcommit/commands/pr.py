"""
Generate PR command implementation.
"""

import typer
from typing import Optional

from ..services.git_service import GitService
from ..services.ai_service import AIService
from ..utils.file_utils import save_to_file
from ..utils.output_utils import (
    print_error, print_info, print_loader,
    print_result_box, print_next_steps
)


def generate_pr_command(
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save PR message to file"),
    title_only: bool = typer.Option(False, "--title-only", help="Generate only PR title"),
) -> None:
    """
    Generate a Pull Request message from git diff --cached using Gemini AI.
    """
    # Check if we're in a git repository
    if not GitService.is_git_repository():
        print_error("Not in a git repository")
        raise typer.Exit(1)

    # Check for staged changes
    if not GitService.has_staged_changes():
        print_info("No staged changes found")
        print_info("Use 'git add <files>' to stage changes first")
        return

    # Get staged diff
    diff_content, success = GitService.get_staged_diff()

    if not success:
        print_error(diff_content)  # diff_content contains error message
        raise typer.Exit(1)

    try:
        if title_only:
            print_loader("Generating PR title...")
        else:
            print_loader("Generating PR message...")

        # Generate PR message using AI
        ai_service = AIService()
        pr_message = ai_service.generate_pr_message(diff_content, title_only)

        # Display the generated PR message
        title = "Generated PR Title" if title_only else "Generated PR Message"
        save_info = None
        if output_file and save_to_file(pr_message, output_file):
            save_info = f"Saved PR message to: {output_file}"

        print_result_box(title, pr_message, save_info)

        # Show next steps
        if title_only:
            steps = [
                "Copy the title above for your PR",
                "Use when creating pull request on GitHub/GitLab"
            ]
        else:
            steps = [
                "Copy the message above for your PR",
                "Use the title as PR title and description as PR body"
            ]
            if output_file:
                steps.append(f"Or copy from file: {output_file}")

        print_next_steps(steps)

    except Exception as e:
        print_error(f"Error generating PR message: {e}")
        raise typer.Exit(1)
