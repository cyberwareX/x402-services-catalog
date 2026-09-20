# CyberWareX - x402 service catalog for AI agents

> A suite of x402-native services built for autonomous AI agents. Every endpoint speaks x402: your agent hits it, gets a 402 price quote, settles in USDC on Base, and receives the result. No accounts, no API keys, no humans in the loop.

Machine-readable, always-current versions (this repo mirrors them):

- Agent capability manifest: https://cyberwarex.com/agents.json
- x402 directory: https://cyberwarex.com/.well-known/x402
- llms.txt: https://cyberwarex.com/llms.txt
- One hosted MCP endpoint for the whole suite: https://cyberwarex.com/mcp

## Payment (all services)

- Protocol: **x402** (USDC on Base)
- **No account, no API key.** An unpaid call returns HTTP 402 with a price quote; sign the USDC EIP-3009 authorization and retry with the `X-PAYMENT` header. Gasless for the payer.
- Contact: x402@cyberwarex.com

## Services (16)

### Agent Web Access

Give your agent reliable eyes on the live web - the one thing an LLM can't do natively. Fetches JavaScript-rendered pages as clean, LLM-ready markdown, extracts elements by CSS selector, and captures full-page screenshots or PDFs of any public URL.

**Use when:** Reach for it when your agent must read a page it was handed, scrape live data, screenshot a site for a report, or turn a URL into a PDF - any time the answer lives on a website the model can't see.

- Base URL: `https://web.cyberwarex.com`
- `GET /fetch` ($0.002 USDC) - Render a page to markdown/text/html
- `GET /extract` ($0.002 USDC) - Extract elements by CSS selector
- `GET /screenshot` ($0.005 USDC) - Full-page PNG screenshot
- `GET /pdf` ($0.005 USDC) - Render a page to PDF
- `GET /ocr` ($0.005 USDC) - OCR: extract text from an image URL (screenshot/scan/receipt/photo) via Tesseract; SSRF-guarded, no charge on empty
- MCP: Official MCP registry: io.github.CyberPunk11147/cyberwarex-web-access - tools: web_fetch, web_extract, web_screenshot, web_pdf (install via registry.modelcontextprotocol.io)
- OpenAPI: https://web.cyberwarex.com/openapi.json
- Example: `curl -i 'https://web.cyberwarex.com/fetch?url=https://example.com&format=markdown'`

### DeFi Safety Oracle

Answer 'is this token safe to trade?' before committing funds. Deterministic, evidence-carrying rug/honeypot risk assessment across 6 EVM chains (Base, BSC, Ethereum, Polygon, Arbitrum, Robinhood Chain): live buy/sell simulation, contract powers (upgradeable proxy, owner mint/pause/blacklist), plus a GoPlus/honeypot.is cross-check. Grade A-F + tradeable flag. Free trial: first 3 calls/day per IP with the 'X-Free-Trial: 1' header - no wallet needed to evaluate. Now with a privilege graph (who can upgrade/mint/pause) and dynamic-tax mutability detection. Deep /v1/risk/check runs an adversarial simulation matrix (buy->sell across trade sizes x caller wallets) to catch size- and address-gated honeypots a single probe misses.

**Use when:** Call it before any swap, token approval, or 'should I buy this' decision - it catches honeypots and hidden sell-taxes so your agent never buys a coin it can't sell.

