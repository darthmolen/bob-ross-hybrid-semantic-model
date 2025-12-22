#!/bin/bash
# Install packages needed for Claude Code sessions
# This script runs automatically via SessionStart hook

# Check if gh is already installed
if command -v gh &> /dev/null; then
    echo "✓ gh CLI already installed: $(gh --version | head -1)"
else
    echo "Installing GitHub CLI (gh)..."

    # Add GitHub CLI repository
    if curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null; then
        sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

        # Install gh
        if sudo apt update -qq 2>/dev/null && sudo apt install gh -y -qq 2>/dev/null; then
            echo "✓ gh CLI installed: $(gh --version | head -1)"
        else
            echo "⚠ Failed to install gh via apt (network may be restricted)"
        fi
    else
        echo "⚠ Failed to fetch gh keyring (network may be restricted)"
    fi
fi

# Verify GH_TOKEN is set for authentication
if [ -n "$GH_TOKEN" ]; then
    echo "✓ GH_TOKEN is configured"
elif [ -n "$GITHUB_TOKEN" ]; then
    # Fall back to GITHUB_TOKEN if set
    export GH_TOKEN="$GITHUB_TOKEN"
    echo "✓ Using GITHUB_TOKEN for gh authentication"
else
    echo "⚠ No GH_TOKEN set - gh commands requiring auth will fail"
    echo "  Set GH_TOKEN in your Claude Code environment configuration"
fi
