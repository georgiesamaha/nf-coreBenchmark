import requests
import re
from github import Github

# Use the Github API
with open("/home/562/gs5517/.github_token", 'r') as f:
    token = f.read().strip()
g = Github(token)

# Fetch all nf-core repositories
nfcore_repos = [repo.full_name for repo in g.get_organization("nf-core").get_repos()]

# Function to fetch the base.config file
def get_base_config(repo):
    url = f"https://raw.githubusercontent.com/{repo}/master/conf/base.config"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to parse the Nextflow lines from the config
def parse_nextflow_lines(config):
    lines = []
    pattern = r'(with(?:Label|Name):.+?\{(?:.|\n)+?\})'
    matches = re.findall(pattern, config, re.DOTALL)
    for match in matches:
        lines.append(match)
    return lines

# Function to extract the desired information from the line
def extract_info(line):
    line = re.sub(r"\s*with(?:Label|Name):\s*", "", line)  # Remove 'withLabel:' or 'withName:'
    line = re.sub(r"\{ check_max\(\s*", "", line)  # Remove "{ check_max( "
    line = re.sub(r"\s*,\s*'cpus'", "", line)  # Remove ", 'cpus'"
    line = re.sub(r"\s*\*\s*task.attempt", "", line)  # Remove "* task.attempt"
    line = re.sub(r"\s*,\s*'memory'", "", line)  # Remove ", 'memory'"
    line = re.sub(r"\s*,\s*'time'", "", line)  # Remove ", 'time'"
    line = re.sub(r"\s*\)\s*}", "", line)  # Remove "    ) }"
    line = line.strip()  # Remove leading/trailing whitespace
    return line

# File to write reformatted output
output_file = "config_parse.txt"

# Loop over all nf-core repositories and write reformatted output to the file
with open(output_file, 'w') as f:
    for repo in nfcore_repos:
        config = get_base_config(repo)
        if config is not None:
            lines = parse_nextflow_lines(config)
            if lines:
                for line in lines:
                    if "withLabel:error ignore" not in line and "withLabel:error_retry" not in line:
                        formatted_line = extract_info(line)
                        process = formatted_line.split()[0]  # Extract the process or label
                        info = ' '.join(formatted_line.split()[1:])  # Extract the time/cpus/memory information
                        f.write(f"{repo} {process} {info}\n")
