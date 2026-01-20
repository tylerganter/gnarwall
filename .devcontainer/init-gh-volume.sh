#!/bin/bash
# GitHub CLI volume initialization
# Fixes ownership of the gh config directory (Docker volume mounts as root)

set -euo pipefail

chown -R node:node /home/node/.config/gh
