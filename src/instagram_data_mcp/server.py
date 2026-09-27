"""MCP server for the Instagram Data API (https://data.fastsocial.co).

Every tool is generated from the bundled openapi.json, so the server never drifts from the
API it wraps: one GET endpoint = one tool, its query parameters = the tool's input schema.
Read-only by construction; the API itself cannot log in, post, follow or like.

Auth: set IG_DATA_API_KEY in the MCP client's env. Free keys at
https://fastsocial.co/instagram-api
"""
import json
import os
import re
from importlib import resources

import httpx
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

BASE_URL = os.getenv("IG_DATA_API_BASE", "https://data.fastsocial.co").rstrip("/")
SIGNUP_URL = "https://fastsocial.co/instagram-api"
TIMEOUT = float(os.getenv("IG_DATA_API_TIMEOUT", "60"))


def _load_spec():
    return json.loads(resources.files(__package__).joinpath("openapi.json").read_text(encoding="utf-8"))


def _tool_name(op_id):
    # MCP tool names: letters, digits, underscore. Prefix keeps them distinct from other servers'.
    return "instagram_" + re.sub(r"[^a-z0-9]+", "_", op_id.lower()).strip("_")


def _clean(text):
    # Spec descriptions carry markdown bold for docs; plain text reads better to a model.
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text or "").strip()


def build_tools(spec):
    """Return {tool_name: (path, Tool)} for every GET operation in the spec."""
    tools = {}
    for path, methods in spec.get("paths", {}).items():
        op = methods.get("get")
        if not op:
            continue
        props, required = {}, []
        for p in op.get("parameters", []):
            if p.get("in") != "query":
                continue
            schema = dict(p.get("schema") or {"type": "string"})
            schema.pop("pattern", None)  # the API validates; client-side regex only adds false rejections
            if p.get("description"):
                schema["description"] = _clean(p["description"])
            if "example" in p:
                schema["examples"] = [p["example"]]
            props[p["name"]] = schema
            if p.get("required"):
                required.append(p["name"])
        name = _tool_name(op.get("operationId") or path.strip("/").split("/")[-1])
        desc = _clean(op.get("summary", "")) + ". " + _clean(op.get("description", ""))
        tools[name] = (path, types.Tool(
            name=name,
            description=desc.strip(),
            inputSchema={"type": "object", "properties": props, "required": required},
            annotations=types.ToolAnnotations(readOnlyHint=True, openWorldHint=True),
        ))
    return tools


def _error(msg):
    return [types.TextContent(type="text", text=json.dumps({"ok": False, "error": msg}))]


def create_server():
    spec = _load_spec()
    tools = build_tools(spec)

    async def list_tools(ctx, params):
        return types.ListToolsResult(tools=[t for _, t in tools.values()])

    async def call_tool(ctx, params):
        content = await _call(params.name, params.arguments)
        is_error = content[0].text.startswith('{"ok": false')
        return types.CallToolResult(content=content, isError=is_error)

    async def _call(name, arguments):
        if name not in tools:
            return _error("Unknown tool: %s" % name)
        key = os.getenv("IG_DATA_API_KEY", "").strip()
        if not key:
            return _error("IG_DATA_API_KEY is not set. Get a free key at %s and add it to this "
                          "server's env in your MCP client config." % SIGNUP_URL)
        path, _ = tools[name]
        params = {k: v for k, v in (arguments or {}).items() if v not in (None, "")}
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.get(BASE_URL + path, params=params,
                                     headers={"X-API-Key": key, "User-Agent": "instagram-data-mcp"})
        except httpx.HTTPError as e:
            return _error("Request failed: %s" % e)
        body = r.text
        credits = r.headers.get("X-Credits-Remaining")
        if credits is not None:
            try:
                payload = r.json()
                if isinstance(payload, dict):
                    payload.setdefault("meta", {})
                    if isinstance(payload["meta"], dict):
                        payload["meta"]["credits_remaining"] = credits
                    body = json.dumps(payload)
            except ValueError:
                pass
        if r.status_code >= 400:
            return _error("HTTP %s: %s" % (r.status_code, body[:500]))
        return [types.TextContent(type="text", text=body)]

    return Server(
        "instagram-data",
        version=__import__(__package__).__version__,
        title="Instagram Data",
        description="Read-only public Instagram data for AI agents: profiles, posts, reels, stories, "
                    "highlights, comments, likers, followers, hashtags, places, audio and search.",
        website_url=SIGNUP_URL,
        instructions="Read-only public Instagram data. Pass a username (with or without @) or a "
                     "post/reel URL. Each call spends API credits; meta.credits_remaining shows the balance.",
        on_list_tools=list_tools,
        on_call_tool=call_tool,
    )


async def _run():
    server = create_server()
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


def main():
    import anyio
    anyio.run(_run)


if __name__ == "__main__":
    main()
