# RepoRift

A powerful, terminal-based tool for managing your GitHub repositories with ease. RepoRift streamlines repository management, merging, and exporting, all from a clean and intuitive command-line interface.

## Features

- **Repository Listing & Search:**
  - View all your repositories.
  - Search repositories by name (e.g., `search <term>`).
- **Export (Clone) Repositories:**
  - Export one or multiple repositories to your local machine.
  - Use numbers, comma-separated lists, or ranges (e.g., `1,3-5`).
- **Merge Local Files/Folders:**
  - Merge any file or folder from your system into a selected remote GitHub repository and branch.
  - Choose the target path in the repo for each file/folder.
  - Supports both files and directories.
- **Branch Management:**
  - Select any branch (local or remote) for merge operations.
  - Create new branches on the fly.
- **Clean Menus:**
  - Minimal, readable prompts.
  - Easy navigation with `b` to go back at any menu.
- **Help & About:**
  - Built-in help menu for quick reference.
  - About page for project information.

## Getting Started

### Prerequisites
- Python 3.7+
- [GitPython](https://gitpython.readthedocs.io/en/stable/)
- [PyGithub](https://pygithub.readthedocs.io/en/latest/)

Install dependencies:
```bash
pip install GitPython PyGithub
```

### Usage
1. Run the program:
   ```bash
   python3 reporift.py
   ```
2. Authenticate with your GitHub token (PAT).
3. Use the menu to:
   - List/search repositories
   - Export (clone) repositories
   - Merge local files/folders into a remote repo/branch
   - Get help or view about info

### Example Workflows
- **Export multiple repos:**
  - Enter: `1,3-5` to export repos 1, 3, 4, and 5.
- **Search:**
  - Enter: `search calculator` to filter repos by name.
- **Merge:**
  - Enter: `merge 2` to merge files/folders into the 2nd repo.
  - Paste a valid path, select the branch, and specify the target path in the repo.

## Security
- Uses GitHub Personal Access Tokens (PATs).
- Tokens are stored securely and never exposed.
- Logout removes the token from disk.

## Menu Overview

```
1. repositories
2. Clone repository by URL
3. About
4. Help
5. Logout
6. Exit
```

- **repositories:** List and manage your GitHub repositories.
- **Clone repository by URL:** Clone any public or private repo using its URL.
- **About:** Information about RepoRift.
- **Help:** Show help menu.
- **Logout:** Log out of your GitHub account.
- **Exit:** Quit the program.

thanks to GitHub Copilot for its merge feature; the process of getting it working proved to be quite challenge.
