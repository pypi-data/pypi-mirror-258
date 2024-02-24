def read_config(file_path='init.cfg'):
    api_key = None
    source_branch_name = None
    local_repo_path = None

    with open(file_path, 'r') as file:
        for line in file:
            if 'API Key:' in line:
                api_key = line.split('API Key:')[1].strip()
            elif 'Source Branch:' in line:
                source_branch_name = line.split('Source Branch:')[1].strip()
            elif 'Local Repo Path:' in line:
                local_repo_path = line.split('Local Repo Path:')[1].strip()

    return api_key, source_branch_name, local_repo_path