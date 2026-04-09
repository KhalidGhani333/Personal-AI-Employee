#!/usr/bin/env node

/**
 * File Management MCP Server
 * Provides file operations for AI Employee Vault via MCP protocol
 * Handles moving, copying, and managing task files
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

// Vault base path
const VAULT_PATH = process.env.OBSIDIAN_VAULT_PATH ||
  path.join(__dirname, '../../AI_Employee_Vault');

// Valid folders
const VALID_FOLDERS = ['Inbox', 'Needs_Action', 'Needs_Approval', 'Done', 'Files'];

// Create MCP server
const server = new Server(
  {
    name: 'file-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Helper: Validate folder name
function validateFolder(folder) {
  if (!VALID_FOLDERS.includes(folder)) {
    throw new Error(`Invalid folder: ${folder}. Must be one of: ${VALID_FOLDERS.join(', ')}`);
  }
}

// Helper: Get full path
function getFullPath(folder, filename) {
  validateFolder(folder);
  return path.join(VAULT_PATH, folder, filename);
}

// Helper: Check if file exists
async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'move_task',
        description: 'Move a task file from one folder to another',
        inputSchema: {
          type: 'object',
          properties: {
            filename: {
              type: 'string',
              description: 'Name of the file to move (e.g., task.md)',
            },
            from_folder: {
              type: 'string',
              description: 'Source folder (Inbox, Needs_Action, Needs_Approval, Done, Files)',
            },
            to_folder: {
              type: 'string',
              description: 'Destination folder (Inbox, Needs_Action, Needs_Approval, Done, Files)',
            },
            rename: {
              type: 'string',
              description: 'Optional: New filename (if renaming)',
            },
          },
          required: ['filename', 'from_folder', 'to_folder'],
        },
      },
      {
        name: 'copy_task',
        description: 'Copy a task file from one folder to another',
        inputSchema: {
          type: 'object',
          properties: {
            filename: {
              type: 'string',
              description: 'Name of the file to copy',
            },
            from_folder: {
              type: 'string',
              description: 'Source folder',
            },
            to_folder: {
              type: 'string',
              description: 'Destination folder',
            },
            new_name: {
              type: 'string',
              description: 'Optional: New filename for the copy',
            },
          },
          required: ['filename', 'from_folder', 'to_folder'],
        },
      },
      {
        name: 'list_tasks',
        description: 'List all task files in a folder',
        inputSchema: {
          type: 'object',
          properties: {
            folder: {
              type: 'string',
              description: 'Folder to list (Inbox, Needs_Action, Needs_Approval, Done, Files)',
            },
            pattern: {
              type: 'string',
              description: 'Optional: Filter by filename pattern (e.g., "Plan_*")',
            },
          },
          required: ['folder'],
        },
      },
      {
        name: 'read_task',
        description: 'Read the contents of a task file',
        inputSchema: {
          type: 'object',
          properties: {
            filename: {
              type: 'string',
              description: 'Name of the file to read',
            },
            folder: {
              type: 'string',
              description: 'Folder containing the file',
            },
          },
          required: ['filename', 'folder'],
        },
      },
      {
        name: 'delete_task',
        description: 'Delete a task file (use with caution)',
        inputSchema: {
          type: 'object',
          properties: {
            filename: {
              type: 'string',
              description: 'Name of the file to delete',
            },
            folder: {
              type: 'string',
              description: 'Folder containing the file',
            },
          },
          required: ['filename', 'folder'],
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
      case 'move_task': {
        const { filename, from_folder, to_folder, rename } = args;

        const sourcePath = getFullPath(from_folder, filename);
        const destFilename = rename || filename;
        const destPath = getFullPath(to_folder, destFilename);

        // Check if source exists
        if (!(await fileExists(sourcePath))) {
          throw new Error(`File not found: ${filename} in ${from_folder}`);
        }

        // Check if destination already exists
        if (await fileExists(destPath)) {
          throw new Error(`File already exists: ${destFilename} in ${to_folder}`);
        }

        // Move file
        await fs.rename(sourcePath, destPath);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                action: 'move',
                from: `${from_folder}/${filename}`,
                to: `${to_folder}/${destFilename}`,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'copy_task': {
        const { filename, from_folder, to_folder, new_name } = args;

        const sourcePath = getFullPath(from_folder, filename);
        const destFilename = new_name || filename;
        const destPath = getFullPath(to_folder, destFilename);

        // Check if source exists
        if (!(await fileExists(sourcePath))) {
          throw new Error(`File not found: ${filename} in ${from_folder}`);
        }

        // Copy file
        await fs.copyFile(sourcePath, destPath);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                action: 'copy',
                from: `${from_folder}/${filename}`,
                to: `${to_folder}/${destFilename}`,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'list_tasks': {
        const { folder, pattern } = args;

        const folderPath = path.join(VAULT_PATH, folder);
        validateFolder(folder);

        const files = await fs.readdir(folderPath);
        let filteredFiles = files.filter(f => f.endsWith('.md'));

        if (pattern) {
          const regex = new RegExp(pattern.replace('*', '.*'));
          filteredFiles = filteredFiles.filter(f => regex.test(f));
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                folder,
                count: filteredFiles.length,
                files: filteredFiles,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'read_task': {
        const { filename, folder } = args;

        const filePath = getFullPath(folder, filename);

        if (!(await fileExists(filePath))) {
          throw new Error(`File not found: ${filename} in ${folder}`);
        }

        const content = await fs.readFile(filePath, 'utf-8');

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                filename,
                folder,
                content,
                size: content.length,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'delete_task': {
        const { filename, folder } = args;

        const filePath = getFullPath(folder, filename);

        if (!(await fileExists(filePath))) {
          throw new Error(`File not found: ${filename} in ${folder}`);
        }

        await fs.unlink(filePath);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                action: 'delete',
                file: `${folder}/${filename}`,
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
  console.error('File Management MCP server running on stdio');
  console.error(`Vault path: ${VAULT_PATH}`);
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
