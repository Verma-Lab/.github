import requests
import os

# GitHub API endpoint to fetch repositories
org_name = 'Verma-Lab'
url = f'https://api.github.com/orgs/{org_name}/repos'

# Fetch repositories data
response = requests.get(url)
repos = response.json()

# Prepare the content for README.md
readme_content = """
# Welcome to Verma-Lab

![Verma-Lab Logo](https://link-to-your-logo-image.png)

## About Us
We are a team of developers and researchers working on innovative projects in various fields including AI, ML, and data analysis.

## Tools We Use
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black&style=flat)
![TensorFlow](https://img.shields.io/badge/-TensorFlow-FF6F00?logo=tensorflow&logoColor=white&style=flat)
![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat)
![Azure](https://img.shields.io/badge/-Azure-0078D4?logo=microsoft-azure&logoColor=white&style=flat)

## Key Projects
"""

# Add each repository to the README content
for repo in repos:
    readme_content += f"### [{repo['name']}]({repo['html_url']})\n"
    readme_content += f"{repo['description']}\n\n"
    readme_content += f"Last pushed by: {repo['pushed_at']}\n\n"

# Add more sections as needed
readme_content += """
## Contributors
- [Contributor 1](https://github.com/contributor1)
- [Contributor 2](https://github.com/contributor2)

## Latest Updates
- **July 2024**: Launched new features in Project 1.
- **June 2024**: Published a new research paper on AI.

## Contact Us
- **Email**: contact@verma-lab.com
- **Twitter**: [@verma_lab](https://twitter.com/verma_lab)
"""

# Write the content to README.md
with open('README.md', 'w') as f:
    f.write(readme_content)
