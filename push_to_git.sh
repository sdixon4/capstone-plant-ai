#!/bin/bash

# Helper script to add, commit, and push changes to GitHub
echo "📦 Pushing updates to GitHub..."

# Default commit message
COMMIT_MSG=${1:-"Update notebook and simulation files"}

git add .
git commit -m "$COMMIT_MSG"
git push origin main

echo "✅ Push complete!"

