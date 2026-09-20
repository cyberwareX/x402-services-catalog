#!/usr/bin/env python3
"""Regenerate README.md from agents.json (the machine catalog). Keeps the human/AI-readable repo
in lockstep with the live catalog at https://cyberwarex.com/agents.json. Run after re-snapshotting."""
import json, time, re

def _nodash(s):
    """Hard house rule: no em/en dashes anywhere outbound. Collapse to a plain hyphen."""
    if not isinstance(s, str):
        return s
    return re.sub("\\s*[\u2014\u2013]\\s*", " - ", s)

d = json.load(open("agents.json"))
org = d["org"]
pay = d["payment"]
L = []
L.append(f"# {org['name']} - x402 service catalog for AI agents")
L.append("")
L.append(f"> {org['summary']}")
L.append("")
L.append("Machine-readable, always-current versions (this repo mirrors them):")
L.append("")
L.append(f"- Agent capability manifest: {d['discovery']['directory'].replace('/.well-known/x402','')}/agents.json")
L.append(f"- x402 directory: {d['discovery']['directory']}")
L.append(f"- llms.txt: {d['discovery']['llms_txt']}")
L.append(f"- One hosted MCP endpoint for the whole suite: {d['discovery']['mcp']}")
L.append("")
L.append("## Payment (all services)")
L.append("")
L.append(f"- Protocol: **x402** ({pay['asset']} on {pay.get('network_name', pay['network'])})")
L.append("- **No account, no API key.** An unpaid call returns HTTP 402 with a price quote; sign the "
         "USDC EIP-3009 authorization and retry with the `X-PAYMENT` header. Gasless for the payer.")
L.append(f"- Contact: {org['contact']}")
L.append("")
L.append(f"## Services ({d['tool_count']})")
L.append("")
for t in d["tools"]:
    L.append(f"### {t['title']}")
    L.append("")
    L.append(t["description"])
    L.append("")
    uw = t.get("use_when") or []
    if uw:
        L.append("**Use when:** " + " ".join(str(x) for x in uw))
        L.append("")
    L.append(f"- Base URL: `{t['base_url']}`")
    for e in t.get("endpoints", []):
        price = "free" if not e.get("price_usdc") else f"${e['price_usdc']} USDC"
        L.append(f"- `{e.get('method','GET')} {e['path']}` ({price}) - {e.get('desc','')}")
    ft = (t.get("payment") or {}).get("free_trial")
    if ft:
        L.append(f"- Free trial: {ft.get('calls_per_ip_per_day')} call(s)/day per IP "
                 f"(header `{ft.get('header','X-Free-Trial: 1')}`)")
    if t.get("mcp"):
        L.append(f"- MCP: {t['mcp']}")
    if t.get("openapi"):
        L.append(f"- OpenAPI: {t['openapi']}")
    if t.get("example_request"):
        L.append(f"- Example: `{t['example_request']}`")
    L.append("")
L.append("---")
L.append(f"_Generated from `agents.json` on {time.strftime('%Y-%m-%d', time.gmtime())}. "
         "Source of truth: https://cyberwarex.com/agents.json_")
open("README.md", "w").write(_nodash("\n".join(L)) + "\n")
print("README.md written:", len(L), "lines")