- Base URL: `https://oracle.cyberwarex.com`
- `GET /contract` ($0.02 USDC) - Contract powers + ownership analysis
- `GET /honeypot` ($0.04 USDC) - Live buy/sell honeypot simulation
- `GET /token` ($0.06 USDC) - Full safety report (all of the above)
- `POST /screen` ($0.15 USDC) - Batch screen up to 25 tokens in one POST
- `GET /risk/explain` ($0.01 USDC) - Agent verdict: ALLOW/LIMIT/RECHECK/BLOCK + reason codes
- `POST /v1/risk/check` ($0.03 USDC) - Full multi-dimensional risk decomposition for agents
- `GET /verdict` ($0.02 USDC) - One-call launch screening: GREEN/CAUTION/BLOCK (allow/review/reject) + reasons, incl. deployer prior-scams & code-rugged-before. For launchpads: auto-reject rugs before listing. Cache-first (~$0 on repeats)
- `GET /deployer` ($0.01 USDC) - Deployer-wallet reputation from our verdict ledger: prior proven honeypot/scam tokens (dead launches excluded)
- `GET /template` ($0.01 USDC) - Contract-template reputation: honeypot/scam siblings sharing this bytecode fingerprint (fuzzy-matched)
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- MCP: Official MCP registry: io.github.CyberPunk11147/cyberwarex-defi-oracle - tools: token_safety, honeypot_check, contract_risk (install via registry.modelcontextprotocol.io)
- OpenAPI: https://oracle.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://oracle.cyberwarex.com/token?address=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&chain=base'`

### Voice-to-Text

Pay-per-message speech-to-text for agents that need to hear. Transcribes a voice message (up to 10s) for a flat $0.015 over x402; longer audio billed per 10-second block. Upload wav, mp3, m4a, ogg or webm as multipart form-data.

**Use when:** Use it whenever audio comes in - a voice note, a call recording, a spoken command - and your agent needs the words as text to act on.

- Base URL: `https://voice.cyberwarex.com`
- `POST /transcribe` ($0.015 USDC) - Voice message to text, billed per 10-second block
- MCP: Official MCP registry: io.github.CyberPunk11147/cyberwarex-voice-stt - tool: voice_transcribe (install via registry.modelcontextprotocol.io)
- OpenAPI: https://voice.cyberwarex.com/openapi.json
- Example: `curl -i -X POST -F 'audio=@message.wav' \
  https://voice.cyberwarex.com/transcribe`

### Onchain Query API

Pay-per-call EVM chain data for AI agents: wallet balances, token profiles with live DEX market data, spot prices, gas market, decoded transactions, and ENS - across Base, Ethereum, Arbitrum, Optimism, Polygon. No API keys, no node infra, no subscription: one x402 USDC micropayment per call.

**Use when:** Reach for it any time you need a wallet balance, token price, gas, an ENS name, or a tx receipt - no node to run, no RPC key to hold.

- Base URL: `https://chain.cyberwarex.com`
- `GET /block` ($0.001 USDC) - Latest block: number, timestamp, age, base fee, gas used/limit (chain-tip / liveness check)
- `GET /balance` ($0.001 USDC) - Native ETH/POL balance of any address with USD value
- `GET /erc20-balance` ($0.001 USDC) - ERC-20 balance (USDC by default, any token) with symbol + decimals
- `GET /wallet` ($0.003 USDC) - Wallet snapshot: native + USDC balance, tx count, contract-or-EOA, USD values
- `GET /token` ($0.004 USDC) - ERC-20 profile: on-chain metadata + live DEX price, liquidity, 24h volume
- `GET /price` ($0.002 USDC) - Spot USD price for a ticker, CoinGecko id, or token address
- `GET /gas` ($0.002 USDC) - Live gas market: base fee, priority-fee percentiles, estimated USD cost
- `GET /tx` ($0.003 USDC) - Transaction lookup + decode, including ERC-20 transfers
- `GET /ens` ($0.003 USDC) - ENS resolution both directions (name to address, address to name)
- `GET /derivatives` ($0.005 USDC) - Perp futures snapshot for a symbol (keyless Binance): funding rate + annualized, mark/index, open interest + USD, 24h stats, long/short ratio
- Free trial: 1 call(s)/day per IP (header `X-Free-Trial: 1`)
- MCP: Official MCP registry: io.github.CyberPunk11147/cyberwarex-chain-data - tools: chain_wallet/token/price/gas/tx/ens (install via registry.modelcontextprotocol.io)
- OpenAPI: https://chain.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://chain.cyberwarex.com/price?query=eth'`

### SEO Audit

On-page SEO audit of any live URL: title/meta/canonical/robots, Open Graph + Twitter cards, headings, image alts, favicon - a 0-100 score with actionable issues, parsed from the live page on every call.

