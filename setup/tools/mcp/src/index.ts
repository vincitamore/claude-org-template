#!/usr/bin/env node
/**
 * org-viewer MCP Server
 *
 * Provides Claude Code integration for the org-viewer:
 * - Check if org-viewer is running
 * - Get URLs (local and Tailscale)
 * - Open specific documents
 * - Force index rebuild
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import { execSync } from 'child_process';
import * as os from 'os';

// ============================================================================
// Configuration
// ============================================================================

const DEFAULT_PORT = 3847;
const SERVER_URL = process.env.ORG_VIEWER_URL || `http://localhost:${DEFAULT_PORT}`;

// ============================================================================
// Helper Functions
// ============================================================================

async function fetchJson(url: string, options?: RequestInit): Promise<unknown> {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

function getTailscaleHostname(): string | null {
  try {
    // Try to get Tailscale hostname
    const result = execSync('tailscale status --json', { encoding: 'utf-8', timeout: 5000 });
    const status = JSON.parse(result);
    if (status.Self?.DNSName) {
      // DNSName includes trailing dot, remove it
      return status.Self.DNSName.replace(/\.$/, '');
    }
  } catch {
    // Tailscale not available or not connected
  }
  return null;
}

function getMachineHostname(): string {
  return os.hostname();
}

// ============================================================================
// Tool Definitions
// ============================================================================

const tools: Tool[] = [
  {
    name: 'org_viewer_status',
    description: 'Check if org-viewer server is running and get basic stats. Returns server health, document counts, and index status.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'org_viewer_url',
    description: 'Get the URL(s) for accessing org-viewer. Returns local URL and Tailscale URL if available.',
    inputSchema: {
      type: 'object',
      properties: {
        format: {
          type: 'string',
          enum: ['all', 'local', 'tailscale'],
          description: 'Which URL format to return (default: all)',
        },
      },
      required: [],
    },
  },
  {
    name: 'org_viewer_open',
    description: 'Get the URL to open a specific document in org-viewer. Returns the full URL path that can be opened in a browser.',
    inputSchema: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: 'Document path relative to org root (e.g., "tasks/my-task.md")',
        },
      },
      required: ['path'],
    },
  },
  {
    name: 'org_viewer_refresh',
    description: 'Force the org-viewer to rebuild its document index. Useful after bulk file operations.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'org_viewer_search',
    description: 'Search documents in org-viewer. Returns matching documents with paths and excerpts.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Search query (searches titles, content, and tags)',
        },
        type: {
          type: 'string',
          enum: ['task', 'knowledge', 'inbox', 'project', 'all'],
          description: 'Filter by document type (default: all)',
        },
        limit: {
          type: 'number',
          description: 'Maximum results to return (default: 20)',
        },
      },
      required: ['query'],
    },
  },
  {
    name: 'org_viewer_publish',
    description: 'Generate tag index pages from document frontmatter tags. Creates/updates files in tags/ directory for graph navigation.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'org_viewer_tag_stats',
    description: 'Get tag usage statistics - which tags are most used, orphan tags, etc.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
];

// ============================================================================
// Tool Handlers
// ============================================================================

async function handleOrgViewerStatus(): Promise<string> {
  try {
    const health = await fetchJson(`${SERVER_URL}/api/health`) as { status: string; timestamp: string };
    const status = await fetchJson(`${SERVER_URL}/api/status`) as {
      documents: {
        total: number;
        byType: Record<string, number>;
      };
      index: {
        lastUpdated: string;
      };
    };

    return JSON.stringify({
      running: true,
      health: health.status,
      documents: status.documents,
      lastIndexed: status.index?.lastUpdated,
      url: SERVER_URL,
    }, null, 2);
  } catch (error) {
    return JSON.stringify({
      running: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      url: SERVER_URL,
      hint: 'Start the server with: cd projects/org-viewer && pnpm dev:server',
    }, null, 2);
  }
}

async function handleOrgViewerUrl(format: string = 'all'): Promise<string> {
  const localUrl = SERVER_URL;
  const tailscaleHost = getTailscaleHostname();
  const machineHost = getMachineHostname();
  const port = DEFAULT_PORT;

  const urls: Record<string, string | null> = {
    local: localUrl,
    machine: `http://${machineHost}:${port}`,
    tailscale: tailscaleHost ? `http://${tailscaleHost}:${port}` : null,
  };

  if (format === 'local') {
    return urls.local!;
  } else if (format === 'tailscale') {
    return urls.tailscale || 'Tailscale not available';
  } else {
    return JSON.stringify({
      local: urls.local,
      machine: urls.machine,
      tailscale: urls.tailscale,
      note: urls.tailscale
        ? 'Use Tailscale URL to access from any device on your tailnet'
        : 'Install Tailscale for remote access',
    }, null, 2);
  }
}

async function handleOrgViewerOpen(docPath: string): Promise<string> {
  // Normalize path (remove .md extension, handle backslashes)
  const normalizedPath = docPath
    .replace(/\\/g, '/')
    .replace(/\.md$/, '');

  const localUrl = `${SERVER_URL}/#/doc/${encodeURIComponent(normalizedPath)}`;
  const tailscaleHost = getTailscaleHostname();
  const tailscaleUrl = tailscaleHost
    ? `http://${tailscaleHost}:${DEFAULT_PORT}/#/doc/${encodeURIComponent(normalizedPath)}`
    : null;

  return JSON.stringify({
    path: normalizedPath,
    urls: {
      local: localUrl,
      tailscale: tailscaleUrl,
    },
    note: 'Copy URL to browser or use system open command',
  }, null, 2);
}

async function handleOrgViewerRefresh(): Promise<string> {
  try {
    const result = await fetchJson(`${SERVER_URL}/api/status/reindex`, {
      method: 'POST',
    }) as { success: boolean; documents: number; duration: number };

    return JSON.stringify({
      success: true,
      documents: result.documents,
      duration: `${result.duration}ms`,
    }, null, 2);
  } catch (error) {
    return JSON.stringify({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    }, null, 2);
  }
}

async function handleOrgViewerSearch(
  query: string,
  type: string = 'all',
  limit: number = 20
): Promise<string> {
  try {
    const params = new URLSearchParams({ q: query });
    if (type !== 'all') {
      params.append('type', type);
    }
    params.append('limit', limit.toString());

    const results = await fetchJson(`${SERVER_URL}/api/search?${params}`) as Array<{
      path: string;
      title: string;
      type: string;
      score: number;
      excerpt?: string;
    }>;

    return JSON.stringify({
      query,
      count: results.length,
      results: results.map(r => ({
        path: r.path,
        title: r.title,
        type: r.type,
        score: Math.round(r.score * 100) / 100,
        excerpt: r.excerpt,
      })),
    }, null, 2);
  } catch (error) {
    return JSON.stringify({
      error: error instanceof Error ? error.message : 'Unknown error',
      hint: 'Is org-viewer running?',
    }, null, 2);
  }
}

async function handleOrgViewerPublish(): Promise<string> {
  try {
    const result = await fetchJson(`${SERVER_URL}/api/publish/tags`, {
      method: 'POST',
    }) as {
      success: boolean;
      duration: number;
      stats: {
        totalTags: number;
        generated: number;
        unchanged: number;
        removed: number;
      };
      generated: string[];
      removed: string[];
    };

    return JSON.stringify({
      success: true,
      duration: `${result.duration}ms`,
      stats: result.stats,
      generated: result.generated,
      removed: result.removed,
    }, null, 2);
  } catch (error) {
    return JSON.stringify({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      hint: 'Is org-viewer running?',
    }, null, 2);
  }
}

async function handleOrgViewerTagStats(): Promise<string> {
  try {
    const result = await fetchJson(`${SERVER_URL}/api/publish/tags/stats`) as {
      totalTags: number;
      totalUsages: number;
      tags: Array<{ tag: string; count: number }>;
    };

    return JSON.stringify({
      totalTags: result.totalTags,
      totalUsages: result.totalUsages,
      topTags: result.tags.slice(0, 20),
      orphanTags: result.tags.filter(t => t.count === 1).map(t => t.tag),
    }, null, 2);
  } catch (error) {
    return JSON.stringify({
      error: error instanceof Error ? error.message : 'Unknown error',
      hint: 'Is org-viewer running?',
    }, null, 2);
  }
}

// ============================================================================
// MCP Server Setup
// ============================================================================

const server = new Server(
  {
    name: 'org-viewer-mcp',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result: string;

    switch (name) {
      case 'org_viewer_status':
        result = await handleOrgViewerStatus();
        break;

      case 'org_viewer_url':
        result = await handleOrgViewerUrl((args as { format?: string })?.format);
        break;

      case 'org_viewer_open':
        result = await handleOrgViewerOpen((args as { path: string }).path);
        break;

      case 'org_viewer_refresh':
        result = await handleOrgViewerRefresh();
        break;

      case 'org_viewer_search':
        result = await handleOrgViewerSearch(
          (args as { query: string; type?: string; limit?: number }).query,
          (args as { type?: string }).type,
          (args as { limit?: number }).limit
        );
        break;

      case 'org_viewer_publish':
        result = await handleOrgViewerPublish();
        break;

      case 'org_viewer_tag_stats':
        result = await handleOrgViewerTagStats();
        break;

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [{ type: 'text', text: result }],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            error: error instanceof Error ? error.message : 'Unknown error',
          }),
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
  console.error('org-viewer MCP server running on stdio');
}

main().catch(console.error);
