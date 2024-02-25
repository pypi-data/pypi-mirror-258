from .read_config import read_config
from .gitOperations import pull_or_fetch_branch,get_current_branch,merge_branches
from .reviewCode import reviewCode

def authorFlow():
     # Get configuration details from read_config function
    api_key, source_branch_name, local_repo_path = read_config()

    #Get current branch
    current_branch = get_current_branch(local_repo_path)

    

    if(current_branch!=source_branch_name):
        merge_branches(source_branch_name,current_branch,local_repo_path)
        print('------- Start Reviewing -------')
        reviewCode(current_branch, source_branch_name,local_repo_path)
    else:
        print('Your source branch and current branch are same. Try again')
    
    
    