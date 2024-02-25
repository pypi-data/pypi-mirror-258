import re

# ANSI escape codes for color formatting
GREEN = '\033[92m'
RESET = '\033[0m'

def jira_to_git_branch(jira_ticket_title, issue_type, jira_ticket_number):
    # Remove special characters and replace spaces with hyphens
    sanitized_title = ''.join(char if char.isalnum() or char in {' ', '-'} else ' ' for char in jira_ticket_title)
    sanitized_title = sanitized_title.replace(' ', '-').lower()

    # Replace consecutive hyphens with a single hyphen
    sanitized_title = re.sub('-+', '-', sanitized_title)

    # Truncate the branch name to a reasonable length (e.g., 200 characters)
    truncated_title = sanitized_title[:200]
    issue_type = get_jira_issue_type(issue_type)
    sanitized_jira_ticket_number = jira_ticket_number.replace(' ', '').upper()
    final_name = issue_type + '/' + sanitized_jira_ticket_number + '-' + truncated_title

    return final_name

def get_jira_issue_type(issue_type):
    try:
        issue_type = int(issue_type)
        issue_types = {
            1: 'feature',
            2: 'issue',
            3: 'hotfix',
        }

        return issue_types.get(issue_type, 'invalid issue type')
    except ValueError:
        return 'invalid issue type'

def main():
    while True:
        jira_ticket_issue_type = input("Select issue Type: \n 1. feature \n 2. issue \n 3. hotfix ")
        jira_ticket_title = input("Enter jira issue title: ")
        jira_ticket_number = input("Enter jira issue number: ")

        git_branch_name = jira_to_git_branch(jira_ticket_title, jira_ticket_issue_type, jira_ticket_number)
        if 'invalid issue type' in git_branch_name.lower():
            print("Invalid issue type. Please try again.")
        else:
            colored_branch_name = GREEN + git_branch_name + RESET
            print(f"Git Branch Name:\n{colored_branch_name}")

            break

if __name__ == '__main__':
    main()