**Use when:** Use it when an agent is auditing or improving a website - it scores real on-page SEO so the agent can tell a client exactly what to fix.

- Base URL: `https://seo.cyberwarex.com`
- `GET /audit` ($0.01 USDC) - Full on-page SEO audit with 0-100 score and issues
- `GET /trends` ($0.02 USDC) - Google Trends for a keyword: interest over time, peak, direction, top + rising related queries (6h cache)
- `GET /meta` (free) - Free structured OG/Twitter/favicon metadata preview
- Free trial: 1 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://seo.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://seo.cyberwarex.com/audit?url=https://example.com'`

### Agent Search

Keyless web search for AI agents: one metasearch query across major engines on a dedicated SearXNG instance, clean trimmed JSON (title/url/snippet/engine), up to 10 results. No accounts, no API keys, no subscription. Free trial: 3 calls/day with the 'X-Free-Trial: 1' header.

**Use when:** Call it whenever your agent needs fresh facts from the open web - one keyless query, clean JSON back, no search account to set up.

- Base URL: `https://search.cyberwarex.com`
- `GET /search` ($0.003 USDC) - Web search - q, category (general|news|images), lang, max_results<=10
- `GET /contents` ($0.002 USDC) - Read one web page as clean markdown/text (JS rendered), truncate with max_chars
- `GET /search-contents` ($0.006 USDC) - Web search with the page text of the top results already extracted (up to 5 pages, parallel)
- `GET /news` ($0.001 USDC) - Ranked news brief for any topic: corroboration + freshness scored headlines, 15-min cache, zero-LLM
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://search.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://search.cyberwarex.com/search?q=x402+protocol&max_results=3'`

### Email Validation

Keyless email validation for agents & apps: RFC syntax, MX/DNS deliverability, disposable-domain detection (8k+ list), role-account & free-provider flags, typo suggestions, 0-100 score. No SMTP callouts. Free trial: 3/day with 'X-Free-Trial: 1'.

**Use when:** Use it before sending to, signing up, or trusting an email address - flags typos, dead domains, and disposable throwaways so your agent doesn't waste a send.

- Base URL: `https://validate.cyberwarex.com`
- `GET /validate` ($0.005 USDC) - Validate one email - syntax, MX, disposable, role, score, verdict
- `POST /validate-batch` ($0.05 USDC) - Batch validate up to 100 emails for one flat price
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://validate.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://validate.cyberwarex.com/validate?email=test@gmail.com'`

### Video Intelligence

YouTube transcripts and metadata for AI agents: per-segment timed transcripts (manual or auto captions; json/text/srt) and rich video metadata (title, channel, duration, chapters, caption inventory). Never downloads media. Free trial: 1 call/day with the 'X-Free-Trial: 1' header.

**Use when:** Reach for it to summarize or fact-check a YouTube video - transcript and metadata as JSON, no media download.

- Base URL: `https://video.cyberwarex.com`
- `GET /transcript` ($0.003 USDC) - Timed transcript - url (required), lang (default en), format (json|text|srt)
- `GET /meta` ($0.001 USDC) - Video metadata - title, channel, duration, chapters, available captions
- Free trial: 1 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://video.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://video.cyberwarex.com/meta?url=https://www.youtube.com/watch?v=arj7oStGLkU'`

### x402 Uptime Monitor

Fleet-wide reliability data over the x402 rail: uptime percentage, average response time and check counts per endpoint over 1/7/30-day windows. Add endpoints, pull stats, no signup - one USDC micropayment per call.

**Use when:** Use it when an agent needs to know if an endpoint is up and how fast - pay-per-check monitoring with no dashboard to run.

- Base URL: `https://uptime.cyberwarex.com`
- `GET /stats` ($0.002 USDC) - Fleet-wide uptime/latency stats over 1, 7 and 30 day windows.
- `GET /endpoints/{name}/history` ($0.002 USDC) - Raw check history for one endpoint: every probe with timestamp, status code, response time and up/down verdict over a day window.
- `GET /endpoints/{name}/sla` ($0.002 USDC) - SLA report for one endpoint: uptime percentage, downtime periods, mean/p95/p99 latency and total checks.
- OpenAPI: https://uptime.cyberwarex.com/openapi.json
- Example: `curl -i 'https://uptime.cyberwarex.com/stats'`

