# #!/bin/sh -x
#
# # A script to regenerate a list of roles and their CI status.
#
# # Print the header of the table.
# echo "|Role name|GitHub Action|GitLab CI|Version|"
# echo "|---------|-------------|---------|-------|"
#
# # Loop over the found roles.
# # find ~/Documents/github.com/buluma/ansible-role-* | awk 'BEGIN { FS="/" } ; { print $NF }' | while read -r rolename ; do
# find ~/Documents/GitHub/ansible-role-* | awk 'BEGIN { FS="/" } ; { print $NF }' | while read -r rolename ; do
#
#   # Find the short name, i.e. "httpd" instead of "ansible-role-httpd"
#   shortrolename=$(echo "${rolename}" | sed "s/^ansible-role//")
#
#   # Save the markdown per column in a variable, better readable loop.
#   galaxy="[${shortrolename}](https://galaxy.ansible.com/buluma/${shortrolename})"
#   github="[![github](https://github.com/buluma/${rolename}/workflows/Ansible%20Molecule/badge.svg)](https://github.com/buluma/${rolename}/actions)"
#   gitlab="[![gitlab](https://gitlab.com/buluma/${rolename}/badges/master/pipeline.svg)](https://gitlab.com/buluma/${rolename})"
#   version="[![version](https://img.shields.io/github/commits-since/buluma/${rolename}/latest.svg)](https://github.com/buluma/${rolename}/releases)"
#
#   # Print the line of one role.
#   echo "|${galaxy}|${github}|${gitlab}|${version}|"
#
# done

## V2
#!/bin/sh -x

# Output folder
output_folder=~/Documents/GitHub/role_status

# Create the output folder if it doesn't exist
mkdir -p "$output_folder"

# Loop over the found roles.
find ~/Documents/GitHub/ansible-role-* | awk 'BEGIN { FS="/" } ; { print $NF }' | while read -r rolename ; do

  # Find the short name, i.e. "httpd" instead of "ansible-role-httpd"
  shortrolename=$(echo "${rolename}" | sed "s/^ansible-role//")

  # Save the information in a JSON file
  json_file="${output_folder}/${shortrolename}_status.json"

  cat <<EOF > "$json_file"
{
  "role": "${shortrolename}",
  "galaxy": "https://galaxy.ansible.com/buluma/${shortrolename}",
  "github": "https://github.com/buluma/${rolename}/actions",
  "gitlab": "https://gitlab.com/buluma/${rolename}",
  "version": "https://github.com/buluma/${rolename}/releases"
}
EOF

done
