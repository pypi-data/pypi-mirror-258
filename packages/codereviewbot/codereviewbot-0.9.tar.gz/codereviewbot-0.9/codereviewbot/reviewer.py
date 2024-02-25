import os
from . import constants
from .reviewCode import reviewCode
from .utilities import is_valid_string
from .gitOperations import pull_or_fetch_branch,get_current_branch,merge_branches
from .read_config import read_config

def getInfoFromReviewer():
    # Get configuration details from read_config function
    api_key, source_branch_name, local_repo_path = read_config()

    # Now you can use these variables as needed
    print(f"API Key: {api_key}")
    print(f"Source Branch Name: {source_branch_name}")
    print(f"Local Repository Path: {local_repo_path}")

    while True:
        branch_name = input(constants.ENTER_THE_BRANCH_NAME_THAT_YOU_WANT_TO_REVIEW).strip()
        if is_valid_string(branch_name):
            break
        else:
            print(constants.INVALID_BRANCH_NAME)

    #the below methods are for pulling latest from remote of source branch and branch he wants to review
    pull_or_fetch_branch(source_branch_name, local_repo_path)
    pull_or_fetch_branch(branch_name,local_repo_path)

    #Now I will get the get the current branch if current branch is same as branch name entered for review
    # then I will merge source branch code into current branch (Downmerge)
    current_branch = get_current_branch(local_repo_path)
    if(current_branch == None):
        print('Error in fetching current branch')
    elif(current_branch == branch_name):
        print('Start merge')
        merge_branches(source_branch_name,branch_name,local_repo_path)
        print('------- Start Reviewing -------')
        reviewCode(branch_name, source_branch_name,local_repo_path)
    else:
        print('Resolve conflicts and then merge')
    
    
        
    

    
    
    
