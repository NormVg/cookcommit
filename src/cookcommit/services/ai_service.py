"""
AI service for generating commit and PR messages.
"""

from typing import List, Optional
from google import genai
from ..config import API_KEY, DEFAULT_MODEL, LITE_MODEL
from ..utils.text_utils import chunk_text


class AIService:
    """Service for AI-powered message generation."""

    def __init__(self):
        """Initialize the AI service with Gemini client."""
        self.client = genai.Client(api_key=API_KEY)

    def generate_commit_message(self, diff_content: str) -> str:
        """
        Generate a commit message from git diff content.

        Args:
            diff_content: Git diff content

        Returns:
            Generated commit message
        """
        chunks = chunk_text(diff_content)

        if len(chunks) == 1:
            prompt = self._create_single_chunk_commit_prompt(chunks[0])
        else:
            prompt = self._create_multi_chunk_commit_prompt(chunks)

        response = self.client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        return response.text.strip()

    def generate_pr_message(self, diff_content: str, title_only: bool = False) -> str:
        """
        Generate a PR message from git diff content.

        Args:
            diff_content: Git diff content
            title_only: Generate only PR title if True

        Returns:
            Generated PR message or title
        """
        chunks = chunk_text(diff_content)

        if len(chunks) == 1:
            prompt = self._create_single_chunk_pr_prompt(chunks[0], title_only)
        else:
            prompt = self._create_multi_chunk_pr_prompt(chunks, title_only)

        response = self.client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        return response.text.strip()

    def _summarize_chunk(self, chunk: str) -> str:
        """Summarize a single diff chunk."""
        summary_prompt = f"""
Summarize the changes in this git diff chunk. Be concise and focus on what was modified:

{chunk}

Provide a brief summary of the changes:
"""

        response = self.client.models.generate_content(
            model=LITE_MODEL,
            contents=summary_prompt
        )
        return response.text.strip()

    def _create_single_chunk_commit_prompt(self, chunk: str) -> str:
        """Create prompt for single chunk commit message."""
        return f"""
Analyze this git diff and generate a concise, informative commit message with a small explanation.

Rules for the commit message:
1. Use conventional commit format: type(scope): description
2. Types: feat, fix, docs, style, refactor, test, chore
3. Keep the first line under 50 characters
4. Be specific about what changed
5. Focus on the "why" and "what", not the "how"

Git diff:
{chunk}

Generate only the commit message, nothing else.
"""

    def _create_multi_chunk_commit_prompt(self, chunks: List[str]) -> str:
        """Create prompt for multi-chunk commit message."""
        # Summarize each chunk first
        chunk_summaries = []
        for chunk in chunks:
            summary = self._summarize_chunk(chunk)
            chunk_summaries.append(summary)

        return f"""
Based on these summaries of git diff chunks, generate a concise, informative commit message.

Rules for the commit message:
1. Use conventional commit format: type(scope): description
2. Types: feat, fix, docs, style, refactor, test, chore
3. Keep the first line under 50 characters
4. Be specific about what changed
5. Focus on the "why" and "what", not the "how"

Change summaries:
{chr(10).join(f"Chunk {i+1}: {summary}" for i, summary in enumerate(chunk_summaries))}

Generate only the commit message, nothing else.
"""

    def _create_single_chunk_pr_prompt(self, chunk: str, title_only: bool) -> str:
        """Create prompt for single chunk PR message."""
        if title_only:
            return f"""
Analyze this git diff and generate a concise Pull Request title.

Rules for the PR title:
1. Keep it under 72 characters
2. Use conventional commit format: type(scope): description
3. Types: feat, fix, docs, style, refactor, test, chore
4. Be specific about what changed
5. Focus on the main feature/change

Git diff:
{chunk}

Generate only the PR title, nothing else.
"""
        else:
            return f"""
Analyze this git diff and generate a comprehensive Pull Request message.

Format the PR message as follows:
1. Title: Use conventional commit format (type(scope): description) - keep under 72 characters
2. Description: Explain what this PR does and why
3. Changes: List the main changes made
4. Testing: Mention how this should be tested (if applicable)

Rules:
- Be clear and informative
- Focus on the "what" and "why"
- Use markdown formatting
- Include relevant details for reviewers

Git diff:
{chunk}

Generate a complete PR message with title and description.
"""

    def _create_multi_chunk_pr_prompt(self, chunks: List[str], title_only: bool) -> str:
        """Create prompt for multi-chunk PR message."""
        # Summarize each chunk first
        chunk_summaries = []
        for chunk in chunks:
            summary = self._summarize_chunk(chunk)
            chunk_summaries.append(summary)

        if title_only:
            return f"""
Based on these summaries of git diff chunks, generate a concise Pull Request title.

Rules for the PR title:
1. Keep it under 72 characters
2. Use conventional commit format: type(scope): description
3. Types: feat, fix, docs, style, refactor, test, chore
4. Be specific about what changed
5. Focus on the main feature/change

Change summaries:
{chr(10).join(f"Chunk {i+1}: {summary}" for i, summary in enumerate(chunk_summaries))}

Generate only the PR title, nothing else.
"""
        else:
            return f"""
Based on these summaries of git diff chunks, generate a comprehensive Pull Request message.

Format the PR message as follows:
1. Title: Use conventional commit format (type(scope): description) - keep under 72 characters
2. Description: Explain what this PR does and why
3. Changes: List the main changes made
4. Testing: Mention how this should be tested (if applicable)

Rules:
- Be clear and informative
- Focus on the "what" and "why"
- Use markdown formatting
- Include relevant details for reviewers

Change summaries:
{chr(10).join(f"Chunk {i+1}: {summary}" for i, summary in enumerate(chunk_summaries))}

Generate a complete PR message with title and description.
"""
