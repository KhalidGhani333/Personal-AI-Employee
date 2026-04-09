#!/bin/bash

# Dashboard Lock Helper Functions
# Provides safe Dashboard.md updates with locking mechanism

DASHBOARD="AI_Employee_Vault/Dashboard.md"
LOCK_FILE="AI_Employee_Vault/.dashboard.lock"
LOCK_TIMEOUT=30  # seconds
MAX_WAIT=60      # seconds

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function: Acquire Dashboard lock
acquire_dashboard_lock() {
    local waited=0
    local process_name="${1:-unknown}"

    while [ -f "$LOCK_FILE" ]; do
        # Check if we've waited too long
        if [ $waited -ge $MAX_WAIT ]; then
            echo -e "${RED}ERROR: Lock timeout after ${MAX_WAIT}s${NC}" >&2
            echo -e "${YELLOW}Removing stale lock...${NC}" >&2
            rm -f "$LOCK_FILE"
            break
        fi

        # Check lock age
        if [ -f "$LOCK_FILE" ]; then
            local lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || stat -f %m "$LOCK_FILE" 2>/dev/null || echo 0)))

            if [ $lock_age -gt $LOCK_TIMEOUT ]; then
                echo -e "${YELLOW}WARNING: Removing stale lock (age: ${lock_age}s)${NC}" >&2
                rm -f "$LOCK_FILE"
                break
            fi
        fi

        # Wait and retry
        sleep 1
        waited=$((waited + 1))
    done

    # Create lock file with metadata
    cat > "$LOCK_FILE" << EOF
pid: $$
process: $process_name
timestamp: $(date +%s)
datetime: $(date '+%Y-%m-%d %H:%M:%S')
EOF

    return 0
}

# Function: Release Dashboard lock
release_dashboard_lock() {
    if [ -f "$LOCK_FILE" ]; then
        # Verify we own the lock
        local lock_pid=$(grep "^pid:" "$LOCK_FILE" 2>/dev/null | cut -d' ' -f2)
        if [ "$lock_pid" = "$$" ]; then
            rm -f "$LOCK_FILE"
        else
            echo -e "${YELLOW}WARNING: Lock owned by different process (PID: $lock_pid)${NC}" >&2
        fi
    fi
}

# Function: Check if Dashboard is locked
is_dashboard_locked() {
    if [ -f "$LOCK_FILE" ]; then
        local lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || stat -f %m "$LOCK_FILE" 2>/dev/null || echo 0)))

        if [ $lock_age -gt $LOCK_TIMEOUT ]; then
            # Stale lock
            return 1
        else
            # Valid lock
            return 0
        fi
    else
        # No lock
        return 1
    fi
}

# Function: Get lock info
get_lock_info() {
    if [ -f "$LOCK_FILE" ]; then
        cat "$LOCK_FILE"
    else
        echo "No lock file"
    fi
}

# Function: Update Dashboard section safely
update_dashboard_section() {
    local section="$1"
    local content="$2"
    local process_name="${3:-dashboard_update}"

    # Acquire lock
    if ! acquire_dashboard_lock "$process_name"; then
        echo -e "${RED}ERROR: Failed to acquire Dashboard lock${NC}" >&2
        return 1
    fi

    # Update Dashboard
    # Note: Implement your actual update logic here
    # This is a placeholder
    echo "Updating Dashboard section: $section"

    # Release lock
    release_dashboard_lock

    return 0
}

# Function: Append to Dashboard safely
append_to_dashboard() {
    local content="$1"
    local process_name="${2:-dashboard_append}"

    if ! acquire_dashboard_lock "$process_name"; then
        echo -e "${RED}ERROR: Failed to acquire Dashboard lock${NC}" >&2
        return 1
    fi

    # Append to Dashboard
    echo "$content" >> "$DASHBOARD"

    release_dashboard_lock
    return 0
}

# Function: Read Dashboard safely (no lock needed for reads)
read_dashboard() {
    if [ -f "$DASHBOARD" ]; then
        cat "$DASHBOARD"
    else
        echo "Dashboard not found"
        return 1
    fi
}

# Trap to ensure lock is always released on exit
trap release_dashboard_lock EXIT INT TERM

# Export functions for use in other scripts
export -f acquire_dashboard_lock
export -f release_dashboard_lock
export -f is_dashboard_locked
export -f get_lock_info
export -f update_dashboard_section
export -f append_to_dashboard
export -f read_dashboard
