#!/bin/bash
# Protect main and develop branches
# - main: PRs required, no deletions, no force push
# - develop: direct push allowed, no deletions, no force push
# Usage: ./protect-branches.sh owner/repo

set -e

REPO="${1:-}"

if [[ -z "$REPO" ]]; then
  echo "Usage: $0 owner/repo"
  echo "Example: $0 mabrax/my-project"
  exit 1
fi

echo "Setting up branch protection for $REPO..."

# Check if develop exists, create if not
if ! gh api "repos/$REPO/branches/develop" &>/dev/null; then
  echo "Creating develop branch from main..."
  DEFAULT_SHA=$(gh api "repos/$REPO/git/refs/heads/main" --jq '.object.sha')
  gh api "repos/$REPO/git/refs" -X POST -f ref="refs/heads/develop" -f sha="$DEFAULT_SHA"
fi

# Main: PRs required
read -r -d '' MAIN_RULES << 'EOF' || true
{
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "enforce_admins": true,
  "required_status_checks": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

# Develop: no PR required, just prevent deletion/force push
read -r -d '' DEVELOP_RULES << 'EOF' || true
{
  "required_pull_request_reviews": null,
  "enforce_admins": true,
  "required_status_checks": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

echo "Protecting main (PRs required)..."
echo "$MAIN_RULES" | gh api "repos/$REPO/branches/main/protection" -X PUT --input -

echo "Protecting develop (direct push allowed)..."
echo "$DEVELOP_RULES" | gh api "repos/$REPO/branches/develop/protection" -X PUT --input -

echo ""
echo "Done!"
echo "  main:    PRs required, no deletions, no force push"
echo "  develop: direct push OK, no deletions, no force push"
