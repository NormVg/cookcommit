"""
Generate commit command implementation.
"""

import typer
from typing import Optional

from ..services.git_service import GitService
from ..services.ai_service import AIService
from ..utils.file_utils import save_to_file
from ..utils.output_utils import (
    print_error, print_success, print_info, print_loader,
    print_result_box, print_next_steps, extract_first_line
)


def generate_commit_command(
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save commit message to file"),
    auto_commit: bool = typer.Option(False, "--commit", "-c", help="Automatically commit with generated message"),
) -> None:
    """
    Generate a commit message from git diff --cached using Gemini AI.
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
        print_loader("Generating commit message...")

        # Generate commit message using AI
        ai_service = AIService()
        commit_message = ai_service.generate_commit_message(diff_content)

        # Display the generated commit message
        save_info = None
        if output_file and save_to_file(commit_message, output_file):
            save_info = f"Saved commit message to: {output_file}"

        print_result_box("Generated Commit Message", commit_message, save_info)

        # Auto-commit if requested
        if auto_commit:
            first_line = extract_first_line(commit_message)
            result, commit_success = GitService.commit_with_message(first_line)

            if commit_success:
                print_success("Successfully committed changes!")
                print_info(f"Commit message: {first_line}")
            else:
                print_error(f"Failed to commit: {result}")
                raise typer.Exit(1)
        else:
            # Show next steps
            steps = [
                "Copy the message above",
                f'Run: git commit -m "{extract_first_line(commit_message)}"'
            ]
            if output_file:
                steps.append(f"Or use: git commit -F {output_file}")

            print_next_steps(steps)

    except Exception as e:
        print_error(f"Error generating commit message: {e}")
        raise typer.Exit(1)
