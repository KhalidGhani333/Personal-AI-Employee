#!/bin/bash

# Git Vault Sync Script
# Synchronizes AI_Employee_Vault between cloud VM and local machine
# Usage: ./sync.sh [pull|push|status]

set -e

# Configuration
VAULT_DIR="AI_Employee_Vault"
LOG_FILE="logs/git-sync.log"
LOCK_FILE=".git-sync-lock"
MAX_RETRIES=3
RETRY_DELAY=5

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    log "ERROR: $1"
    rm -f "$LOCK_FILE"
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✅ $1${NC}"
    log "SUCCESS: $1"
}

# Warning message
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    log "WARNING: $1"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    error_exit "Git is not installed. Please install git first."
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    error_exit "Not a git repository. Run 'git init' first."
fi

# Create lock file to prevent concurrent syncs
if [ -f "$LOCK_FILE" ]; then
    error_exit "Sync already in progress (lock file exists). If stuck, remove $LOCK_FILE"
fi
touch "$LOCK_FILE"

# Cleanup on exit
trap "rm -f $LOCK_FILE" EXIT

# Function: Check for uncommitted changes
check_uncommitted() {
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        return 1  # Has uncommitted changes
    fi
    return 0  # Clean
}

# Function: Auto-commit changes
auto_commit() {
    local commit_msg="$1"

    # Check if there are changes to commit
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        log "Auto-committing changes..."
        git add AI_Employee_Vault/ 2>/dev/null || true
        git add README.md SUMMARY.md COMPLETE_PROJECT_GUIDE.md 2>/dev/null || true

        if ! git diff-index --quiet HEAD -- 2>/dev/null; then
            git commit -m "$commit_msg" || error_exit "Failed to commit changes"
            success "Changes committed: $commit_msg"
        else
            log "No changes to commit"
        fi
    fi
}

# Function: Pull changes from remote
sync_pull() {
    log "Starting pull operation..."

    # Fetch latest changes
    log "Fetching from remote..."
    git fetch origin || error_exit "Failed to fetch from remote"

    # Check if there are uncommitted changes
    if ! check_uncommitted; then
        warning "Uncommitted changes detected. Auto-committing..."
        auto_commit "Auto-commit before pull ($(date '+%Y-%m-%d %H:%M:%S'))"
    fi

    # Pull with rebase to avoid merge commits
    log "Pulling changes with rebase..."
    if git pull --rebase origin main 2>&1 | tee -a "$LOG_FILE"; then
        success "Pull completed successfully"

        # Show what changed
        log "Recent changes:"
        git log --oneline -5 | tee -a "$LOG_FILE"
    else
        # Check if it's a rebase conflict
        if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
            error_exit "Rebase conflict detected. Run './sync.sh resolve' to handle conflicts."
        else
            error_exit "Pull failed. Check logs for details."
        fi
    fi
}

# Function: Push changes to remote
sync_push() {
    log "Starting push operation..."

    # Check if there are uncommitted changes
    if ! check_uncommitted; then
        warning "Uncommitted changes detected. Auto-committing..."
        auto_commit "Manual sync from local machine ($(date '+%Y-%m-%d %H:%M:%S'))"
    fi

    # Pull first to ensure we're up to date
    log "Pulling latest changes before push..."
    sync_pull

    # Push to remote
    log "Pushing to remote..."
    if git push origin main 2>&1 | tee -a "$LOG_FILE"; then
        success "Push completed successfully"
    else
        error_exit "Push failed. Check logs for details."
    fi
}

