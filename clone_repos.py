import requests
import os

def get_user_repositories(username, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.github.com/users/{username}/repos"
    params = {"per_page": 100}  # Adjust the per_page parameter as needed
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve repositories for user {username}")
        print(f"Response: {response.text}")
        return None

def clone_repositories(repositories, destination_folder, repo_prefix):
    os.makedirs(destination_folder, exist_ok=True)
    os.chdir(destination_folder)

    for repo in repositories:
        repo_name = repo["name"]
        if repo_name.startswith(repo_prefix):
            repo_url = repo["clone_url"]
            os.system(f"git clone {repo_url}")

if __name__ == "__main__":
    github_username = "buluma"
    github_token = "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"  # Generate a token with repo scope from https://github.com/settings/tokens
    repo_prefix = "ansible-role-"

    repos = get_user_repositories(github_username, github_token)

    if repos:
        destination_folder = "../roles"
        clone_repositories(repos, destination_folder, repo_prefix)
        print("Repositories cloned successfully.")
    else:
        print("Failed to retrieve repositories.")
