import os
from . import constants
from .utilities import is_valid_string
from .reviewer import getInfoFromReviewer
from .author import authorFlow

def startReview():
    current_directory = os.getcwd()
    init_cfg_path = os.path.join(current_directory, "init.cfg")

    if os.path.isfile(init_cfg_path):
        print(f"Found init.cfg file in: {current_directory}")
        while True:
            role = input(constants.AUTHOR_OR_REVIEWER).strip().lower()
            if role == constants.AUTHOR_ROLE:
                authorFlow()
                break
            elif role == constants.REVIEWER_ROLE:
                getInfoFromReviewer()
                break
            elif role == constants.EXIT_COMMAND:
                print(constants.EXIT_PROGRAM)
                return
            else:
                print(constants.INVALID_ROLE)
       
    else:
         # Capture user details if the file doesn't exist.
        api_key = input(constants.ENTER_API_KEY).strip()
        source_branch = input(constants.ENTER_SOURCE_BRANCH).strip()
        local_repo_path = input(constants.ENTER_LOCAL_REPO_PATH).strip()

        # Check if both fields have non-zero length
        if is_valid_string(api_key) and is_valid_string(source_branch) and is_valid_string(local_repo_path):
            # Write details to init.cfg file
            with open(init_cfg_path, 'w') as file:
                file.write(f"API Key: {api_key}\n")
                file.write(f"Source Branch: {source_branch}\n")
                file.write(f"Local Repo Path: {local_repo_path}\n")
            print(constants.SAVED_SUCCESSFULLY)
        else:
            print(constants.FILE_NOT_CREATED)





if __name__ == "__main__":
    startReview()
    
