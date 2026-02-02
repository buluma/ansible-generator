import os
import subprocess
import requests

# Your GitHub username (used for filtering if needed, though API will use authenticated user)
GH_USER = "buluma"
# The prefix of the repositories you want to clone
PREFIX = "ansible-role-"
# Directory to clone into
CLONE_DIR = "../ansible-roles"
# Get the token from an environment variable
GH_TOKEN = os.environ.get("GITHUB_TOKEN")

def get_repos():
    """
    Get all repositories for the authenticated user that start with the given prefix.
    """
    if not GH_TOKEN:
        print("GITHUB_TOKEN environment variable not set.")
        print("Please set it to your GitHub personal access token.")
        print("e.g. export GITHUB_TOKEN=your_token_here")
        return []

    repos = []
    page = 1
    headers = {"Authorization": f"token {GH_TOKEN}"}
    while True:
        # Use /user/repos to list repositories for the authenticated user
        # type=owner filters for repositories owned by the authenticated user
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&type=owner"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            try:
                print(f"Response: {response.json()}")
            except ValueError:
                print(f"Response text: {response.text}")
            break

        data = response.json()
        if not data:
            break

        for repo in data:
            if repo["name"].startswith(PREFIX):
                repos.append(repo)

        page += 1

    return repos

def process_repo(repo):
    """
    Process a single repository.
    """
    repo_name = repo["name"]
    clone_path = os.path.join(CLONE_DIR, repo_name)
    archived_path = os.path.join(CLONE_DIR, f"archived-{repo_name}")

    if repo["archived"]:
        if os.path.exists(clone_path):
            print(f"Repository {repo_name} is archived and exists. Renaming to {archived_path}...")
            os.rename(clone_path, archived_path)
        elif os.path.exists(archived_path):
            print(f"Archived repository {repo_name} already exists as {archived_path}. Skipping.")
        else:
            print(f"Repository {repo_name} is archived and does not exist locally. Skipping cloning.")
    else:
        if os.path.exists(clone_path):
            print(f"Repository {repo_name} already exists. Skipping.")
        else:
            print(f"Cloning {repo_name}...")
            https_url = repo["clone_url"].replace("https://", f"https://oauth2:{GH_TOKEN}@")
            subprocess.run(["git", "clone", https_url, clone_path], check=True)

if __name__ == "__main__":
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    all_repos = get_repos()
    print(f"Found {len(all_repos)} repositories to process.")

    if not all_repos:
        print("No repositories found or an error occurred. Exiting.")
    else:
        for repo in all_repos:
            process_repo(repo)

        print("Done.")
