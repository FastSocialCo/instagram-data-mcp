# Changelog

## 0.1.6
- Registry entry points at PyPI instagram-data-mcp 0.1.5, which adds the `instagram_top_accounts` tool (daily ranking of the 2,000 most-followed accounts). The remote server already had it.

## 0.1.5
- This repository now holds only the plugin manifests for the remote server. The local Python
  package is unchanged on PyPI; its source stays at tag v0.1.4. The npm stdio bridge, never
  published, is gone.
- README: what the plugin sends, how sign-in works, and a table of every tool.
- SECURITY.md, and a `.cursor-plugin/plugin.json` copy of the manifest.

## 0.1.4
- Sign in with OAuth: add the URL and approve in your browser, no key to paste.
- Agent Plugins manifest now points at the remote URL.
- npm stdio bridge (published once the npm token is set).

## 0.1.3
- Remote MCP server at https://data.fastsocial.co/mcp.

## 0.1.2
- Listed on the official MCP Registry.

## 0.1.0
- First release: 27 read-only tools.
