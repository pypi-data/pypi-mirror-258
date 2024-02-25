
# Jira Git branch Namer

`jira-git-branch-namer` is a Python package designed to simplify the process of generating Git branch names based on Jira issue information.

## Features

- Converts Jira issue titles into Git branch names.
- Supports various Jira issue types such as features, issues, and hotfixes.
- Truncates and sanitizes branch names for compatibility with Git.
- Interactive command-line interface for easy use.

## Installation

```bash
pip install jira-git-branch-namer
```

## Usage

```bash
jira-git-branch-namer 
```

Example:

```bash
Select issue Type:
  1. feature
  2. issue
  3. hotfix
Enter jira issue title: Example Issue Title
Enter jira issue number: ABC-123
Git Branch Name:
  feature/ABC-123-example-issue-title
```

## Publish In PyPi
This package has been Publish in [PyPi](https://pypi.org/project/jira-git-branch-namer/0.1.1/)

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or contribute code on [GitHub](https://github.com/dev-scripts/jira-git-branch-namer).

## License

This project is licensed under the MIT License - see the [LICENSE](https://link-to-your-license-file) file for details.

---
Feel free to add more sections or customize it further based on the specifics of your package. The README serves as a valuable resource for users to understand your project, so make it informative and user-friendly.