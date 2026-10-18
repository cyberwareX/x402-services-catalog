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

## Services (9)

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

Answer 'is this token safe to trade?' before committing funds. Deterministic, evidence-carrying rug/honeypot risk assessment across 6 EVM chains (Base, BSC, Ethereum, Polygon, Arbitrum, Robinhood Chain): live buy/sell simulation, contract powers (upgradeable proxy, owner mint/pause/blacklist), plus a GoPlus/honeypot.is cross-check. Grade A-F + tradeable flag. Free trial: first 3 calls/day per IP with the 'X-Free-Trial: 1' header - no wallet needed to evaluate. Now with a privilege graph (who can upgrade/mint/pause) and dynamic-tax mutability detection. Deep /v1/risk/check runs an adversarial simulation matrix (buy->sell across trade sizes x caller wallets) to catch size- and address-gated honeypots a single probe misses. New: a Crypto Identity Graph (/v1/identity/*) answers "who is behind this wallet or token" - age, real X account, creator history, and impersonation/rug signals built from 130k+ tokens we've graded ourselves. New: Crowd Check (/v1/holders/*) - is the crowd real? Snipers, launch bundles, dev selling, bot farms funded from one source and fake airdrop holder counts, on Base, Ethereum, Robinhood Chain and Solana. Free quote, $0.10 quick check, $1 full scan.

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
- `GET /v1/identity/wallet` ($0.02 USDC) - Who is behind a wallet: age, ENS, linked X account, deployer history
- `GET /v1/identity/x` ($0.01 USDC) - X/Twitter account profile: age, followers, verified status, trust signals
- `GET /v1/identity/token` ($0.05 USDC) - Who is behind a token: market, socials, creator wallet, impersonation/rug signals
- `GET /v1/identity/quick` ($0.001 USDC) - Cheapest identity taster: feed an address or handle, get a one-line trust verdict
- `GET /v1/holders/quote` (free) - Crowd Check free quote: params chain (base|ethereum|robinhood|solana) and token. Returns quote_id, the two options (quick $0.10, full $1) and a teaser (holders, dust, real). If status is computing, call again with params id=<quote_id>
- `GET /v1/holders/quick` ($0.1 USDC) - Crowd Check quick check ($0.10): instant risk score 0-100 with reasons - snipers, launch bundles, dev holding and whether the dev sold, dev-fed insiders, padded holder count, top-10 share, whether the creator can pull the pool (liquidity lock), risky trading hooks, creator rug record. Param quote=<quote_id>
- `GET /v1/holders/scan` ($1.0 USDC) - Crowd Check full scan ($1): is the crowd real? Top 300 real holders profiled (wallet age, real funder traced through routers), funder clusters, fresh wallets, snipers, launch bundles, dev and insider holdings, risk score 0-100, verdict organic/mixed/farmed. Param quote=<quote_id>. Returns a job; call again with the same quote for the result (never charged twice)
- `GET /v1/holders/creator` ($0.02 USDC) - Crowd Check creator check ($0.02): who is behind a token - creator wallet, its funding chain (up to 8 hops) and that chain's record of earlier tokens, wallet age and throwaway-wallet signals, plus any registered name and X account linked to the creator (claimed or proven both ways). Serial launchers flagged. params quote (from /v1/holders/quote).
- `GET /v1/holders/pool` ($0.02 USDC) - Crowd Check pool safety ($0.02): can the liquidity be pulled (burned / wallet / a lock service with the real locked share and unlock date) and what a Uniswap v4 hook may do on every trade (take a cut, set any fee, block sells), platform hook or the creator's own. params quote.
- `GET /v1/holders/verdict` ($0.03 USDC) - Crowd Check instant verdict for trading bots ($0.03): ok / caution / avoid with risk score, top reasons and flags (liquidity pullable, serial launcher, v4 hook, bundled share). params chain, token. Returns 202, not charged, until ready.
- `GET /v1/paper/backtest` ($0.05 USDC) - Paper test ($0.05): what would have happened if you had followed a rule on every new token we found. params preset (avoid_farms | locked_pools_only | clean_checks | small_pools_only | farms_only | everything) or filters, horizon 1|6|24, chain, bankroll. Returns trades, win rate with 95% interval, average and median return, drawdown, crash rate, and the same numbers for ALL tokens as a baseline, fees and price impact charged.
- `GET /v1/watch/start` ($0.1 USDC) - Crowd Check watch ($0.10): watch one token for 1 to 168 hours. Returns a ticket. Params chain (base|ethereum|robinhood|solana), token, hours. Then poll for plain alerts: pool liquidity down 30 percent, price down 50 percent, creator balance down 50 percent, measured from the best level since the watch began.
- `GET /v1/watch/poll` ($0.01 USDC) - Crowd Check watch poll ($0.01): what changed since the last look. Param ticket from /v1/watch/start. Plain-language alerts, none if nothing moved. Not charged when market data is unavailable or the watch expired.
- `GET /v1/holders/card` ($0.1 USDC) - Crowd Check plain card ($0.10): who holds the supply, who can pull the pool, who holds powers over the token, and the largest sensible position, under 900 characters with a verdict (go, caution, no_go). Free quote first at /v1/holders/quote, then ?quote=<id>. Not financial advice.
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- MCP: Official MCP registry: io.github.CyberPunk11147/cyberwarex-defi-oracle - tools: token_safety, honeypot_check, contract_risk (install via registry.modelcontextprotocol.io)
- OpenAPI: https://oracle.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://oracle.cyberwarex.com/token?address=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&chain=base'`

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

### Agent Search

Keyless web search for AI agents: one metasearch query across major engines on a dedicated SearXNG instance, clean trimmed JSON (title/url/snippet/engine), up to 10 results. No accounts, no API keys, no subscription. Free trial: 3 calls/day with the 'X-Free-Trial: 1' header.

**Use when:** Call it whenever your agent needs fresh facts from the open web - one keyless query, clean JSON back, no search account to set up. Use /answer when you want ONE cited answer to a question instead of raw links - it searches, reads the top pages, and returns the answer with sources.

- Base URL: `https://search.cyberwarex.com`
- `GET /search` ($0.003 USDC) - Web search - q, category (general|news|images), lang, max_results<=10
- `GET /contents` ($0.002 USDC) - Read one web page as clean markdown/text (JS rendered), truncate with max_chars
- `GET /search-contents` ($0.006 USDC) - Web search with the page text of the top results already extracted (up to 5 pages, parallel)
- `GET /news` ($0.001 USDC) - Ranked news brief for any topic: corroboration + freshness scored headlines, 15-min cache, zero-LLM
- `GET /answer` ($0.03 USDC) - Answer engine - one call searches, reads the top pages, and returns a concise cited answer with sources
- Free trial: 3 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://search.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' \
  'https://search.cyberwarex.com/search?q=x402+protocol&max_results=3'`

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

### Agent Council

Pay-per-call council of AI models for agents that need a judgement call rather than a lookup. Your question goes to 3 or 4 DIFFERENT models (deepseek, gpt-oss, glm, nemotron); each answers independently, and in deep mode each then sees the others and revises. A chair returns one verdict with confidence, the points every seat agreed on, the dissent that held, and what would flip the answer. Use it when one model's opinion is not enough: is this safe, is this worth it, which option. Typical answer in 5-7 seconds. No account, no API key. The grounded tier (/grounded) spends on real evidence first: it scans your question for a contract address, URL or $TICKER, buys the matching checks (honeypot sim, sanctions, page content, SEC profile), and one analyst returns a verdict that rests on what was found, with the source list and spend ledger included.

**Use when:** Call it when the next step is a judgement call rather than a fact: whether to trust something, which of two options to take, whether a deal or a risk is worth it. You get several independent models' verdict plus where they disagreed, instead of one model's guess. Use /grounded when the decision turns on facts we can go and buy: a contract address, a link, a ticker.

- Base URL: `https://council.cyberwarex.com`
- `GET+POST /council` ($0.01 USDC) - Quick council: 3 models, 1 round -> verdict, confidence, consensus, dissent, watch_for
- `GET+POST /council-deep` ($0.03 USDC) - Deep council: 4 models, 2 rounds (each seat sees the others and revises) -> a verdict that survived cross-examination
- `GET+POST /grounded` ($0.05 USDC) - Grounded council: priced per request ($0.05-$0.12). We buy the evidence first (honeypot sim, sanctions screen, page content, SEC profile), then one analyst judges on what came back; the response lists every source and what we spent. Measured equal to the 4-model panel on evidence-rich questions, and about 6x faster. GET it unpaid to see the quote first. Needs a contract address, URL or $TICKER in the question: with nothing to check it returns 503 and charges nothing.
- Free trial: 1 call(s)/day per IP (header `X-Free-Trial: 1`)
- OpenAPI: https://council.cyberwarex.com/openapi.json
- Example: `curl -H 'X-Free-Trial: 1' 'https://council.cyberwarex.com/council?q=Is%20a%203-day-old%20pool%20paying%2042%25%20APY%20with%20an%20unverified%20proxy%20admin%20safe%3F'`

---
_Generated from `agents.json` on 2026-10-18. Source of truth: https://cyberwarex.com/agents.json_
