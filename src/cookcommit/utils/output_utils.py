"""
Output formatting utilities.
"""

from typing import Optional


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"❌ {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✅ {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"💡 {message}")


def print_loader(message: str) -> None:
    """Print a loader message."""
    print(f"🤖 {message}")


def print_result_box(title: str, content: str, save_info: Optional[str] = None) -> None:
    """
    Print content in a formatted box.

    Args:
        title: Box title
        content: Content to display
        save_info: Optional save information
    """
    print("\n" + "="*60)
    print(f"📝 {title}:")
    print("="*60)
    print(content)
    print("="*60)

    if save_info:
        print(f"\n💾 {save_info}")


def print_next_steps(steps: list[str]) -> None:
    """Print next steps."""
    print("\n💡 Next steps:")
    for step in steps:
        print(f"   • {step}")


def extract_first_line(text: str) -> str:
    """Extract the first line from multi-line text."""
    return text.split('\n')[0] if text else ""
