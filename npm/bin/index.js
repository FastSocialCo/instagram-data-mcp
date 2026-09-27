#!/usr/bin/env node
// stdio <-> Streamable HTTP bridge for the Instagram Data API's remote MCP server.
// Reads newline-delimited JSON-RPC from stdin, POSTs each message to the remote endpoint with
// the user's key from IG_DATA_API_KEY, and writes the replies to stdout. No dependencies.
'use strict';

const URL_ = process.env.IG_DATA_API_MCP_URL || 'https://data.fastsocial.co/mcp';
const KEY = (process.env.IG_DATA_API_KEY || '').trim();
const TIMEOUT_MS = Number(process.env.IG_DATA_API_TIMEOUT || 60) * 1000;

function out(msg) { process.stdout.write(JSON.stringify(msg) + '\n'); }
function fail(id, message) { if (id !== undefined && id !== null) out({ jsonrpc: '2.0', id, error: { code: -32000, message } }); }

async function forward(raw) {
  let msg;
  try { msg = JSON.parse(raw); } catch { return out({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Parse error' } }); }
  const headers = { 'content-type': 'application/json', accept: 'application/json, text/event-stream', 'user-agent': 'instagram-data-mcp-npm' };
  if (KEY) headers['x-api-key'] = KEY;
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(URL_, { method: 'POST', headers, body: raw, signal: ctl.signal });
    if (r.status === 202) return;
    const text = await r.text();
    if (!text) return;
    if ((r.headers.get('content-type') || '').includes('text/event-stream')) {
      for (const line of text.split('\n')) if (line.startsWith('data:')) { try { out(JSON.parse(line.slice(5).trim())); } catch {} }
      return;
    }
    const body = JSON.parse(text);
    for (const m of Array.isArray(body) ? body : [body]) out(m);
  } catch (e) {
    fail(msg && msg.id, 'Could not reach ' + URL_ + ': ' + (e && e.message ? e.message : e));
  } finally {
    clearTimeout(t);
  }
}

if (!KEY) process.stderr.write('instagram-data-mcp: IG_DATA_API_KEY is not set. Tools will list, but calls need a key. Free keys: https://fastsocial.co/instagram-api\n');

let buf = '';
let chain = Promise.resolve();
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  buf += chunk;
  let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (line) chain = chain.then(() => forward(line));
  }
});
process.stdin.on('end', () => { chain.then(() => process.exit(0)); });
