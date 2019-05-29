#!/usr/bin/env bash

# Give all install scripts execute permissions.
# run this in bin/install.sh
#chmod +x bin/install_scripts/*.sh
#bin/install_scripts/install_docker.sh
#exit 1

curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
exit 1
