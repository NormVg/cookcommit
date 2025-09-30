# CookCommit CLI

A modular CLI tool for AI-powered git commit and PR message generation using Gemini AI.

## 🏗️ Project Structure

```
cookcommit/
├── src/
│   └── cookcommit/
│       ├── __init__.py
│       ├── config.py              # Configuration constants
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── save.py            # Save diff command
│       │   ├── commit.py          # Generate commit command
│       │   └── pr.py              # Generate PR command
│       ├── services/
│       │   ├── __init__.py
│       │   ├── git_service.py     # Git operations
│       │   └── ai_service.py      # AI message generation
│       └── utils/
│           ├── __init__.py
│           ├── text_utils.py      # Text processing
│           ├── file_utils.py      # File operations
│           └── output_utils.py    # Output formatting
├── cli.py                         # Main entry point
├── setup.py                       # Package setup
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Basic Commands

```bash
# Save git diff to file
python cli.py save -o my-diff.txt

# Generate commit message
python cli.py commit

# Generate commit message and auto-commit
python cli.py commit --commit

# Generate PR message
python cli.py pr

# Generate PR title only
python cli.py pr --title-only
```

### Advanced Usage

```bash
# Generate commit message with output file
python cli.py commit -o commit-msg.txt

# Auto-commit with AI-generated message
python cli.py commit --commit

# Generate PR message and save to file
python cli.py pr -o pr-message.md
```

## 🔧 Features

### Save Command
- ✅ Saves `git diff --cached` to text file
- ✅ Checks for git repository
- ✅ Handles empty staged changes

### Commit Command
- ✅ Generates AI-powered commit messages
- ✅ Uses conventional commit format
- ✅ Automatic chunking for large diffs
- ✅ **Auto-commit flag** (`--commit`)
- ✅ Save to file option
- ✅ Clean, minimal output

### PR Command
- ✅ Generates comprehensive PR messages
- ✅ Title-only option
- ✅ Markdown formatting
- ✅ Handles large codebases
- ✅ Save to file option

## 🤖 AI Features

- **Smart Chunking**: Automatically handles large diffs
- **Conventional Commits**: Follows industry standards
- **Context-Aware**: Understands code changes
- **Multi-Model**: Uses different models for speed/quality

## 📋 Command Reference

### `save`
```bash
python cli.py save [OPTIONS]

Options:
  -o, --output TEXT  Output file name [default: diff.txt]
```

### `commit`
```bash
python cli.py commit [OPTIONS]

Options:
  -o, --output TEXT  Save commit message to file
  -c, --commit       Automatically commit with generated message
```

### `pr`
```bash
python cli.py pr [OPTIONS]

Options:
  -o, --output TEXT  Save PR message to file
  --title-only       Generate only PR title
```

## 🔄 Complete Workflow

```bash
# 1. Make changes and stage them
git add src/feature.py

# 2. Generate and auto-commit
python cli.py commit --commit

# 3. Generate PR message for GitHub
python cli.py pr -o pr-template.md
```

## 🏭 Architecture Benefits

- **Modular Design**: Separated concerns across multiple files
- **Service Layer**: Clean separation of git and AI operations
- **Utility Functions**: Reusable components
- **Type Hints**: Better code documentation and IDE support
- **Error Handling**: Comprehensive error management
- **Extensible**: Easy to add new commands and features
