import subprocess
import os

def run_git_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f'Command Output: {result.stdout}')  # Providing feedback can be helpful
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f'Error executing command: {e.cmd}')
        print(f'Return code: {e.returncode}')
        print(f'Stdout: {e.stdout}')
        print(f'Error: {e.stderr}')
        return None

def get_current_branch(local_repo_path):
    # Get the current branch name
    result = run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=local_repo_path)
    return result.strip() if result is not None else None

def branch_exists(branch_name, local_repo_path):
    # Check if the branch exists locally
    branch_exists_result = run_git_command(['git', 'branch', '--list', branch_name], cwd=local_repo_path)
    # Check if the branch name is in the command output
    return branch_exists_result is not None and branch_name in branch_exists_result

def pull_branch(branch_name, local_repo_path):
    # Pull the latest changes from the remote branch
    try:
        result = subprocess.run(['git', 'pull', 'origin', branch_name], cwd=local_repo_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f'pull_result: {result.stdout}')
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f'Error pulling branch: {e.stderr}')
        if 'conflict' in e.stderr.lower():
            print('Resolve conflicts and try again.')
        else:
            print(f'Error: {e.stderr}')
        return None

def switch_and_pull_branch(branch_name, local_repo_path):
    # Switch to the specified branch and pull changes
    switch_result = run_git_command(['git', 'checkout', branch_name], cwd=local_repo_path)
    print(f'switch_result: {switch_result}')

    if switch_result is not None and 'error' not in switch_result.lower():
        pull_result = pull_branch(branch_name, local_repo_path)
        return pull_result
    else:
        print(f'Error switching to branch {branch_name}.')
        return None

def merge_branches(source_branch, target_branch, local_repo_path):
    try:
        # Checkout the target branch
        checkout_result = run_git_command(['git', 'checkout', target_branch], cwd=local_repo_path)
        print(f'checkout_result: {checkout_result}')

        # Merge the source branch into the target branch
        merge_result = run_git_command(['git', 'merge', source_branch], cwd=local_repo_path)
        print(f'merge_result: {merge_result}')

        return merge_result
    except subprocess.CalledProcessError as e:
        print(f'Error merging branches: {e.stderr}')
        if 'conflict' in e.stderr.lower():
            print('Resolve conflicts and try again.')
        else:
            print(f'Error: {e.stderr}')
        return None

def pull_or_fetch_branch(branch_name, local_repo_path):
    if os.path.isdir(local_repo_path):
        current_branch = get_current_branch(local_repo_path)
        if current_branch:
            print(f'Currently in branch: {current_branch}')
            if current_branch == branch_name:
                print(f'Branch {branch_name} is already checked out. Pulling it locally.')
                pull_branch(branch_name, local_repo_path)
            else:
                print(f'Branch {branch_name} does not match the current branch. Switching and pulling.')
                switch_and_pull_branch(branch_name, local_repo_path)
        else:
            print('Unable to determine the current branch.')
    else:
        print(f'Local repository path does not exist: {local_repo_path}')


