# ===============================
# RepoRift
# Author: Angello
# Description: Terminal-based tool for managing GitHub repositories.
# Features: Login, clone, export, push local files, and more.
# ===============================

import os
import sys
import time
import shutil
from github import Github, InputGitTreeElement
import inquirer
from getpass import getpass
import requests
from git import Repo
import subprocess
import re
import json
from pathlib import Path
import shlex

class RepoRift:
    """
    Terminal-based GitHub Repository Manager (RepoRift).
    Features:
    - Login to GitHub
    - Clone repositories by URL
    - Export (clone) repositories in bulk or individually
    - Push local files or directories to a remote GitHub repo
    - Search/filter repositories
    """

    def __init__(self):
        self.github_client = None
        self.user = None
        self.token_file = os.path.join(str(Path.home()), '.reprrift_token')
        self.github_username = None
        self.github_token = None
        if self.load_saved_token():
            self.main_menu()
        else:
            self.login_menu()

    def load_saved_token(self):
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    token = f.read().strip()
                    if token:
                        try:
                            self.github_client = Github(token)
                            self.user = self.github_client.get_user()
                            _ = self.user.login  # Will raise if token is invalid
                            self.github_token = token
                            return True
                        except Exception:
                            print("\nSaved GitHub token is invalid or expired. Please log in again.")
                            os.remove(self.token_file)
                            time.sleep(1)
                            return False
        except Exception:
            pass
        return False

    def save_token(self, token):
        try:
            with open(self.token_file, 'w') as f:
                f.write(token)
            os.chmod(self.token_file, 0o600)
            return True
        except Exception:
            return False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("="*50)
        print("RepoRift")
        print("="*50)

    def login_menu(self):
        while True:
            try:
                self.clear_screen()
                self.print_header()
                print("\n1. Login with GitHub credentials")
                print("2. Clone repository by URL")
                print("3. About")
                print("4. Exit or (Ctrl + C)")
                choice = input().strip()
                if choice == '1':
                    self.github_login()
                elif choice == '2':
                    self.clone_repo_by_url()
                elif choice == '3':
                    self.about_page()
                elif choice == '4':
                    sys.exit(0)
            except KeyboardInterrupt:
                print("\nQuitting program")
                sys.exit(0)

    def github_login(self):
        if self.github_client and self.user:
            self.main_menu()
            return
        while True:
            self.clear_screen()
            self.print_header()
            print("\nGitHub Login")
            print("-"*20)
            print("Enter your GitHub Personal Access Token (or 'B' to go back): ")
            token = getpass("")
            if token.strip().lower() == 'b':
                return
            try:
                client = Github(token)
                user = client.get_user()
                # Test token validity explicitly
                try:
                    login = user.login  # This will raise BadCredentialsException if invalid
                except Exception:
                    print("\ninvalid token")
                    time.sleep(1)
                    continue
                self.github_client = client
                self.user = user
                self.github_username = user.login
                self.github_token = token
                if self.save_token(token):
                    print("\nLogin successful!")
                    time.sleep(1)
                    self.main_menu()
                    return
            except Exception:
                print("\ninvalid token")
                time.sleep(1)
                continue

    def get_valid_directory(self, repo_name):
        while True:
            try:
                self.clear_screen()
                self.print_header()
                print("\nSelect destination option:")
                print("1. local repository folder")
                print("2. Choose existing directory")
                print("B. Back to menu")
                choice = input().strip().upper()
                if choice == 'B':
                    return None
                elif choice == '1':
                    base = os.path.join(os.getcwd(), "repositories")
                    os.makedirs(base, exist_ok=True)
                    return os.path.join(base, repo_name)
                elif choice == '2':
                    while True:
                        directory = input("\nEnter destination directory (or 'B' to go back): ").strip()
                        if directory.lower() == 'b':
                            break
                        if not directory:
                            print("Error: Directory cannot be empty.")
                            continue
                        directory = os.path.expanduser(directory)
                        if not os.path.isdir(directory):
                            print("Error: Directory does not exist.")
                            continue
                        return os.path.join(directory, repo_name)
                else:
                    print("Invalid choice.")
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nQuitting program")
                sys.exit(0)

    def clone_repo_by_url(self):
        while True:
            self.clear_screen()
            self.print_header()
            url = input("\nEnter the repository URL to clone (or 'B' to go back): ").strip()
            if url.lower() == 'b': return
            if url.startswith('https://github.com/'):
                url_git = url if url.endswith('.git') else url + '.git'
            else:
                print("Invalid GitHub URL.")
                time.sleep(1)
                continue
            repo_name = url_git.rstrip('/').split('/')[-1].replace('.git','')
            while True:
                self.clear_screen()
                self.print_header()
                print(f"\nRepository: {repo_name}")
                print("\nSelect destination option:")
                print("1. local repository folder")
                print("2. Choose existing directory")
                print("B. Back to menu")
                choice = input().strip().upper()
                if choice == 'B': return
                elif choice == '1':
                    dest = os.path.join(os.getcwd(), "repositories", repo_name)
                elif choice == '2':
                    while True:
                        path = input("Enter the path to the existing directory (or 'B' to go back): ").strip()
                        if path.lower() == 'b':
                            dest = None
                            break
                        elif os.path.isdir(path):
                            confirm = input("Confirm export? (y/n): ").strip().lower()
                            if confirm == 'y':
                                dest = os.path.join(path, repo_name)
                                break
                            elif confirm == 'n':
                                continue
                            else:
                                print("Invalid input. Please enter 'y' for yes or 'n' for no.")
                        else:
                            print("Invalid directory.")
                    if dest is None:
                        continue
                else:
                    print("Invalid choice.")
                    time.sleep(1)
                    continue
                if os.path.exists(dest) and os.listdir(dest):
                    print(f"Destination '{dest}' exists and is not empty.")
                    input("Press Enter to continue...")
                    return
                try:
                    Repo.clone_from(url_git, dest)
                    print(f"Cloned: {dest}")
                    input("Press Enter to continue...")
                except Exception as e:
                    print(f"Clone failed: {e}")
                    input("Press Enter to continue...")
                return

    def main_menu(self):
        while True:
            try:
                self.clear_screen()
                self.print_header()
                print(f"\nLogged in as: {self.user.login}")
                print("1. repositories")
                print("2. Clone repository by URL")
                print("3. About")
                print("4. Help")
                print("5. Logout")
                print("6. Exit")
                choice = input().strip()
                if choice == '1': self.repository_list_menu()
                elif choice == '2': self.clone_repo_by_url()
                elif choice == '3': self.about_page()
                elif choice == '4':
                    self.help_menu()
                elif choice == '5':
                    self.github_client = None; self.user = None
                    if os.path.exists(self.token_file): os.remove(self.token_file)
                    self.login_menu(); return
                elif choice == '6':
                    print("Quitting program")
                    sys.exit(0)
                else:
                    print("Invalid choice.")
                    input("Press Enter to continue...")
            except KeyboardInterrupt:
                print("\nQuitting program")
                sys.exit(0)

    def repository_list_menu(self):
        repos = list(self.user.get_repos())
        filter_term = ""
        while True:
            self.clear_screen()
            self.print_header()
            filtered = [r for r in repos if filter_term.lower() in r.name.lower()]
            print("\nYour repositories:")
            for i, repo in enumerate(filtered, 1):
                print(f"{i}. {repo.name}{' (private)' if repo.private else ''}")
            print("\nCommands: search <term>, numbers (e.g. 1,3-5) to export, merge <repo_number>, B to go back")
            selection = input().strip()
            # If filter is active and user presses enter on blank, reset filter
            if not selection:
                if filter_term:
                    filter_term = ""
                    continue
                else:
                    continue
            if selection.lower().startswith('search'):
                parts = selection.split(' ', 1)
                filter_term = parts[1] if len(parts) > 1 else ""
                continue
            if selection.lower().startswith('merge'):
                parts = selection.split()
                if len(parts) == 2 and parts[1].isdigit():
                    idx = int(parts[1])
                    if 1 <= idx <= len(filtered):
                        self.merge_local_files_into_remote_repo(preselected_repo=filtered[idx-1])
                        continue
                    else:
                        print("Invalid repository number for merge.")
                        input("Press Enter to continue...")
                        continue
                else:
                    print("Usage: merge <repo_number>")
                    input("Press Enter to continue...")
                    continue
            if re.match(r'^([\d]+(-[\d]+)?)(,[\d]+(-[\d]+)?)*$', selection):
                sels = []
                for part in selection.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-', 1)); sels.extend(range(start, end + 1))
                    else:
                        sels.append(int(part))
                dest_dir = None
                while True:
                    print("\nSelect destination option:")
                    print("1. local repository folder")
                    print("2. Choose existing directory")
                    print("B. Back to menu")
                    choice = input().strip().upper()
                    if choice == '1':
                        dest_dir = os.path.join(os.getcwd(), "repositories")
                        break
                    elif choice == '2':
                        while True:
                            path = input("Enter the path to the existing directory (or 'B' to go back): ").strip()
                            if path.lower()=='b': 
                                dest_dir = None
                                break
                            elif os.path.isdir(path):
                                confirm = input("Confirm export? (y/n): ").strip().lower()
                                if confirm == 'y':
                                    dest_dir = path
                                    break
                                elif confirm == 'n':
                                    continue
                                else:
                                    print("Invalid input. Please enter 'y' for yes or 'n' for no.")
                            else:
                                print("Invalid directory.")
                        if dest_dir is not None:
                            break
                    elif choice == 'B':
                        break
                    else:
                        print("Invalid choice."); time.sleep(1)
                if not dest_dir:
                    print("Export cancelled."); time.sleep(1); continue
                print("cloning:")
                for num in sorted(set(sels)):
                    idx = num - 1
                    if 0 <= idx < len(filtered):
                        repo = filtered[idx]
                        repo_dir = os.path.join(dest_dir, repo.name)
                        if os.path.exists(repo_dir) and os.listdir(repo_dir):
                            status = 'exists'
                        else:
                            try:
                                Repo.clone_from(repo.clone_url, repo_dir)
                                status = 'cloned'
                            except Exception as e:
                                status = f'failed ({e})'
                        print(f"{repo.name}   {status}")
                print()
                if dest_dir == os.path.join(os.getcwd(), "repositories"):
                    print(f"Cloning complete. saved in: {dest_dir}")
                else:
                    print("Cloning complete.")
                print()
                input("\nPress Enter to return...")
                continue
            if selection.lower() == 'b':
                return
            print("Invalid input.")
            input("Press Enter to continue...")

    def repository_details_menu(self, repo):
        while True:
            self.clear_screen()
            self.print_header()
            print(f"\nRepository: {repo.name}")
            print("1. Export (clone) this repository")
            print("2. Merge local files/folders into this repository")
            print("B. Back to list")
            choice = input().strip().lower()
            if choice == '1':
                self.export_selected_repository(repo)
            elif choice == '2':
                self.merge_local_files_into_remote_repo(preselected_repo=repo)
            elif choice == 'b':
                return
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def prompt_common_export_destination(self):
        while True:
            print("\nSelect destination option:")
            print("1. local repository folder")
            print("2. Choose existing directory")
            print("B. Back to menu")
            choice = input().strip().upper()
            if choice == '1':
                return os.path.join(os.getcwd(), "repositories")
            elif choice == '2':
                while True:
                    path = input("Enter the path to the existing directory (or 'B' to go back): ").strip()
                    if path.lower()=='b': 
                        break
                    elif os.path.isdir(path):
                        confirm = input("Confirm export? (y/n): ").strip().lower()
                        if confirm == 'y':
                            return path
                        elif confirm == 'n':
                            continue
                        else:
                            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
                    else:
                        print("Invalid directory.")
            elif choice == 'B':
                return None
            else:
                print("Invalid choice."); time.sleep(1)

    def export_repository(self, repo, summary_mode=False):
        while True:
            self.clear_screen()
            self.print_header()
            print(f"\nRepository: {repo.name}")
            print("\nSelect destination option:")
            print("1. local repository folder")
            print("2. Choose existing directory")
            print("B. Back to export menu")
            choice = input().strip().upper()
            if choice == '1':
                dest_dir = os.path.join(os.getcwd(),"repositories",repo.name)
            elif choice == '2':
                canceled=False
                while True:
                    path = input("Enter the path to the existing directory (or 'B' to go back): ").strip()
                    if path.lower()=='b': 
                        canceled=True
                        break
                    elif os.path.isdir(path):
                        confirm = input("Confirm export? (y/n): ").strip().lower()
                        if confirm == 'y':
                            dest_dir = os.path.join(path,repo.name);
                            break
                        elif confirm == 'n':
                            continue
                        else:
                            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
                    else:
                        print("Invalid directory.")
                if canceled: continue
            elif choice == 'B':
                return None
            else:
                print("Invalid choice."); time.sleep(1); continue
            if os.path.exists(dest_dir) and os.listdir(dest_dir):
                print(f"Directory '{dest_dir}' exists and is not empty.")
                if not summary_mode: input("Press Enter to continue...")
            else:
                print(f"Cloning '{repo.name}' into {dest_dir}...")
                try:
                    Repo.clone_from(repo.clone_url,dest_dir)
                    print("Clone complete.")
                    if not summary_mode: input("Press Enter to continue...")
                except Exception as e:
                    print(f"Clone failed: {e}")
                    if not summary_mode: input("Press Enter to continue...")
            return dest_dir

    def about_page(self):
        """
        Display the About page with summary, author, and documentation link.
        """
        self.clear_screen()
        self.print_header()
        print("\nabout")
        print("-" * 40)
        print("RepoRift is a terminal-based tool for managing your GitHub repositories.\n")
        print("Author:      Angello")
        print("Version:     1.0.0")
        print("License:     MIT")
        print("\nFeatures:")
        print("  - Login to GitHub with a personal access token")
        print("  - Clone repositories by URL")
        print("  - Export (clone) repositories in bulk or individually")
        print("  - Search and filter repositories")
        print("\nFor questions, concerns, and additional info visit:")
        print("  https://github.com/Ang3110/RepoRift")
        input("\nPress Enter to return...")

    def merge_local_files_into_remote_repo(self, preselected_repo=None):
        import git
        import tempfile
        import shutil
        self.clear_screen()
        self.print_header()
        print("\nMerge Local Files into Remote Repo")
        print("-" * 40)
        # Step 1: Select remote repo
        if preselected_repo is None:
            user_repos = list(self.user.get_repos())
            print("\nYour GitHub repositories:")
            for i, r in enumerate(user_repos, 1):
                print(f"{i}. {r.name}{' (private)' if r.private else ''}")
            idx = input().strip()
            if idx.lower() == 'b':
                return
            if not idx.isdigit() or int(idx) < 1 or int(idx) > len(user_repos):
                print("Invalid selection.")
                input("Press Enter to continue...")
                return
            remote_repo = user_repos[int(idx)-1]
        else:
            remote_repo = preselected_repo
        # Step 2: Clone repo to temp dir
        temp_dir = tempfile.mkdtemp(prefix='reporift_merge_')
        print(f"Cloning {remote_repo.full_name} into temporary directory...")
        token = getattr(self, 'github_token', None)
        if not token:
            try:
                with open(self.token_file, 'r') as f:
                    token = f.read().strip()
            except Exception:
                token = None
        if not token:
            print("No GitHub token available for push.")
            input("Press Enter to continue...")
            return
        remote_url = f"https://{token}@github.com/{remote_repo.full_name}.git"
        try:
            repo = git.Repo.clone_from(remote_url, temp_dir)
            # Fetch all remote branches
            repo.git.fetch('--all')
        except Exception as e:
            print(f"Failed to clone repo: {e}")
            shutil.rmtree(temp_dir)
            input("Press Enter to continue...")
            return
        # Step 3: List and select branch (show all remote branches)
        repo.git.fetch('--all')
        remote_branches = [ref.name.replace('origin/', '') for ref in repo.remotes.origin.refs if ref.name.startswith('origin/') and ref.name != 'origin/HEAD']
        local_branches = [h.name for h in repo.heads]
        all_branches = sorted(set(local_branches + remote_branches))
        if not all_branches:
            print("No branches found. Creating 'main' branch.")
            repo.git.checkout('-b', 'main')
            all_branches = ['main']
        print("\nAvailable branches:")
        for i, b in enumerate(all_branches, 1):
            print(f"{i}. {b}")
        branch_input = input().strip()
        if branch_input.lower() == 'b':
            shutil.rmtree(temp_dir)
            return
        if branch_input.lower() == 'n':
            new_branch = input("Enter new branch name: ").strip()
            if new_branch:
                try:
                    repo.git.checkout('-b', new_branch)
                    print(f"Switched to new branch '{new_branch}'.")
                except Exception as e:
                    print(f"Failed to create branch: {e}")
                    shutil.rmtree(temp_dir)
                    input("Press Enter to continue...")
                    return
            else:
                shutil.rmtree(temp_dir)
                return
        else:
            try:
                if branch_input.isdigit():
                    branch_name = all_branches[int(branch_input)-1]
                else:
                    branch_name = branch_input
                # If branch doesn't exist locally, check it out from remote
                if branch_name not in local_branches and branch_name in remote_branches:
                    repo.git.checkout('-b', branch_name, f'origin/{branch_name}')
                else:
                    repo.git.checkout(branch_name)
                print(f"Switched to branch '{branch_name}'.")
                # Always set upstream to origin/branch_name if it exists
                if branch_name in remote_branches:
                    try:
                        repo.git.branch('--set-upstream-to', f'origin/{branch_name}', branch_name)
                    except Exception:
                        pass
            except Exception as e:
                print(f"Failed to switch branch: {e}")
                shutil.rmtree(temp_dir)
                input("Press Enter to continue...")
                return
        # Step 4: Prompt for a single local file/folder path
        file_map = []  # list of tuples: (src_path, dest_path, is_dir)
        while True:
            path = input("\nEnter a file or directory path to merge (or type 'B' to go back): ").strip()
            if not path or path.lower() == 'b':
                shutil.rmtree(temp_dir)
                return
            if not os.path.exists(path):
                print("invalid path")
                continue
            src = path
            is_dir = os.path.isdir(src)
            # Suggest default destination
            if is_dir:
                default_dest = os.path.relpath(src, os.getcwd()) if os.path.commonpath([os.getcwd(), os.path.abspath(src)]) == os.getcwd() else os.path.basename(src)
            else:
                default_dest = os.path.relpath(src, os.getcwd()) if os.path.commonpath([os.getcwd(), os.path.abspath(src)]) == os.getcwd() else os.path.basename(src)
            print(f"Where do you want to place '{src}' in the repo?")
            print(f"1. Keep original path ({default_dest})")
            print("2. Specify custom path")
            choice = input().strip()
            if choice == '2':
                dest = input("Enter custom destination in repo: ").strip()
                if not dest:
                    dest = default_dest
            else:
                dest = default_dest
            file_map.append((src, dest, is_dir))
            break
        if not file_map:
            print("No files specified.")
            shutil.rmtree(temp_dir)
            input("Press Enter to continue...")
            return
        # Step 5: Copy files and folders into repo at chosen destinations
        for src, dest, is_dir in file_map:
            abs_dest = os.path.join(temp_dir, dest)
            if is_dir:
                # Copy folder contents to the destination directory in repo
                if os.path.exists(abs_dest):
                    shutil.rmtree(abs_dest)
                try:
                    shutil.copytree(src, abs_dest)
                    print(f"Copied directory {src} to {abs_dest} in repo.")
                except Exception as e:
                    print(f"Failed to copy directory {src}: {e}")
            else:
                os.makedirs(os.path.dirname(abs_dest), exist_ok=True)
                try:
                    shutil.copy2(src, abs_dest)
                    print(f"Copied file {src} to {abs_dest} in repo.")
                except Exception as e:
                    print(f"Failed to copy file {src}: {e}")
        # Step 6: Stage, commit, push
        repo.git.add(A=True)
        commit_msg = input("Enter commit message: ").strip()
        if not commit_msg:
            commit_msg = f"Merge local files via RepoRift at {__import__('datetime').datetime.now().isoformat()}"
        try:
            repo.index.commit(commit_msg)
        except Exception:
            pass  # ignore if nothing to commit
        try:
            branch = repo.active_branch.name
            repo.git.push('--set-upstream', 'origin', branch, force=True)
            print("Push successful!")
        except Exception as e:
            print(f"Push failed: {e}")
        input("\nPress Enter to return to menu...")
        shutil.rmtree(temp_dir)
        return

    def help_menu(self):
        self.clear_screen()
        self.print_header()
        print("\nHelp Menu")
        print("-"*40)
        print("1. repositories: List and manage your GitHub repositories.")
        print("2. Clone repository by URL: Clone any public or private repository using its URL.")
        print("3. About: Information about RepoRift.")
        print("4. Help: Show this help menu.")
        print("5. Logout: Log out of your GitHub account.")
        print("6. Exit: Quit the program.")
        print("\nIn repository menus, you can search, export, or merge files/folders into your repositories.")
        print("Type 'b' to go back at any menu.")
        input("\nPress Enter to return to the main menu...")
        return

if __name__ == "__main__":
    RepoRift()
