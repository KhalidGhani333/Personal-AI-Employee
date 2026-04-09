#!/bin/bash

# Setup Work-Zone Folder Structure
# Creates Cloud vs Local separation architecture

set -e

VAULT="AI_Employee_Vault"

echo "🏗️  Setting up Work-Zone Architecture..."
echo ""

# Create Needs_Action folders
echo "📁 Creating Needs_Action folders..."
mkdir -p "$VAULT/Needs_Action/email"
mkdir -p "$VAULT/Needs_Action/social"
mkdir -p "$VAULT/Needs_Action/whatsapp"
mkdir -p "$VAULT/Needs_Action/payments"

# Create Pending_Approval folders
echo "📁 Creating Pending_Approval folders..."
mkdir -p "$VAULT/Pending_Approval/email"
mkdir -p "$VAULT/Pending_Approval/social"
mkdir -p "$VAULT/Pending_Approval/payments"

# Create Approved folders
echo "📁 Creating Approved folders..."
mkdir -p "$VAULT/Approved/email"
mkdir -p "$VAULT/Approved/social"
mkdir -p "$VAULT/Approved/payments"

# Create In_Progress folders (not synced)
echo "📁 Creating In_Progress folders..."
mkdir -p "$VAULT/In_Progress/cloud"
mkdir -p "$VAULT/In_Progress/local"

# Create Done folders
echo "📁 Creating Done folders..."
mkdir -p "$VAULT/Done/email"
mkdir -p "$VAULT/Done/social"
mkdir -p "$VAULT/Done/whatsapp"
mkdir -p "$VAULT/Done/payments"

# Create Failed folders
echo "📁 Creating Failed folders..."
mkdir -p "$VAULT/Failed/cloud"
mkdir -p "$VAULT/Failed/local"

# Create .gitignore for In_Progress (temporary, not synced)
echo "🔒 Configuring In_Progress to not sync..."
cat > "$VAULT/In_Progress/.gitignore" << 'EOF'
# In_Progress folders contain temporary working state
# These should NOT be synced via Git
# Only the process that claimed the task should access it

*
!.gitignore
EOF

# Create README files for each zone
echo "📝 Creating zone documentation..."

cat > "$VAULT/Needs_Action/README.md" << 'EOF'
# Needs_Action

Tasks waiting to be processed.

## Folders

- **email/** - Cloud processes: incoming emails needing replies
- **social/** - Cloud processes: social media tasks
- **whatsapp/** - Local processes: WhatsApp messages (requires session)
- **payments/** - Local processes: payment requests (requires approval)

## Processing

- Cloud: Reads from email/ and social/
- Local: Reads from whatsapp/ and payments/
- Both use claim-by-move to In_Progress/
EOF

cat > "$VAULT/Pending_Approval/README.md" << 'EOF'
# Pending_Approval

Draft items created by cloud, waiting for human approval.

## Folders

- **email/** - Draft email replies
- **social/** - Draft social media posts
- **payments/** - Payment approval requests

## Workflow

1. Cloud writes draft files here
2. Human reviews in Obsidian
3. Human changes status: pending → approved/rejected
4. Local executor processes approved items
EOF

cat > "$VAULT/Approved/README.md" << 'EOF'
# Approved

Items approved by human, ready for execution.

## Folders

- **email/** - Approved email replies
- **social/** - Approved social posts
- **payments/** - Approved payments

## Processing

- Local executor moves approved items here
- Then moves to In_Progress/local/ for execution
- Finally archives to Done/
EOF

cat > "$VAULT/In_Progress/README.md" << 'EOF'
# In_Progress

Tasks currently being processed.

## Folders

- **cloud/** - Cloud is processing (drafting, analyzing)
- **local/** - Local is processing (sending, posting, executing)

## Important

- These folders are NOT synced via Git
- Only the claiming process should access files here
- Files are temporary working state
- Completed tasks move to Done/
- Failed tasks move to Failed/
EOF

cat > "$VAULT/Done/README.md" << 'EOF'
# Done

Completed tasks archive.

## Folders

- **email/** - Sent emails
- **social/** - Posted social media
- **whatsapp/** - Sent WhatsApp messages
- **payments/** - Executed payments

## Retention

- Files older than 30 days can be archived
- Use for audit trail and history
EOF

cat > "$VAULT/Failed/README.md" << 'EOF'
# Failed

Failed operations for review.

## Folders

- **cloud/** - Cloud processing failures
- **local/** - Local execution failures

## Review

- Check error logs
- Fix issues
- Manually retry or discard
EOF

echo ""
echo "✅ Work-Zone folder structure created!"
echo ""
echo "📊 Structure:"
echo "   Needs_Action/     - Tasks to process"
echo "   Pending_Approval/ - Drafts awaiting approval"
echo "   Approved/         - Ready for execution"
echo "   In_Progress/      - Currently processing (not synced)"
echo "   Done/             - Completed tasks"
echo "   Failed/           - Failed operations"
echo ""
echo "🔐 Security:"
echo "   ✅ In_Progress/ excluded from Git sync"
echo "   ✅ Claim-by-move prevents conflicts"
echo "   ✅ Single-writer rule for Dashboard"
echo ""
echo "📚 Next steps:"
echo "   1. Review WORKZONE_ARCHITECTURE.md"
echo "   2. Update cloud scripts to use new folders"
echo "   3. Update local scripts to use new folders"
echo "   4. Test workflow end-to-end"
echo ""
