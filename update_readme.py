import os
import requests

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'Verma-Lab'
REPO_NAME = '.github'

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_commit_data():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_contributors():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contributors"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

commit_data = fetch_commit_data()
contributors = fetch_contributors()

# Generate commit history
commit_history = ""
for commit in commit_data[:5]:  # Get the latest 5 commits
    commit_message = commit['commit']['message']
    author = commit['commit']['author']['name']
    date = commit['commit']['author']['date']
    commit_history += f"- {commit_message} by {author} on {date}\n"

# Generate contributors list
contributors_list = "\n".join([f"- [{contributor['login']}](https://github.com/{contributor['login']})" for contributor in contributors])

# Prepare README content
readme_content = f"""
## Hi there 👋

<!--

**Here are some ideas to get you started:**

🙋‍♀️ A short introduction - what is your organization all about?
🌈 Contribution guidelines - how can the community get involved?
👩‍💻 Useful resources - where can the community find your docs? Is there anything else the community should know?
🍿 Fun facts - what does your team eat for breakfast?
🧙 Remember, you can do mighty things with the power of [Markdown](https://docs.github.com/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
-->

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
### [Project 1](https://github.com/Verma-Lab/project-1)
A brief description of what Project 1 does.

### [Project 2](https://github.com/Verma-Lab/project-2)
A brief description of what Project 2 does.

## Latest Commits
{commit_history}

## Contributors
- [Contributor 1](https://github.com/contributor1)
- [Contributor 2](https://github.com/contributor2)

## Latest Updates
- **July 2024**: Launched new features in Project 1.
- **June 2024**: Published a new research paper on AI.

## Contact Us
- **Email**: Anurag.Verma@Pennmedicine.upenn.edu
- **Twitter**:

#

## Repository Badges : .github (Sample Repo, Public)
</br>
<div align="center">
  <img src="https://img.shields.io/github/stars/Verma-Lab/.github?style=social" alt="GitHub stars" />
  <img src="https://img.shields.io/github/forks/Verma-Lab/.github?style=social" alt="GitHub forks" />
  <img src="https://img.shields.io/github/issues/Verma-Lab/.github" alt="GitHub issues" />
  <img src="https://img.shields.io/github/issues-pr/Verma-Lab/.github" alt="GitHub pull requests" />
  <img src="https://img.shields.io/github/last-commit/Verma-Lab/.github" alt="GitHub last commit" />
  <img src="https://img.shields.io/github/contributors/Verma-Lab/.github" alt="GitHub contributors" />
</div>

"""

# Write the content to .github/profile/README.md
os.makedirs('.github/profile', exist_ok=True)
with open('.github/profile/README.md', 'w') as f:
    f.write(readme_content)
