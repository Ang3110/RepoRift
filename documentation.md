# RepoRift Documentation

## Overview
RepoRift is a terminal-based tool for seamless management of GitHub repositories. It provides a streamlined workflow for exporting, merging, and organizing repositories and files, with a focus on usability and clarity.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Authentication](#authentication)
- [Main Menu](#main-menu)
- [Repository Management](#repository-management)
- [Merge Workflow](#merge-workflow)
- [Export Workflow](#export-workflow)
- [Search & Filtering](#search--filtering)
- [Security](#security)
- [FAQ](#faq)

---

## Features
- Clean, minimal terminal UI
- List/search repositories
- Export/clone multiple repositories at once
- Merge local files or folders into any repo/branch
- Flexible destination paths for merged files
- Branch selection and creation
- Integrated help and about menus
- Secure token handling and logout

---

## Installation
1. Ensure you have Python 3.7+ installed.
2. (Recommended) Set up a Python virtual environment. This is especially helpful if you encounter SSH permission conflicts or broken Python configurations:
   - On Linux & macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows (Command Prompt):
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
3. Install dependencies:
   ```bash
   pip install GitPython PyGithub inquirer
   ```
   If you see an error about `inquirer` missing, simply run:
   ```bash
   pip install inquirer
   ```
4. Place your GitHub Personal Access Token in a file named `token` in the project directory, or enter it when prompted.

---

## Authentication
- On first run, you'll be prompted for your GitHub username and Personal Access Token (PAT).
- The token is stored securely and removed on logout.
- Fine-grained PATs are recommended for best security.

---

## Main Menu
```
1. repositories
2. Clone repository by URL
3. About
4. Help
5. Logout
6. Exit
```
- Use the number or hotkey for navigation.
- Type `b` to go back at any menu.

---

## Repository Management
- **Listing:** Shows all your repositories.
- **Searching:** Use `search <term>` to filter repos by name. Press Enter on blank to reset filter.
- **Exporting:** Select one or more repos using numbers, comma-separated lists, or ranges.
- **Merging:** Use `merge <repo_number>` to start the merge workflow for a specific repo.

---

## Merge Workflow
1. Select a repository and branch.
2. Paste a valid file or directory path (or type `b` to go back).
3. Choose where to place the file/folder in the repo (keep original path or specify custom).
4. Enter a commit message and confirm push.

---

## Export Workflow
- Choose destination directory (default is `repositories/` in your current working directory).
- Supports batch export of multiple repos.

---

## Search & Filtering
- Use `search <term>` to filter repositories.
- Press Enter on a blank input to reset the filter.

---

## Security
- Tokens are stored with restricted permissions (`chmod 600`).
- Logout deletes the token file.
- No sensitive information is logged or displayed.

---

## FAQ
**Q: How do I go back in a menu?**  
A: Type `b` at any prompt.

**Q: How do I merge a file into a specific folder in the repo?**  
A: After selecting the file, choose the custom destination option and enter the desired path.

**Q: Is my token safe?**  
A: Yes. Tokens are stored securely and deleted on logout.

**Q: Will my token transfer if I move the program to a different directory or a new machine?**  
A: No. The token is stored in a file named `token` in the same directory as the program. If you move the program to a new directory or machine, you must also move the `token` file with it (or re-enter your token when prompted).

---

For more information, see the README.md or use the in-app Help menu.