### Transaction Simulator

Decode an unsigned transaction and know what it does BEFORE signing. Given a chain, to, value and calldata, it decodes the function and arguments, flags dangerous actions (unlimited token approvals, setApprovalForAll, ownership transfers, native-value drains), and runs a keyless eth_call preview reporting whether the transaction would succeed or revert. Works across Base, BSC, Ethereum, Polygon, Arbitrum and Optimism. Deterministic, read-only, no keys. Free trial: 3 calls/day per IP with the 'X-Free-Trial: 1' header. The essential pre-sign safety check for any trading or wallet agent.

**Use when:** Call it right before signing any transaction - preview exactly what it will do and flag risky actions so your agent doesn't sign a drainer.

- Base URL: `https://simulate.cyberwarex.com`
- `GET+POST /safe-to-sign` ($0.02 USDC) - Pre-sign Safety Firewall: one GREEN/REVIEW/BLOCK verdict fusing tx decode+sim, signature-drainer, address-risk, URL-phishing and token-safety. Call before signing anything.
- `GET /simulate` ($0.005 USDC) - Decode + risk flags + eth_call would-succeed/revert preview
- `GET /decode` ($0.002 USDC) - Calldata decode + risk flags (no simulation, cheaper)
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://simulate.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://simulate.cyberwarex.com/decode?data=0x095ea7b3...ffffffff'`

### Signature Decoder

Pay-per-call decoder for off-chain signature requests: turn an opaque EIP-712 typed-data request (eth_signTypedData_v4) or a personal_sign string into a human-readable summary plus security risk flags for the drainer patterns wallets miss - gasless unlimited token approvals (EIP-2612 Permit, DAI permit, Uniswap Permit2) and asset-transferring marketplace orders (Seaport). Keyless, deterministic, no network.

**Use when:** Use it before approving an off-chain signature (Permit, Permit2, Seaport) - it decodes what you're really authorizing and flags drainer patterns.

- Base URL: `https://sign.cyberwarex.com`
- `GET /decode` ($0.002 USDC) - Decode an EIP-712 typed-data or personal_sign request into a summary + security risk flags.
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://sign.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://sign.cyberwarex.com/decode?typed_data=<url-encoded EIP-712 JSON>'`

### Address Risk

Pay-per-call address-risk and sanctions screening for agents. /risk returns a 0-100 risk score and a BLOCK/REVIEW/ALLOW verdict composed from OFAC sanctions, a curated taint set (mixer/hack/scam), and CyberWareX's own DeFi Oracle scam/deployer ledger - a deployer-history signal no generic list has. /screen is the sanctions/taint-only compliance check. Deterministic, keyless, no LLM.

**Use when:** Call it before paying or interacting with an address - screens for OFAC sanctions and scam-taint so your agent doesn't touch dirty funds.

- Base URL: `https://sanctions.cyberwarex.com`
- `GET /risk` ($0.01 USDC) - Full address-risk score + BLOCK/REVIEW/ALLOW verdict from sanctions, taint, and our scam/deployer ledger.
- `GET /screen` ($0.005 USDC) - Sanctions + taint screen -> BLOCK/REVIEW/ALLOW
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://sanctions.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://sanctions.cyberwarex.com/screen?address=0x0000000000000000000000000000000000000001'`

### Contract ABI

Pay-per-call contract ABI fetcher for AI agents: get a verified contract's ABI and metadata (function/event signatures, name, compiler, proxy detection) by address, keylessly, from Sourcify. Block explorers gate the ABI behind an API key; this does not. Pairs with tx-sim (calldata) and sig-decoder (signatures). Base, Ethereum, Arbitrum, Optimism, Polygon, BSC, Avalanche.

**Use when:** Reach for it when your agent needs a contract's ABI to decode or call it - fetched by address, keyless, no explorer account.

