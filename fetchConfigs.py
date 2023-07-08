import requests
import re

# The nf-core GitHub organization
org = "nf-core"

# Your GitHub personal access token
# Expects github token is saved to homedir and github_token file
with open('$HOME/.github_token', 'r') as file:
    token = file.read().replace('\n', '')

# The headers for the requests
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Get all the nf-core repositories from the GitHub API
res = requests.get(f"https://api.github.com/orgs/{org}/repos", headers=headers)
repos = res.json()

# Check if there was an error
if "message" in repos:
    print(f"Error fetching repositories: {repos['message']}")
    exit(1)

# A regex to match the resource requirements in the base.config file
pattern = re.compile(r'\s+cpus\s+=\s+{ check_max\((.+)\s*\*\s*task\.attempt, \'cpus\' \) }|\s+memory\s+=\s+{ check_max\((.+)\s*\*\s*task\.attempt, \'memory\' \) }|\s+time\s+=\s+{ check_max\((.+)\s*\*\s*task\.attempt, \'time\' \) }')

# A regex to match the label names
label_pattern = re.compile(r'withLabel:(process_single|process_low|process_medium|process_high|process_high_memory)')

# Create a list to store the results
results = []

# Go through each repo
for repo in repos:
    # The repo name
    repo_name = repo["name"]

    # Default branch
    default_branch = repo["default_branch"]

    print(f"Fetching base.config for {repo_name} from branch {default_branch}")

    # Try to get the base.config file from the conf directory in the default branch of the repo
    res = requests.get(f"https://raw.githubusercontent.com/{org}/{repo_name}/{default_branch}/conf/base.config", headers=headers)

    # If the request was successful
    if res.status_code == 200:
        # The contents of the base.config file
        config = res.text

        # Find all 'withLabel' sections in the config
        matches = label_pattern.findall(config)

        # For each 'withLabel' section
        for label in matches:
            # Try to find the resource requirements in the section
            matches = pattern.findall(config)

            # If there are matches
            if matches:
                # Extract the resources
                cpus = [re.sub(r'\s*\*\s*task\.attempt', '', match[0]) for match in matches if match[0]]
                memory = [re.sub(r'\s*\*\s*task\.attempt', '', match[1]) for match in matches if match[1]]
                time = [re.sub(r'\s*\*\s*task\.attempt', '', match[2]) for match in matches if match[2]]

                # Add the results to the list
                results.append([repo_name, default_branch, label, ", ".join(cpus), ", ".join(memory), ", ".join(time)])
    else:
        print(f"Error fetching base.config for {repo_name} from branch {default_branch}: {res.content}")

# Write the results to a tab-delimited file
output_file = "nf-core_pipeline_resources.txt"
with open(output_file, "w") as file:
    # Write the header
    file.write("Pipeline Name\tBranch\tLabel\tCPUs\tMemory\tTime\n")

    # Write the results
    for result in results:
        file.write("\t".join(result) + "\n")

print(f"Output written to {output_file}")
