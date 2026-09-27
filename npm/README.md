# instagram-data-mcp

<!-- mcp-name: io.github.FastSocialCo/instagram-data-mcp -->

An MCP server for public Instagram data. It gives Claude, Cursor and any other MCP client
27 read-only tools: profiles, posts, reels, stories, highlights, comments, likers,
followers, hashtags, places, audio and search.

It wraps the [Instagram Data API](https://fastsocial.co/instagram-api). Nothing logs in to
Instagram, and nothing can post, follow or like. Public data only.

## Get a key

Sign up at https://fastsocial.co/instagram-api. There is a free plan.

## Connect (no install)

The server runs at `https://data.fastsocial.co/mcp` (Streamable HTTP). Send your key in the
`X-API-Key` header.

Claude Code:

```bash
claude mcp add --transport http instagram-data https://data.fastsocial.co/mcp --header "X-API-Key: your_key"
```

Cursor, Claude Desktop and other clients that take a remote server:

```json
{
  "mcpServers": {
    "instagram-data": {
      "url": "https://data.fastsocial.co/mcp",
      "headers": { "X-API-Key": "your_key" }
    }
  }
}
```

## Or run it locally

```json
{
  "mcpServers": {
    "instagram-data": {
      "command": "uvx",
      "args": ["instagram-data-mcp"],
      "env": { "IG_DATA_API_KEY": "your_key" }
    }
  }
}
```

No `uvx`? `pip install instagram-data-mcp` and use `"command": "instagram-data-mcp"` instead.

## Tools

| Tool | What it does |
|---|---|
| `instagram_profile` | Get an Instagram profile |
| `instagram_user_id` | Instagram username to user id |
| `instagram_username` | Instagram user id to username |
| `instagram_check` | Check if an Instagram handle exists and is public |
| `instagram_posts` | Get recent Instagram posts |
| `instagram_reels` | Get an account's Instagram reels |
| `instagram_tagged` | Get posts an account is tagged in |
| `instagram_post` | Get one Instagram post or reel |
| `instagram_media` | Download URLs for a post, reel or carousel |
| `instagram_comments` | Get comments on an Instagram post |
| `instagram_comment_replies` | Get replies to an Instagram comment |
| `instagram_likers` | Get accounts that liked an Instagram post |
| `instagram_insights` | Instagram engagement rate calculator |
| `instagram_followers` | Get an account's followers |
| `instagram_following` | Get accounts an account follows |
| `instagram_similar` | Find similar Instagram accounts |
| `instagram_stories` | View Instagram stories anonymously |
| `instagram_highlights` | Get Instagram story highlights |
| `instagram_highlight` | Get the items in one highlight |
| `instagram_search` | Search Instagram accounts, hashtags and places |
| `instagram_hashtag` | Get posts for an Instagram hashtag |
| `instagram_place` | Get an Instagram location |
| `instagram_place_posts` | Get posts tagged at an Instagram location |
| `instagram_audio` | Get an Instagram audio track and the reels using it |
| `instagram_audio_search` | Search Instagram music and sounds |
| `instagram_reels_search` | Search Instagram reels by keyword |
| `instagram_usage` | Your usage this month |

Each call costs API credits (stories and highlights cost 3, most others 1). Every response
includes `meta.credits_remaining`. Full reference: https://fastsocial.co/instagram-api/docs

## Things to ask it

- "Compare the engagement rate of @nasa and @spacex."
- "Download every slide of this carousel: https://www.instagram.com/p/..."
- "Show me @natgeo's current stories and summarise them."
- "Find 10 accounts similar to @humansofny."

## Settings

| Env var | Default | |
|---|---|---|
| `IG_DATA_API_KEY` | none | Required |
| `IG_DATA_API_BASE` | `https://data.fastsocial.co` | |
| `IG_DATA_API_TIMEOUT` | `60` | Seconds |

## License

MIT
