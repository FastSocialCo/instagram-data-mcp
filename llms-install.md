# Installing the FastSocial Instagram Data MCP server (for AI agents such as Cline)

This is a hosted, read-only MCP server. Nothing needs to be cloned, built or installed.

- Endpoint: `https://data.fastsocial.co/mcp`
- Transport: Streamable HTTP
- Auth: an API key in the `X-API-Key` header, or OAuth sign-in if the client supports it

## Steps

1. Ask the user for their FastSocial Instagram Data API key. If they don't have one, they can create
   a free one (50 credits a month, no card) at https://fastsocial.co/instagram-api?ref=cline
2. Add this entry to the MCP settings file (for Cline: `cline_mcp_settings.json`), keeping any
   servers already in it:

```json
{
  "mcpServers": {
    "instagram-data": {
      "type": "streamableHttp",
      "url": "https://data.fastsocial.co/mcp",
      "headers": {
        "X-API-Key": "THE_USER_API_KEY"
      }
    }
  }
}
```

3. Reload the MCP servers. The server lists its tools on connect (for example `instagram_profile`,
   `instagram_posts`, `instagram_reels`, `instagram_stories`, `instagram_top_accounts`).
4. Check the connection with `instagram_usage` (free, shows the credits left) or
   `instagram_top_accounts` (free).

The key goes in the header only, never in the URL. Every call is read-only.
