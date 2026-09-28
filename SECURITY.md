# Security

## Reporting a problem

Email contact@fastsocial.co with "Security" in the subject. Tell us what you found, how to
reproduce it, and what someone could do with it. Please don't test against other people's accounts
or data, and give us a reasonable chance to fix the problem before you share it publicly.

## What's in scope

- The remote MCP server at `https://data.fastsocial.co/mcp` and its sign-in
  (`https://data.fastsocial.co/oauth/...` and the consent page on fastsocial.co).
- The Instagram Data API at `https://data.fastsocial.co/v1/`.
- The manifests in this repository.

## What this plugin can reach

This plugin contains no code. It gives your client one server address, and every tool on that
server is read-only. See [What this plugin does and what data it sends](README.md#what-this-plugin-does-and-what-data-it-sends).
