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
import { CallToolRequestSchema, ListToolsRequestSchema, } from '@modelcontextprotocol/sdk/types.js';
import { execSync } from 'child_process';
import * as os from 'os';
import { existsSync, readFileSync, writeFileSync, readdirSync, mkdirSync, renameSync } from 'fs';
import { join, basename, relative } from 'path';
import matter from 'gray-matter';
// ============================================================================
// Configuration
// ============================================================================
const DEFAULT_PORT = 3847;
const SERVER_URL = process.env.ORG_VIEWER_URL || `http://localhost:${DEFAULT_PORT}`;
// Org system paths - get ORG_ROOT from environment or use cwd
const ORG_ROOT = process.env.ORG_ROOT || process.cwd();
const ORG_PATHS = {
    reminders: join(ORG_ROOT, 'reminders'),
    remindersCompleted: join(ORG_ROOT, 'reminders', 'completed'),
};
// ============================================================================
// Helper Functions
// ============================================================================
async function fetchJson(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
}
function getTailscaleHostname() {
    try {
        // Try to get Tailscale hostname
        const result = execSync('tailscale status --json', { encoding: 'utf-8', timeout: 5000 });
        const status = JSON.parse(result);
        if (status.Self?.DNSName) {
            // DNSName includes trailing dot, remove it
            return status.Self.DNSName.replace(/\.$/, '');
        }
    }
    catch {
        // Tailscale not available or not connected
    }
    return null;
}
function getMachineHostname() {
    return os.hostname();
}
function today() {
    return new Date().toISOString().split('T')[0];
}
function slugify(text) {
    return text
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');
}
function extractTitle(filename, content) {
    const h1Match = content.match(/^#\s+(.+)$/m);
    if (h1Match)
        return h1Match[1];
    return basename(filename, '.md')
        .replace(/-/g, ' ')
        .replace(/\b\w/g, (c) => c.toUpperCase());
}
function parseOrgDocument(filePath) {
    const content = readFileSync(filePath, 'utf-8');
    const { data, content: body } = matter(content);
    const relativePath = relative(ORG_ROOT, filePath).replace(/\\/g, '/');
    return {
        path: filePath,
        relativePath,
        frontmatter: data,
        content: body,
        title: data.title || extractTitle(filePath, body),
    };
}
function writeOrgDocument(filePath, frontmatter, content) {
    const output = matter.stringify(content, frontmatter);
    writeFileSync(filePath, output, 'utf-8');
}
function scanOrgDirectory(dir) {
    if (!existsSync(dir))
        return [];
    const docs = [];
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = join(dir, entry.name);
        if (entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'README.md') {
            try {
                docs.push(parseOrgDocument(fullPath));
            }
            catch {
                // Skip files that fail to parse
            }
        }
    }
    return docs;
}
// ============================================================================
// Tool Definitions
// ============================================================================
const tools = [
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
    // Reminder tools
    {
        name: 'org_reminder_list',
        description: 'List reminders, optionally filtered by status. Returns due times and repeat config.',
        inputSchema: {
            type: 'object',
            properties: {
                status: { type: 'string', enum: ['pending', 'snoozed', 'ongoing', 'completed', 'dismissed'], description: 'Filter by status' },
            },
            required: [],
        },
    },
    {
        name: 'org_reminder_create',
        description: 'Create a new reminder with due datetime. Use ISO format with time (e.g., 2026-02-06T09:00).',
        inputSchema: {
            type: 'object',
            properties: {
                title: { type: 'string', description: 'Reminder title' },
                remindAt: { type: 'string', description: 'Due datetime in ISO format (e.g., 2026-02-06T09:00)' },
                description: { type: 'string', description: 'Optional description' },
                repeat: { type: 'string', enum: ['daily', 'weekly', 'monthly', 'custom'], description: 'Repeat schedule (optional)' },
                repeatUntil: { type: 'string', description: 'End date for repeat (ISO date, optional)' },
                tags: { type: 'array', items: { type: 'string' }, description: 'Tags' },
            },
            required: ['title', 'remindAt'],
        },
    },
    {
        name: 'org_reminder_update',
        description: 'Update reminder due time, repeat config, or tags',
        inputSchema: {
            type: 'object',
            properties: {
                path: { type: 'string', description: 'Reminder path (relative)' },
                remindAt: { type: 'string', description: 'New due datetime (optional)' },
                repeat: { type: 'string', enum: ['daily', 'weekly', 'monthly', 'custom'], description: 'New repeat schedule (optional, null to remove)' },
                repeatUntil: { type: 'string', description: 'New repeat end date (optional)' },
                tags: { type: 'array', items: { type: 'string' }, description: 'Replace all tags' },
                addTags: { type: 'array', items: { type: 'string' }, description: 'Add these tags' },
                removeTags: { type: 'array', items: { type: 'string' }, description: 'Remove these tags' },
            },
            required: ['path'],
        },
    },
    {
        name: 'org_reminder_complete',
        description: 'Mark reminder as completed and move to reminders/completed/',
        inputSchema: {
            type: 'object',
            properties: { path: { type: 'string', description: 'Reminder path (relative)' } },
            required: ['path'],
        },
    },
    {
        name: 'org_reminder_dismiss',
        description: 'Dismiss reminder (skip/cancel) and move to reminders/completed/',
        inputSchema: {
            type: 'object',
            properties: { path: { type: 'string', description: 'Reminder path (relative)' } },
            required: ['path'],
        },
    },
    {
        name: 'org_reminder_snooze',
        description: 'Snooze reminder to a later time. Sets status=snoozed and snoozed-until datetime.',
        inputSchema: {
            type: 'object',
            properties: {
                path: { type: 'string', description: 'Reminder path (relative)' },
                until: { type: 'string', description: 'Snooze until datetime (ISO format, e.g., 2026-02-06T14:00)' },
            },
            required: ['path', 'until'],
        },
    },
];
// ============================================================================
// Tool Handlers
// ============================================================================
async function handleOrgViewerStatus() {
    try {
        const health = await fetchJson(`${SERVER_URL}/api/health`);
        const status = await fetchJson(`${SERVER_URL}/api/status`);
        return JSON.stringify({
            running: true,
            health: health.status,
            documents: status.documents,
            lastIndexed: status.index?.lastUpdated,
            url: SERVER_URL,
        }, null, 2);
    }
    catch (error) {
        return JSON.stringify({
            running: false,
            error: error instanceof Error ? error.message : 'Unknown error',
            url: SERVER_URL,
            hint: 'Start the server with: cd projects/org-viewer && pnpm dev:server',
        }, null, 2);
    }
}
async function handleOrgViewerUrl(format = 'all') {
    const localUrl = SERVER_URL;
    const tailscaleHost = getTailscaleHostname();
    const machineHost = getMachineHostname();
    const port = DEFAULT_PORT;
    const urls = {
        local: localUrl,
        machine: `http://${machineHost}:${port}`,
        tailscale: tailscaleHost ? `http://${tailscaleHost}:${port}` : null,
    };
    if (format === 'local') {
        return urls.local;
    }
    else if (format === 'tailscale') {
        return urls.tailscale || 'Tailscale not available';
    }
    else {
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
async function handleOrgViewerOpen(docPath) {
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
async function handleOrgViewerRefresh() {
    try {
        const result = await fetchJson(`${SERVER_URL}/api/status/reindex`, {
            method: 'POST',
        });
        return JSON.stringify({
            success: true,
            documents: result.documents,
            duration: `${result.duration}ms`,
        }, null, 2);
    }
    catch (error) {
        return JSON.stringify({
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
        }, null, 2);
    }
}
async function handleOrgViewerSearch(query, type = 'all', limit = 20) {
    try {
        const params = new URLSearchParams({ q: query });
        if (type !== 'all') {
            params.append('type', type);
        }
        params.append('limit', limit.toString());
        const results = await fetchJson(`${SERVER_URL}/api/search?${params}`);
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
    }
    catch (error) {
        return JSON.stringify({
            error: error instanceof Error ? error.message : 'Unknown error',
            hint: 'Is org-viewer running?',
        }, null, 2);
    }
}
async function handleOrgViewerPublish() {
    try {
        const result = await fetchJson(`${SERVER_URL}/api/publish/tags`, {
            method: 'POST',
        });
        return JSON.stringify({
            success: true,
            duration: `${result.duration}ms`,
            stats: result.stats,
            generated: result.generated,
            removed: result.removed,
        }, null, 2);
    }
    catch (error) {
        return JSON.stringify({
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
            hint: 'Is org-viewer running?',
        }, null, 2);
    }
}
async function handleOrgViewerTagStats() {
    try {
        const result = await fetchJson(`${SERVER_URL}/api/publish/tags/stats`);
        return JSON.stringify({
            totalTags: result.totalTags,
            totalUsages: result.totalUsages,
            topTags: result.tags.slice(0, 20),
            orphanTags: result.tags.filter(t => t.count === 1).map(t => t.tag),
        }, null, 2);
    }
    catch (error) {
        return JSON.stringify({
            error: error instanceof Error ? error.message : 'Unknown error',
            hint: 'Is org-viewer running?',
        }, null, 2);
    }
}
// ============================================================================
// Reminder Handlers
// ============================================================================
async function handleOrgReminderList(args) {
    let reminders = [];
    if (args.status === 'completed' || args.status === 'dismissed') {
        reminders = scanOrgDirectory(ORG_PATHS.remindersCompleted);
        if (args.status) {
            reminders = reminders.filter((r) => r.frontmatter.status === args.status);
        }
    }
    else {
        reminders = scanOrgDirectory(ORG_PATHS.reminders);
        if (args.status) {
            reminders = reminders.filter((r) => r.frontmatter.status === args.status);
        }
    }
    reminders = reminders.filter((r) => r.frontmatter.type === 'reminder');
    // Sort by remind-at
    reminders.sort((a, b) => {
        const aTime = String(a.frontmatter['remind-at'] || '');
        const bTime = String(b.frontmatter['remind-at'] || '');
        return aTime.localeCompare(bTime);
    });
    return JSON.stringify({
        count: reminders.length,
        reminders: reminders.map((r) => ({
            path: r.relativePath,
            title: r.title,
            status: r.frontmatter.status,
            remindAt: r.frontmatter['remind-at'],
            repeat: r.frontmatter.repeat,
            snoozedUntil: r.frontmatter['snoozed-until'],
            tags: r.frontmatter.tags || [],
        })),
    }, null, 2);
}
async function handleOrgReminderCreate(args) {
    const slug = slugify(args.title);
    const filename = `${slug}.md`;
    const filePath = join(ORG_PATHS.reminders, filename);
    if (existsSync(filePath)) {
        throw new Error(`Reminder already exists: ${filename}`);
    }
    if (!existsSync(ORG_PATHS.reminders)) {
        mkdirSync(ORG_PATHS.reminders, { recursive: true });
    }
    const frontmatter = {
        type: 'reminder',
        status: args.repeat ? 'ongoing' : 'pending',
        created: today(),
        'remind-at': args.remindAt,
        repeat: args.repeat || null,
        'repeat-until': args.repeatUntil || null,
        'snoozed-until': null,
        completed: null,
        tags: args.tags || [],
    };
    const content = `# ${args.title}\n\n${args.description || ''}\n`;
    writeOrgDocument(filePath, frontmatter, content);
    return JSON.stringify({
        success: true,
        path: relative(ORG_ROOT, filePath).replace(/\\/g, '/'),
        message: `Created reminder: ${args.title}`,
    }, null, 2);
}
async function handleOrgReminderUpdate(args) {
    const filePath = join(ORG_ROOT, args.path);
    if (!existsSync(filePath)) {
        throw new Error(`Reminder not found: ${args.path}`);
    }
    const doc = parseOrgDocument(filePath);
    if (args.remindAt) {
        doc.frontmatter['remind-at'] = args.remindAt;
    }
    if (args.repeat !== undefined) {
        doc.frontmatter.repeat = args.repeat;
        // Update status if repeat changes
        if (args.repeat && doc.frontmatter.status === 'pending') {
            doc.frontmatter.status = 'ongoing';
        }
    }
    if (args.repeatUntil !== undefined) {
        doc.frontmatter['repeat-until'] = args.repeatUntil;
    }
    if (args.tags) {
        doc.frontmatter.tags = args.tags;
    }
    if (args.addTags) {
        const currentTags = doc.frontmatter.tags || [];
        doc.frontmatter.tags = [...new Set([...currentTags, ...args.addTags])];
    }
    if (args.removeTags) {
        doc.frontmatter.tags = (doc.frontmatter.tags || []).filter((t) => !args.removeTags.includes(t));
    }
    writeOrgDocument(filePath, doc.frontmatter, doc.content);
    return JSON.stringify({
        success: true,
        path: args.path,
        message: `Updated reminder: ${doc.title}`,
        frontmatter: doc.frontmatter,
    }, null, 2);
}
async function handleOrgReminderComplete(docPath) {
    const filePath = join(ORG_ROOT, docPath);
    if (!existsSync(filePath)) {
        throw new Error(`Reminder not found: ${docPath}`);
    }
    const doc = parseOrgDocument(filePath);
    doc.frontmatter.status = 'completed';
    doc.frontmatter.completed = today();
    writeOrgDocument(filePath, doc.frontmatter, doc.content);
    const completedPath = join(ORG_PATHS.remindersCompleted, basename(filePath));
    if (!existsSync(ORG_PATHS.remindersCompleted)) {
        mkdirSync(ORG_PATHS.remindersCompleted, { recursive: true });
    }
    renameSync(filePath, completedPath);
    return JSON.stringify({
        success: true,
        oldPath: docPath,
        newPath: relative(ORG_ROOT, completedPath).replace(/\\/g, '/'),
        message: `Completed reminder: ${doc.title}`,
    }, null, 2);
}
async function handleOrgReminderDismiss(docPath) {
    const filePath = join(ORG_ROOT, docPath);
    if (!existsSync(filePath)) {
        throw new Error(`Reminder not found: ${docPath}`);
    }
    const doc = parseOrgDocument(filePath);
    doc.frontmatter.status = 'dismissed';
    doc.frontmatter.completed = today();
    writeOrgDocument(filePath, doc.frontmatter, doc.content);
    const completedPath = join(ORG_PATHS.remindersCompleted, basename(filePath));
    if (!existsSync(ORG_PATHS.remindersCompleted)) {
        mkdirSync(ORG_PATHS.remindersCompleted, { recursive: true });
    }
    renameSync(filePath, completedPath);
    return JSON.stringify({
        success: true,
        oldPath: docPath,
        newPath: relative(ORG_ROOT, completedPath).replace(/\\/g, '/'),
        message: `Dismissed reminder: ${doc.title}`,
    }, null, 2);
}
async function handleOrgReminderSnooze(args) {
    const filePath = join(ORG_ROOT, args.path);
    if (!existsSync(filePath)) {
        throw new Error(`Reminder not found: ${args.path}`);
    }
    const doc = parseOrgDocument(filePath);
    doc.frontmatter.status = 'snoozed';
    doc.frontmatter['snoozed-until'] = args.until;
    writeOrgDocument(filePath, doc.frontmatter, doc.content);
    return JSON.stringify({
        success: true,
        path: args.path,
        message: `Snoozed reminder until ${args.until}`,
        snoozedUntil: args.until,
    }, null, 2);
}
// ============================================================================
// MCP Server Setup
// ============================================================================
const server = new Server({
    name: 'org-viewer-mcp',
    version: '0.1.0',
}, {
    capabilities: {
        tools: {},
    },
});
// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools };
});
// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    try {
        let result;
        switch (name) {
            case 'org_viewer_status':
                result = await handleOrgViewerStatus();
                break;
            case 'org_viewer_url':
                result = await handleOrgViewerUrl(args?.format);
                break;
            case 'org_viewer_open':
                result = await handleOrgViewerOpen(args.path);
                break;
            case 'org_viewer_refresh':
                result = await handleOrgViewerRefresh();
                break;
            case 'org_viewer_search':
                result = await handleOrgViewerSearch(args.query, args.type, args.limit);
                break;
            case 'org_viewer_publish':
                result = await handleOrgViewerPublish();
                break;
            case 'org_viewer_tag_stats':
                result = await handleOrgViewerTagStats();
                break;
            // Reminder tools
            case 'org_reminder_list':
                result = await handleOrgReminderList(args);
                break;
            case 'org_reminder_create':
                result = await handleOrgReminderCreate(args);
                break;
            case 'org_reminder_update':
                result = await handleOrgReminderUpdate(args);
                break;
            case 'org_reminder_complete':
                result = await handleOrgReminderComplete(args.path);
                break;
            case 'org_reminder_dismiss':
                result = await handleOrgReminderDismiss(args.path);
                break;
            case 'org_reminder_snooze':
                result = await handleOrgReminderSnooze(args);
                break;
            default:
                throw new Error(`Unknown tool: ${name}`);
        }
        return {
            content: [{ type: 'text', text: result }],
        };
    }
    catch (error) {
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
