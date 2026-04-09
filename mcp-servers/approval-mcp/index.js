#!/usr/bin/env node

/**
 * Approval MCP Server
 * Provides human-in-the-loop approval workflow via MCP protocol
 * Handles approval requests for sensitive actions
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: '../../.env' });

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Vault paths
const VAULT_PATH = process.env.OBSIDIAN_VAULT_PATH ||
  path.join(__dirname, '../../AI_Employee_Vault');
const APPROVAL_FOLDER = path.join(VAULT_PATH, 'Needs_Approval');

// Create MCP server
const server = new Server(
  {
    name: 'approval-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Helper: Generate approval filename
function generateApprovalFilename(action) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
  const sanitized = action.replace(/[^a-zA-Z0-9]/g, '_').slice(0, 50);
  return `approval_${sanitized}_${timestamp}.md`;
}

// Helper: Check approval status
async function checkApprovalStatus(filename) {
  const approvalPath = path.join(APPROVAL_FOLDER, filename);

  try {
    const content = await fs.readFile(approvalPath, 'utf-8');

    if (content.includes('DECISION: APPROVED')) {
      return 'approved';
    } else if (content.includes('DECISION: REJECTED')) {
      return 'rejected';
    }
    return 'pending';
  } catch (error) {
    return 'not_found';
  }
}

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'request_approval',
        description: 'Create an approval request for a sensitive action',
        inputSchema: {
          type: 'object',
          properties: {
            action: {
              type: 'string',
              description: 'Description of the action requiring approval',
            },
            details: {
              type: 'string',
              description: 'Detailed information about the action',
            },
            priority: {
              type: 'string',
              description: 'Priority level (high, medium, low)',
              enum: ['high', 'medium', 'low'],
            },
            timeout_minutes: {
              type: 'number',
              description: 'Minutes to wait for approval (default: 60)',
            },
          },
          required: ['action', 'details'],
        },
      },
      {
        name: 'check_approval',
        description: 'Check the status of an approval request',
        inputSchema: {
          type: 'object',
          properties: {
            approval_id: {
              type: 'string',
              description: 'Approval request filename',
            },
          },
          required: ['approval_id'],
        },
      },
      {
        name: 'list_pending_approvals',
        description: 'List all pending approval requests',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'cancel_approval',
        description: 'Cancel a pending approval request',
        inputSchema: {
          type: 'object',
          properties: {
            approval_id: {
              type: 'string',
              description: 'Approval request filename to cancel',
            },
          },
          required: ['approval_id'],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'request_approval': {
        const { action, details, priority = 'medium', timeout_minutes = 60 } = args;

        const filename = generateApprovalFilename(action);
        const filePath = path.join(APPROVAL_FOLDER, filename);

        const content = `---
action: ${action}
created: ${new Date().toISOString()}
status: pending
priority: ${priority}
timeout_minutes: ${timeout_minutes}
---

# Approval Required

## Action
${action}

## Details
${details}

## Decision Required
Add your decision below and save this file:

DECISION: [PENDING]

Options:
- DECISION: APPROVED
- DECISION: REJECTED

---
Instructions:
1. Review the action and details above
2. Replace [PENDING] with your decision
3. Save this file
4. The system will detect your decision automatically
`;

        await fs.writeFile(filePath, content, 'utf-8');

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                approval_id: filename,
                action,
                status: 'pending',
                file_path: `Needs_Approval/${filename}`,
                timeout_minutes,
                created: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'check_approval': {
        const { approval_id } = args;

        const status = await checkApprovalStatus(approval_id);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                approval_id,
                status,
                checked_at: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'list_pending_approvals': {
        const files = await fs.readdir(APPROVAL_FOLDER);
        const mdFiles = files.filter(f => f.endsWith('.md'));

        const approvals = [];
        for (const file of mdFiles) {
          const status = await checkApprovalStatus(file);
          if (status === 'pending') {
            approvals.push({
              approval_id: file,
              status,
            });
          }
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                count: approvals.length,
                pending_approvals: approvals,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'cancel_approval': {
        const { approval_id } = args;

        const filePath = path.join(APPROVAL_FOLDER, approval_id);

        // Read current content
        const content = await fs.readFile(filePath, 'utf-8');

        // Update status to cancelled
        const updatedContent = content.replace(
          'DECISION: [PENDING]',
          'DECISION: CANCELLED'
        );

        await fs.writeFile(filePath, updatedContent, 'utf-8');

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                approval_id,
                status: 'cancelled',
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: false,
            error: error.message,
            tool: name,
          }, null, 2),
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Approval MCP server running on stdio');
  console.error(`Approval folder: ${APPROVAL_FOLDER}`);
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
