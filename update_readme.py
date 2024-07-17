import os
import requests

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'Verma-Lab'
REPOS = ['.github']  # Add more repositories if needed

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_commit_data(repo_name):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{repo_name}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_contributors(repo_name):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{repo_name}/contributors"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

commit_tables = ""
all_contributors = set()

for repo in REPOS:
    commit_data = fetch_commit_data(repo)
    contributors = fetch_contributors(repo)
    all_contributors.update([contributor['login'] for contributor in contributors])
    
    # Generate commit history table
    commit_table = f"### {repo} Commits\n\n"
    commit_table += "| Committer | Commit Message | Date |\n"
    commit_table += "| --- | --- | --- |\n"
    for commit in commit_data[:5]:  # Get the latest 5 commits
        commit_message = commit['commit']['message']
        author = commit['commit']['author']['name']
        date = commit['commit']['author']['date']
        commit_table += f"| {author} | {commit_message} | {date} |\n"
    
    commit_tables += commit_table + "\n"

# Generate contributors list
contributors_list = "\n".join([f"- [{contributor}](https://github.com/{contributor})" for contributor in all_contributors])

# Prepare README content
readme_content = f"""
# Welcome to Verma-Lab

![Screenshot 2024-07-16 at 3 46 20 PM](https://github.com/user-attachments/assets/de609b6b-c700-4d76-9ec9-ccc8763291cd)

## About Us
We are a team of developers and researchers working on innovative projects in various fields including Bioinformatics and Human Genetics.

## Tools We Use
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black&style=flat)
![TensorFlow](https://img.shields.io/badge/-TensorFlow-FF6F00?logo=tensorflow&logoColor=white&style=flat)
![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat)
![Azure](https://img.shields.io/badge/-Azure-0078D4?logo=microsoft-azure&logoColor=white&style=flat)

## Key Projects

## Latest Commits
{commit_tables}

## Contributors
{contributors_list}

## Latest Updates
- **July 2024**: Launched new features in Project 1.
- **June 2024**: Published a new research paper on AI.

## Contact Us
- **Email**: contact@verma-lab.com
- **Twitter**: [@verma_lab](https://twitter.com/verma_lab)
"""

# Write the content to profile/README.md in the root directory
os.makedirs('profile', exist_ok=True)
with open('profile/README.md', 'w') as f:
    f.write(readme_content)