- Base URL: `https://abi.cyberwarex.com`
- `GET /abi` ($0.003 USDC) - Verified ABI + function/event signatures + proxy detection for a contract address.
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://abi.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://abi.cyberwarex.com/abi?address=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2&chain=ethereum'`

### URL Safety

Pay-per-call URL / phishing safety check for AI agents: score a link from keyless deterministic heuristics (typosquat/homoglyph of a known brand, punycode/mixed-script hosts, credentials-in-URL, raw-IP hosts, suspicious TLDs, deep subdomains) plus a best-effort domain-age check via RDAP. Returns a 0-100 risk score + SAFE/SUSPICIOUS/DANGEROUS verdict + reasons. Pairs with the web/oracle tools.

**Use when:** Use it before opening or forwarding any link - scores phishing and typosquat risk so your agent (or its user) doesn't click a trap.

- Base URL: `https://safe.cyberwarex.com`
- `GET /check` ($0.003 USDC) - Phishing-risk score + SAFE/SUSPICIOUS/DANGEROUS verdict + reasons for a URL.
- `GET /domain` ($0.002 USDC) - WHOIS (registrar, age, expiry, nameservers) + live DNS (A/AAAA/MX/NS/TXT) for a domain, keyless
- `GET+POST /subscribe` (free) - Buy prepaid suite credit (pay usd=N, get N+10% credit as a cwx_ key). Use the key suite-wide via X-Subscription-Key.
- `GET /credits` (free) - Free: check a prepaid key balance (?key=cwx_...).
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://safe.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://safe.cyberwarex.com/check?url=https://coinbase.com.secure-login.xyz/verify'`

### SEC Company Data

Pay-per-call US company data from SEC EDGAR (keyless, public domain): resolve a ticker to a company profile, list recent filings (10-K/10-Q/8-K/Form 4) with direct document URLs, and pull key annual fundamentals (revenue, net income, assets, equity, EPS) from XBRL. No API key.

**Use when:** Use it for company research - a US company's profile, SEC filings, and fundamentals straight from EDGAR, keyless.

- Base URL: `https://stocks.cyberwarex.com`
- `GET+POST /company` ($0.002 USDC) - Company profile for a US ticker: name, CIK, SIC industry, exchanges, tickers, incorporation state
- `GET+POST /filings` ($0.004 USDC) - Recent SEC filings (10-K/10-Q/8-K/Form 4) with form, dates, accession and direct doc URL; filter by form
- `GET+POST /fundamentals` ($0.004 USDC) - Key annual XBRL fundamentals: revenue, net income, assets, liabilities, equity, cash, EPS, shares
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://stocks.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' 'https://stocks.cyberwarex.com/fundamentals?ticker=AAPL'`

### Weather

Pay-per-call global weather (keyless, open-meteo.com; met.no fallback): current conditions, hourly (168h) and daily (16d) forecast, and air quality (EU/US AQI, PM2.5, PM10, O3, NO2, UV), by lat+lon or place name (open-meteo geocoding). Temperature, feels-like, humidity, wind, pressure, cloud, precipitation + probability, sunrise/sunset, WMO condition. No API key.

**Use when:** Call it whenever a task depends on the weather or air quality: current conditions, a forecast, or AQI anywhere, by place name or lat/lon, keyless.

- Base URL: `https://weather.cyberwarex.com`
- `GET+POST /current` ($0.001 USDC) - Current weather: temp, feels-like, humidity, wind, pressure, cloud, precip, condition (lat+lon or place); air=1 embeds air quality
- `GET+POST /air` ($0.001 USDC) - Air quality: EU + US AQI with bands, PM2.5, PM10, O3, NO2, SO2, CO, dust, UV index
- `GET+POST /forecast` ($0.002 USDC) - Forecast: current + hourly (168h, from now) + daily (16d min/max, precip, wind, UV, sunrise/sunset), by lat+lon or place
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://weather.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' 'https://weather.cyberwarex.com/current?place=Los%20Angeles&air=1'`

---
_Generated from `agents.json` on 2026-09-20. Source of truth: https://cyberwarex.com/agents.json_
