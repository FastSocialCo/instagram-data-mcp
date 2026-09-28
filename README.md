# Instagram Data MCP server

Connect your AI assistant to FastSocial's Instagram Data API, and it can look up public Instagram
profiles, posts, reels, stories, highlights, comments, hashtags, places and audio. It only reads.
Nothing logs in to Instagram, and nothing can post, follow, like or send messages.

The server is remote. There is nothing to install or run: your assistant talks to

```
https://data.fastsocial.co/mcp
```

over Streamable HTTP. The first time it connects, a fastsocial.co page opens in your browser where
you sign in and click Allow.

This repository holds the plugin manifests (`plugin.json`, `mcp.json` and the copy Cursor reads in
`.cursor-plugin/`), the `server.json` that lists the server in the official MCP Registry as
`io.github.FastSocialCo/instagram-data-mcp`, and a LobeHub manifest. It contains no code that runs
on your machine. The server's code is not here.

## Install

### Cursor

Install the plugin from cursor.directory, or add the server to `.cursor/mcp.json` (one project)
or `~/.cursor/mcp.json` (all projects):

```json
{
  "mcpServers": {
    "instagram-data": {
      "url": "https://data.fastsocial.co/mcp"
    }
  }
}
```

Open Settings, then MCP, and connect. Cursor opens the FastSocial sign-in page.

### Claude Code

```bash
claude mcp add --transport http instagram-data https://data.fastsocial.co/mcp
```

Then run `/mcp` inside Claude Code, choose `instagram-data` and sign in.

### Claude app (web and desktop)

1. Open Settings, then Connectors, and add a custom connector.
2. Paste `https://data.fastsocial.co/mcp` as the server URL.
3. Leave the OAuth client ID and secret empty.
4. Connect, and sign in on the FastSocial page that opens.

### VS Code and other clients

Any client that speaks MCP over Streamable HTTP can connect with the server URL. In VS Code, add
this to `.vscode/mcp.json` and press Start:

```json
{
  "servers": {
    "instagram-data": {
      "type": "http",
      "url": "https://data.fastsocial.co/mcp"
    }
  }
}
```

## What this plugin does and what data it sends

### The plugin itself

The plugin is two JSON files that tell your client the server's address. It runs no code, has no
install scripts and stores nothing. Your client makes every request itself, straight to
`https://data.fastsocial.co/mcp` over HTTPS.

### What your client sends

- **The MCP handshake:** your client's name and version, and the protocol version it speaks.
- **Each tool call:** the tool's name and its arguments, which are the things you asked about: an
  Instagram username or user id, a post or reel link, a hashtag, search words, a location, audio or
  highlight id, and a paging cursor. The full list is in the table below.
- **Your sign-in token or API key,** in a request header. Never in the URL.
- The usual details of any web request, such as your IP address and your client's user agent.

Nothing else is sent. The server never sees your files, your editor or your conversation, only the
arguments your assistant puts into a tool call.

### What comes back

Public Instagram data as JSON, plus `meta.credits_remaining`. Photos and videos come back as links,
not files. Private accounts return a `private_account` error. Instagram account owners can opt out;
after that the API returns `451 opted_out` for their account.

### Read-only

Every tool reads. None changes anything on Instagram. The only thing a call changes is your own
credit balance for the month. The server marks every tool `readOnlyHint: true` and
`openWorldHint: true` in `tools/list`. There are no tools that write or delete.

### Signing in

The first time your client connects, the server replies that it needs sign-in and says where to
find out how. Your client then opens a page on fastsocial.co in your browser. There you:

1. enter your email and the code FastSocial emails you,
2. see which app is asking, and click Allow (or Deny).

If you don't have a plan yet, a Free plan is made for you when you click Allow. You never type a
password into your assistant, and the plugin never sees or stores your credentials. Your client
keeps the tokens it receives. An access token lasts an hour, and your client renews it with a
refresh token that lasts 30 days and changes every time it is used.

To cut off every app you've connected, sign in at https://fastsocial.co/cart/api/account and press
New key. Sign-ins tied to the old key stop working at once.

For client developers: discovery starts at
`https://data.fastsocial.co/.well-known/oauth-protected-resource/mcp`. The authorization server
supports OAuth 2.1 with PKCE (S256 only), dynamic client registration and token revocation, for
public clients.

### Using an API key instead