# Function: Show sync status
sync_status() {
    echo ""
    echo "📊 Git Sync Status"
    echo "=================="
    echo ""

    # Check git status
    echo "📁 Working Directory Status:"
    git status --short
    echo ""

    # Check remote status
    echo "🌐 Remote Status:"
    git fetch origin 2>/dev/null
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")
    BASE=$(git merge-base @ @{u} 2>/dev/null || echo "")

    if [ -z "$REMOTE" ]; then
        echo "⚠️  No remote branch configured"
    elif [ "$LOCAL" = "$REMOTE" ]; then
        echo "✅ Up to date with remote"
    elif [ "$LOCAL" = "$BASE" ]; then
        echo "⬇️  Behind remote (need to pull)"
    elif [ "$REMOTE" = "$BASE" ]; then
        echo "⬆️  Ahead of remote (need to push)"
    else
        echo "🔀 Diverged from remote (need to sync)"
    fi
    echo ""

    # Show recent commits
    echo "📝 Recent Commits (last 5):"
    git log --oneline -5
    echo ""

    # Show vault statistics
    echo "📊 Vault Statistics:"
    echo "   Inbox: $(ls -1 AI_Employee_Vault/Inbox/ 2>/dev/null | wc -l) files"
    echo "   Needs_Action: $(ls -1 AI_Employee_Vault/Needs_Action/ 2>/dev/null | wc -l) files"
    echo "   Needs_Approval: $(ls -1 AI_Employee_Vault/Needs_Approval/ 2>/dev/null | wc -l) files"
    echo "   Done: $(ls -1 AI_Employee_Vault/Done/ 2>/dev/null | wc -l) files"
    echo ""
}

# Function: Resolve conflicts
sync_resolve() {
    echo ""
    echo "🔧 Conflict Resolution Helper"
    echo "============================="
    echo ""

    # Check if we're in a rebase
    if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
        echo "📋 Conflicted files:"
        git diff --name-only --diff-filter=U
        echo ""
        echo "Options:"
        echo "  1. Manually resolve conflicts, then run: git add <files> && git rebase --continue"
        echo "  2. Accept remote version: git checkout --theirs <file> && git add <file>"
        echo "  3. Accept local version: git checkout --ours <file> && git add <file>"
        echo "  4. Abort rebase: git rebase --abort"
        echo ""
        echo "After resolving, run: ./sync.sh push"
    else
        echo "✅ No active conflicts detected"
    fi
    echo ""
}

# Function: Initialize git repository
sync_init() {
    log "Initializing git repository for vault sync..."

    # Check if already initialized
    if [ -d ".git" ]; then
        warning "Git repository already initialized"
        return
    fi

    # Initialize git
    git init || error_exit "Failed to initialize git repository"
    success "Git repository initialized"

    # Create initial commit
    log "Creating initial commit..."
    git add .gitignore README.md AI_Employee_Vault/ 2>/dev/null || true
    git commit -m "Initial commit - Personal AI Employee" || error_exit "Failed to create initial commit"
    success "Initial commit created"

    # Set main as default branch
    git branch -M main

    echo ""
    echo "✅ Git repository initialized!"
    echo ""
    echo "Next steps:"
    echo "  1. Create a GitHub/GitLab repository"
    echo "  2. Add remote: git remote add origin <your-repo-url>"
    echo "  3. Push: git push -u origin main"
    echo "  4. On cloud VM: git clone <your-repo-url>"
    echo "  5. Setup cron: crontab -e"
    echo "     Add: */2 * * * * cd /path/to/project && ./sync.sh pull >> logs/git-sync.log 2>&1"
    echo ""
}

# Main script logic
case "${1:-status}" in
    pull)
        log "=== PULL OPERATION STARTED ==="
        sync_pull
        log "=== PULL OPERATION COMPLETED ==="
        ;;
    push)
        log "=== PUSH OPERATION STARTED ==="
        sync_push
        log "=== PUSH OPERATION COMPLETED ==="
        ;;
    status)
        sync_status
        ;;
    resolve)
        sync_resolve
        ;;
    init)
        sync_init
        ;;
    *)
        echo "Usage: $0 {pull|push|status|resolve|init}"
        echo ""
        echo "Commands:"
        echo "  pull    - Pull changes from remote (for cloud VM)"
        echo "  push    - Push changes to remote (for local machine)"
        echo "  status  - Show sync status"
        echo "  resolve - Help resolve merge conflicts"
        echo "  init    - Initialize git repository"
        echo ""
        exit 1
        ;;
esac

exit 0
