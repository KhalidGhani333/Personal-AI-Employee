#!/usr/bin/env node

/**
 * Social Media MCP Server
 * Provides social media posting capabilities via MCP protocol
 * Supports LinkedIn and Twitter (X) posting
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { chromium } from 'playwright';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: '../../.env' });

// Create MCP server
const server = new Server(
  {
    name: 'social-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Helper: Post to LinkedIn
async function postToLinkedIn(content, headless = true) {
  const browser = await chromium.launch({ headless });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate to LinkedIn
    await page.goto('https://www.linkedin.com/login');

    // Login
    await page.fill('input[name="session_key"]', process.env.LINKEDIN_EMAIL);
    await page.fill('input[name="session_password"]', process.env.LINKEDIN_PASSWORD);
    await page.click('button[type="submit"]');

    // Wait for feed to load
    await page.waitForSelector('[aria-label*="Start a post"]', { timeout: 10000 });

    // Click "Start a post"
    await page.click('[aria-label*="Start a post"]');

    // Wait for editor
    await page.waitForSelector('.ql-editor', { timeout: 5000 });

    // Type content
    await page.fill('.ql-editor', content);

    // Click Post button
    await page.click('button[aria-label*="Post"]');

    // Wait for confirmation
    await page.waitForTimeout(2000);

    return {
      success: true,
      platform: 'linkedin',
      content,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    throw new Error(`LinkedIn posting failed: ${error.message}`);
  } finally {
    await browser.close();
  }
}

// Helper: Post to Twitter
async function postToTwitter(content, headless = true) {
  const browser = await chromium.launch({ headless });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate to Twitter
    await page.goto('https://twitter.com/login');

    // Login
    await page.fill('input[name="text"]', process.env.TWITTER_USERNAME || process.env.TWITTER_EMAIL);
    await page.click('button:has-text("Next")');
    await page.waitForTimeout(1000);

    await page.fill('input[name="password"]', process.env.TWITTER_PASSWORD);
    await page.click('button[data-testid="LoginForm_Login_Button"]');

    // Wait for home feed
    await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });

    // Type tweet
    await page.fill('[data-testid="tweetTextarea_0"]', content);

    // Click Tweet button
    await page.click('[data-testid="tweetButtonInline"]');

    // Wait for confirmation
    await page.waitForTimeout(2000);

    return {
      success: true,
      platform: 'twitter',
      content,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    throw new Error(`Twitter posting failed: ${error.message}`);
  } finally {
    await browser.close();
  }
}

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'post_linkedin',
        description: 'Post content to LinkedIn',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Content to post on LinkedIn',
            },
            headless: {
              type: 'boolean',
              description: 'Run browser in headless mode (default: true)',
            },
          },
          required: ['content'],
        },
      },
      {
        name: 'post_twitter',
        description: 'Post a tweet to Twitter (X)',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Tweet content (max 280 characters)',
            },
            headless: {
              type: 'boolean',
              description: 'Run browser in headless mode (default: true)',
            },
          },
          required: ['content'],
        },
      },
      {
        name: 'post_multi_platform',
        description: 'Post the same content to multiple social platforms',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Content to post',
            },
            platforms: {
              type: 'array',
              items: {
                type: 'string',
                enum: ['linkedin', 'twitter'],
              },
              description: 'Platforms to post to (linkedin, twitter)',
            },
            headless: {
              type: 'boolean',
              description: 'Run browser in headless mode (default: true)',
            },
          },
          required: ['content', 'platforms'],
        },
      },
      {
        name: 'verify_social_credentials',
        description: 'Verify social media credentials are configured',
        inputSchema: {
          type: 'object',
          properties: {
            platform: {
              type: 'string',
              enum: ['linkedin', 'twitter', 'all'],
              description: 'Platform to verify (linkedin, twitter, or all)',
            },
          },
          required: ['platform'],
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
      case 'post_linkedin': {
        const { content, headless = true } = args;

        if (!process.env.LINKEDIN_EMAIL || !process.env.LINKEDIN_PASSWORD) {
          throw new Error('LinkedIn credentials not configured in .env file');
        }

        const result = await postToLinkedIn(content, headless);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'post_twitter': {
        const { content, headless = true } = args;

        if (!process.env.TWITTER_EMAIL || !process.env.TWITTER_PASSWORD) {
          throw new Error('Twitter credentials not configured in .env file');
        }

        if (content.length > 280) {
          throw new Error(`Tweet too long: ${content.length} characters (max 280)`);
        }

        const result = await postToTwitter(content, headless);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'post_multi_platform': {
        const { content, platforms, headless = true } = args;

        const results = [];

        for (const platform of platforms) {
          try {
            if (platform === 'linkedin') {
              const result = await postToLinkedIn(content, headless);
              results.push(result);
            } else if (platform === 'twitter') {
              if (content.length > 280) {
                results.push({
                  success: false,
                  platform: 'twitter',
                  error: `Content too long: ${content.length} characters (max 280)`,
                });
                continue;
              }
              const result = await postToTwitter(content, headless);
              results.push(result);
            }
          } catch (error) {
            results.push({
              success: false,
              platform,
              error: error.message,
            });
          }
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: results.every(r => r.success),
                results,
                timestamp: new Date().toISOString(),
              }, null, 2),
            },
          ],
        };
      }

      case 'verify_social_credentials': {
        const { platform } = args;

        const credentials = {
          linkedin: {
            configured: !!(process.env.LINKEDIN_EMAIL && process.env.LINKEDIN_PASSWORD),
            email: process.env.LINKEDIN_EMAIL ? '***' : null,
          },
          twitter: {
            configured: !!(process.env.TWITTER_EMAIL && process.env.TWITTER_PASSWORD),
            email: process.env.TWITTER_EMAIL ? '***' : null,
          },
        };

        if (platform === 'all') {
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  success: true,
                  credentials,
                  timestamp: new Date().toISOString(),
                }, null, 2),
              },
            ],
          };
        } else {
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  success: true,
                  platform,
                  configured: credentials[platform].configured,
                  timestamp: new Date().toISOString(),
                }, null, 2),
              },
            ],
          };
        }
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
  console.error('Social Media MCP server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
