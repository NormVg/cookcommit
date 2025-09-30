"""
Git operations service.
"""

import subprocess
from pathlib import Path
from typing import Tuple


class GitService:
    """Service for handling git operations."""

    @staticmethod
    def is_git_repository() -> bool:
        """Check if current directory is a git repository."""
        return Path('.git').exists()

    @staticmethod
    def get_staged_diff() -> Tuple[str, bool]:
        """
        Get staged changes using git diff --cached.

        Returns:
            Tuple of (diff_content, success)
        """
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout, True
        except subprocess.CalledProcessError as e:
            return f"Git command failed: {e}", False
        except FileNotFoundError:
            return "Git not found. Please install git.", False

    @staticmethod
    def has_staged_changes() -> bool:
        """Check if there are any staged changes."""
        diff_content, success = GitService.get_staged_diff()
        return success and diff_content.strip() != ""

    @staticmethod
    def commit_with_message(message: str) -> Tuple[str, bool]:
        """
        Commit staged changes with the given message.

        Args:
            message: Commit message

        Returns:
            Tuple of (result_message, success)
        """
        try:
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout, True
        except subprocess.CalledProcessError as e:
            return f"Git commit failed: {e.stderr}", False
