"""Setup configuration for CookCommit."""

from setuptools import setup, find_packages

setup(
    name="cookcommit",
    version="1.0.0",
    description="AI-powered git commit and PR message generator",
    author="CookCommit Team",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "typer>=0.12.0",
        "google-genai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cookcommit=cookcommit.main:app",
        ],
    },
    python_requires=">=3.8",
)
