import json

# Function to fetch data from GitHub API
def fetch_org_data():
    with open('org.json') as f:
        return json.load(f)

# Fetch organization data
org_data = fetch_org_data()

# Prepare README content
readme_content = f"""
# Welcome to Verma-Lab

## Hi there 👋

<!--

**Here are some ideas to get you started:**

🙋‍♀️ A short introduction - what is your organization all about?
🌈 Contribution guidelines - how can the community get involved?
👩‍💻 Useful resources - where can the community find your docs? Is there anything else the community should know?
🍿 Fun facts - what does your team eat for breakfast?
🧙 Remember, you can do mighty things with the power of [Markdown](https://docs.github.com/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
-->

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

## Contributors
- [Contributor 1](https://github.com/contributor1)
- [Contributor 2](https://github.com/contributor2)

## Latest Updates
- **July 2024**: Launched new features in Project 1.
- **June 2024**: Published a new research paper on AI.

## Contact Us
- **Email**: Anurag.Verma@Pennmedicine.upenn.edu
- **Twitter**:


## Stats
<div align="center">
  <p>
    <img src="https://github-readme-stats.vercel.app/api/top-langs?username=Verma-Lab&show_icons=true&locale=en&layout=compact&theme=blue-green" alt="Top Languages" />
  </p>
  <br/>
  <img alt="streak stats" height="200px" width="400px" src="https://github-readme-streak-stats.herokuapp.com/?user=Verma-Lab&theme=blue-green">
  <br/>
  <p>&nbsp;<img align="center" src="https://github-readme-stats.vercel.app/api?username=Verma-Lab&show_icons=true&theme=blue-green" alt="GitHub Stats" /></p>
</div>

"""

# Write the content to .github/profile/README.md
with open('.github/profile/README.md', 'w') as f:
    f.write(readme_content)
