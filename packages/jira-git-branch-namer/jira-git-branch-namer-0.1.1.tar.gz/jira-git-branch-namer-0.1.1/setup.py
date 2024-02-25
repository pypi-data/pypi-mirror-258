# jira_branch/setup.py
from setuptools import setup, find_packages

setup(
    name='jira-git-branch-namer',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jira-git-branch-namer=branch_namer.branch_naming:main',
        ],
    },
)
