#!/bin/bash
# Generates a GitHub App installation access token
# Used by gh-setup.sh and can be run standalone to refresh tokens

set -e

# Find the repo root to locate credentials in .devcontainer/.gh-app
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "/workspace")"
CREDENTIALS_DIR="$REPO_ROOT/.devcontainer/.gh-app"

# Check for required files
if [ ! -f "$CREDENTIALS_DIR/app-id" ] || \
   [ ! -f "$CREDENTIALS_DIR/installation-id" ] || \
   [ ! -f "$CREDENTIALS_DIR/private-key.pem" ]; then
    echo "Error: GitHub App credentials not found." >&2
    echo "Run 'gh-setup' first to configure your GitHub App." >&2
    exit 1
fi

APP_ID=$(cat "$CREDENTIALS_DIR/app-id")
INSTALLATION_ID=$(cat "$CREDENTIALS_DIR/installation-id")
PRIVATE_KEY="$CREDENTIALS_DIR/private-key.pem"

# Base64url encode (RFC 4648)
base64url() {
    openssl base64 -e -A | tr '+/' '-_' | tr -d '='
}

# Generate JWT for GitHub App authentication
generate_jwt() {
    local now=$(date +%s)
    local iat=$((now - 60))  # issued 60 seconds ago to account for clock drift
    local exp=$((now + 540)) # expires in 9 minutes (max is 10)

    # JWT Header
    local header='{"alg":"RS256","typ":"JWT"}'
    local header_base64=$(echo -n "$header" | base64url)

    # JWT Payload
    local payload="{\"iat\":${iat},\"exp\":${exp},\"iss\":\"${APP_ID}\"}"
    local payload_base64=$(echo -n "$payload" | base64url)

    # Sign with private key
    local unsigned="${header_base64}.${payload_base64}"
    local signature=$(echo -n "$unsigned" | openssl dgst -sha256 -sign "$PRIVATE_KEY" | base64url)

    echo "${unsigned}.${signature}"
}

# Generate JWT
JWT=$(generate_jwt)

# Request installation access token
RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $JWT" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/app/installations/${INSTALLATION_ID}/access_tokens")

# Extract token from response (handle optional whitespace in JSON)
TOKEN=$(echo "$RESPONSE" | grep -o '"token": *"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "Error: Failed to get installation token." >&2
    echo "Response: $RESPONSE" >&2
    exit 1
fi

echo "$TOKEN"