If your client can set a header but can't sign in, get a key at https://fastsocial.co/instagram-api
and send it on every request as `X-API-Key: YOUR_KEY` (or `Authorization: Bearer YOUR_KEY`). For
Claude Code:

```bash
claude mcp add --transport http instagram-data https://data.fastsocial.co/mcp --header "X-API-Key: YOUR_KEY"
```

Keep the key out of files you commit.

### Policies

- Privacy policy: https://fastsocial.co/privacy
- Terms: https://fastsocial.co/terms
- Use policy for the data (public data only, no tracking or harassing people, nothing about
  minors): https://fastsocial.co/instagram-api/docs
- Reporting a security problem: [SECURITY.md](SECURITY.md)

## The 27 tools

Each call costs credits from your monthly allowance. Failed calls cost nothing. Every tool is
read-only.

| Tool | What it does | Arguments | Credits |
|---|---|---|---|
| `instagram_profile` | Get an Instagram profile | `username` or `user_id` | 1 |
| `instagram_user_id` | Instagram username to user id | `username` or `user_id` | 1 |
| `instagram_username` | Instagram user id to username | `user_id` | 3 |
| `instagram_check` | Check if an Instagram handle exists and is public | `username` | 1 |
| `instagram_posts` | Get recent Instagram posts | `username` or `user_id`, `cursor` | 1 |
| `instagram_reels` | Get an account's Instagram reels | `username` or `user_id`, `cursor` | 1 |
| `instagram_tagged` | Get posts an account is tagged in | `username` or `user_id`, `cursor` | 1 |
| `instagram_post` | Get one Instagram post or reel | `url` or `shortcode` | 1 |
| `instagram_media` | Download URLs for a post, reel or carousel | `url` or `shortcode` | 1 |
| `instagram_comments` | Get comments on an Instagram post | `url` or `shortcode` | 3 |
| `instagram_comment_replies` | Get replies to an Instagram comment | `url` or `shortcode`, `comment_id`, `cursor` | 3 |
| `instagram_likers` | Get accounts that liked an Instagram post | `url` or `shortcode` | 3 |
| `instagram_insights` | Instagram engagement rate calculator | `username` or `user_id` | 2 |
| `instagram_followers` | Get an account's followers | `username` or `user_id`, `cursor` | 3 |
| `instagram_following` | Get accounts an account follows | `username` or `user_id`, `cursor` | 3 |
| `instagram_similar` | Find similar Instagram accounts | `username` or `user_id` | 1 |
| `instagram_stories` | View Instagram stories anonymously | `username` or `user_id` | 3 |
| `instagram_highlights` | Get Instagram story highlights | `username` or `user_id` | 3 |
| `instagram_highlight` | Get the items in one highlight | `id` | 3 |
| `instagram_search` | Search Instagram accounts, hashtags and places | `q` | 1 |
| `instagram_hashtag` | Get posts for an Instagram hashtag | `tag`, `cursor` | 1 |
| `instagram_place` | Get an Instagram location | `id` | 3 |
| `instagram_place_posts` | Get posts tagged at an Instagram location | `id`, `cursor` | 1 |
| `instagram_audio` | Get an Instagram audio track and the reels using it | `id` | 1 |
| `instagram_audio_search` | Search Instagram music and sounds | `q` | 3 |
| `instagram_reels_search` | Search Instagram reels by keyword | `q`, `cursor` | 3 |
| `instagram_usage` | Your credits used and left this month | none | 0 |

Full reference: https://fastsocial.co/instagram-api/docs

## Things to ask it

- "Compare the engagement rate of @nasa and @spacex."
- "Download every slide of this carousel: https://www.instagram.com/p/..."
- "Show me @natgeo's current stories and summarise them."
- "Find 10 accounts similar to @humansofny."

## Local version

If your client only runs local (stdio) servers, the same tools are on PyPI as
`instagram-data-mcp`. It is not part of this plugin. Its source is the
[`v0.1.4` tag of this repository](https://github.com/FastSocialCo/instagram-data-mcp/tree/v0.1.4).

## Links

- Instagram Data API: https://fastsocial.co/instagram-api
- Docs: https://fastsocial.co/instagram-api/docs
- OpenAPI spec: https://fastsocial.co/instagram-api/openapi.json
- MCP Registry entry: `io.github.FastSocialCo/instagram-data-mcp`

## License

MIT. See [LICENSE](LICENSE).
