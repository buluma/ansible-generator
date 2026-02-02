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
            if repo["name"].startswith(PREFIX) and not repo["archived"]:
                # Construct HTTPS URL with token for authentication
                https_url = repo["clone_url"].replace("https://", f"https://oauth2:{GH_TOKEN}@")
                repos.append(https_url)

        page += 1

    return repos

def clone_repo(repo_url):
    """
    Clone a repository into the CLONE_DIR.
    """
    # The repo_url now contains the token for HTTPS authentication
    repo_name = repo_url.split("/")[-1].replace(".git", "").split('@')[-1].replace('github.com/', '') # Extracting repo name from HTTPS URL with token

    # Ensure repo_name is clean, sometimes there's an extra '/'
    if '/' in repo_name:
        repo_name = repo_name.split('/')[-1]

    clone_path = os.path.join(CLONE_DIR, repo_name)

    if os.path.exists(clone_path):
        print(f"Repository {repo_name} already exists. Skipping.")
        return

    print(f"Cloning {repo_name} from {repo_url.split('@')[-1]} into {clone_path}...")
    subprocess.run(["git", "clone", repo_url, clone_path], check=True)

if __name__ == "__main__":
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    all_repos = get_repos()
    print(f"Found {len(all_repos)} repositories to clone.")

    if not all_repos:
        print("No repositories found or an error occurred. Exiting.")
    else:
        for repo_url in all_repos:
            clone_repo(repo_url)

        print("Done.")
