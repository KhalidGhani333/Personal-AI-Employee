#!/usr/bin/env node

/**
 * Email MCP Server
 * Provides email sending capabilities via MCP protocol
 * Uses Gmail SMTP for sending emails
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: '../../.env' });

// Create email transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_ADDRESS,
    pass: process.env.EMAIL_PASSWORD,
  },
});

// Create MCP server
const server = new Server(
  {
    name: 'email-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'send_email',
        description: 'Send an email via Gmail SMTP',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address',
            },
            subject: {
              type: 'string',
              description: 'Email subject line',
            },
            body: {
              type: 'string',
              description: 'Email body content (plain text)',
            },
            cc: {
              type: 'string',
              description: 'CC email addresses (comma-separated)',
            },
            bcc: {
              type: 'string',
              description: 'BCC email addresses (comma-separated)',
            },
          },
          required: ['to', 'subject', 'body'],
        },
      },
      {
        name: 'send_email_html',
        description: 'Send an HTML email via Gmail SMTP',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address',
            },
            subject: {
              type: 'string',
              description: 'Email subject line',
            },
            html: {
              type: 'string',
              description: 'Email body content (HTML)',
            },
            cc: {
              type: 'string',
              description: 'CC email addresses (comma-separated)',
            },
          },
          required: ['to', 'subject', 'html'],
        },
      },
      {
        name: 'verify_email_config',
        description: 'Verify email configuration and test connection',
        inputSchema: {
          type: 'object',
          properties: {},
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
      case 'send_email': {
        const { to, subject, body, cc, bcc } = args;

        const mailOptions = {
          from: process.env.EMAIL_ADDRESS,
          to,
          subject,
          text: body,
          cc: cc || undefined,
          bcc: bcc || undefined,
        };

        const info = await transporter.sendMail(mailOptions);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                messageId: info.messageId,
                to,
                subject,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'send_email_html': {
        const { to, subject, html, cc } = args;

        const mailOptions = {
          from: process.env.EMAIL_ADDRESS,
          to,
          subject,
          html,
          cc: cc || undefined,
        };

        const info = await transporter.sendMail(mailOptions);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                messageId: info.messageId,
                to,
                subject,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'verify_email_config': {
        await transporter.verify();

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: true,
                message: 'Email configuration verified successfully',
                server: 'Gmail SMTP',
                from: process.env.EMAIL_ADDRESS,
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
  console.error('Email MCP server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
