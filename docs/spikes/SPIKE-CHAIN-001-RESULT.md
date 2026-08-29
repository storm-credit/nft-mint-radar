# SPIKE-CHAIN-001 Result — On-chain discovery feasibility

## Status
**DETECTION MEASURED AND WORKING / EARLINESS STILL UNMEASURED**

Opened by `ADR-012` as the fallback discovery path if allowlist-platform APIs prove inaccessible.
Research plus one live keyless probe run. Zero cost.

## Question
Is on-chain contract-deployment and first-mint monitoring buildable today for Ethereum, Base and
Robinhood Chain, and is it actually *early*?

---

## Infrastructure — not a risk

Robinhood Chain is better provisioned at two months old than most chains are at two years.

| | Robinhood Chain | Ethereum | Base |
|---|---|---|---|
| EIP-155 chain id | **4663** | 1 | 8453 |
| Architecture | Arbitrum Orbit / Nitro L2, settles to Ethereum | — | OP Stack |
| Public RPC | `rpc.mainnet.chain.robinhood.com`, no key, "rate-limited, not for production" | many | `mainnet.base.org`, **no WebSocket** |
| Block time | **~100 ms** (~864k blocks/day) | ~12 s | 2 s |
| Explorer API | **Blockscout**, Etherscan-compatible | Etherscan | Basescan / Blockscout |
| Etherscan V2 | ❌ chain 4663 not supported | ✅ free | ⚠️ paid only |
| Alchemy | ✅ RPC, NFT API, Transfers API, Webhooks, WebSockets | ✅ | ✅ |
| Alchemy gaps on 4663 | ❌ **Trace API, Debug API**, Receipts API | — | — |
| Subgraphs | ✅ The Graph, Goldsky, Ormi | ✅ | ✅ |
| OpenSea | ✅ supports it | ✅ | ✅ |

Blockscout requires a free key from `dev.blockscout.com`, and **one key covers all three chains**.
Free tier is 5 RPS / 100k credits per day, and most calls cost 20 credits — so roughly **5,000
requests/day**. That is enough for enrichment, not for continuous scanning.

Two operational limits to design against:
- `eth_getLogs` and `txlistinternal` are **capped at 1,000 records on Robinhood Chain**. On a chain
  doing ~19.6M tx/day any broad range query silently truncates. Detect `len == 1000` and subdivide.
- Spritehood, a $1.28M mint, is **unverified on Blockscout**. "Verified source code" is therefore
  **not** a usable quality filter on this chain.

### Canonical mint event topics
Recorded here because a probe written against this document used recalled values instead, and two of
three were wrong — one with a hallucinated tail, one only 63 hex characters. Either would have made
every ERC-1155 mint invisible and produced a confident, false "on-chain detection is thin" result.

```text
Transfer(address,address,uint256)                         0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
TransferSingle(address,address,address,uint256,uint256)   0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62
TransferBatch(address,address,address,uint256[],uint256[]) 0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb
```

ERC-20 and ERC-721 share the `Transfer` topic0, so a token filter cannot rely on topic0 alone — an
ERC-721 mint is distinguished by having three indexed topics, an ERC-20 transfer by two.

Any code using these must validate the shape at load time. A malformed topic matches nothing, and
"matches nothing" is indistinguishable from "there was nothing to match" in the output.

### The 100 ms block time is a non-issue, if the design is right
Per-block scanning is dead on arrival: ~26M blocks/month at 60 CU each is ~1.56B CU ≈ **$700/month**
for one chain, and 10 blocks/sec already exceeds Blockscout's free 5 RPS.

Range-polling on a wall-clock interval makes cost identical across all three chains: at ~10 s latency
the whole thing sits **inside free tiers, $0–50/month for all three**. Block time should not drive
polling rate; latency tolerance should. Alchemy WebSocket `eth_subscribe(logs)` is better still and
is supported on 4663 — note Base's public RPC has no WebSocket, so Base needs a keyed provider.

### The Trace/Debug gap is the real constraint
Without `trace_block` / `debug_traceBlockByNumber` on chain 4663, internal `CREATE`/`CREATE2` opcodes
cannot be enumerated. Modern launches overwhelmingly deploy **minimal-proxy clones via a factory**
(Manifold, Zora, thirdweb, Highlight, OpenSea Studio), which means the deploy is an internal call. A
`tx.to == null` scan catches only direct deploys and misses most real launches.

The practical detector on Robinhood Chain is therefore log-based: `Transfer` with
`topic1 = zero address`. That is cheap, chain-agnostic, and catches everything regardless of how it
was deployed — **but it fires at the first mint, not at deploy.**

Whatever lead time a deploy-before-mint gap would have provided, this architecture discards on the
one chain we care most about. "On-chain is earliest" may collapse to "on-chain is simultaneous".

---

## MEASURED 2026-08-29 — run `33265757917`

First live run of `spikes/onchain_probe.py` via GitHub Actions. Public RPCs only, no keys, no cost.
294 RPC calls total across three chains.

### Robinhood Chain — detection works, and the volume is the finding

| Measurement | Value |
|---|---|
| blocks scanned | 3,000 |
| chain time covered | **301 seconds** (~5 minutes) |
| observed block time | 0.1 s, matching the documented ~100 ms |
| **distinct minting contracts** | **240** |
| total mint events | 10,432 |
| `eth_getLogs` calls used | **5** |
| truncations hit | **0** |

Detection is proven and it is cheap: five calls covered five minutes of a chain doing ~864k
blocks/day, with no 1,000-record truncation at this window size.

**240 distinct minting contracts in five minutes.** Extrapolated naively that is roughly 2,900 per
hour and **~69,000 per day, on one chain**. The real mints anyone would want are a handful among them.

This is the strongest evidence yet for the line already recorded in the research: **the scarce
resource is filtering, not discovery.** A radar optimized for speed of detection would deliver a
firehose of junk. Discovery on this chain is nearly free; deciding which 5 of 69,000 matter is the
entire product.

### ERC-1155 is negligible here
`erc721: 10,431` against `erc1155: 1` in the same window.

Stated honestly against an earlier claim of mine: the malformed ERC-1155 topic constants that were
corrected before this run would have hidden **one event out of 10,432** on this chain. The practical
impact here was small. The correction and the load-time guard remain right, because that ratio was
unknowable in advance and may differ on Ethereum or Base — but the catch mattered less than it looked.

### Ethereum and Base — blocked, for two different reasons
- **Ethereum** (`ethereum.publicnode.com`): `eth_getLogs` rejected — *"Archive requests require a
  personal token."* The free public endpoint will not serve log ranges.
- **Base** (`mainnet.base.org`): `-32020 backend response too large`. The window was too wide; Base
  needs smaller block ranges per call, or a keyed provider.

Neither is a dead end. Both need either a smaller window or a free-tier key.

### Timing — still unresolved, and now we know exactly why
0 known, 25 unknown. Every creation lookup failed with
`binary_search_rpc_error: metadata is not found, <block>`.

The cause is concrete: **the Robinhood public RPC is not an archive node.** `eth_getCode` at block
~24.6M against a head of ~49.3M is far outside a pruned node's retention. The binary-search fallback
cannot work on a pruned endpoint at all — it is not a tuning problem.

To resolve the timing question the probe needs archive access: a free Blockscout key
(`dev.blockscout.com`, one key covers all three chains) or an Alchemy free-tier key. Both are free;
neither was used in this run because the run was deliberately keyless.

## The question that decides it — STILL UNRESOLVED

**Does contract deployment reliably precede the public announcement?** The researcher found no data
and explicitly declined to guess. That is the correct outcome to report, and it leaves the fallback
path unproven.

## The finding that may matter more than the answer

On Robinhood Chain, the two largest realised mints so far had **no allowlist at all**:

| Project | Model |
|---|---|
| **Spritehood** — Aug 11, 42,956 sold, $1.28M, ~53 min | **Public, explicitly no whitelist** |
| **StonkBrokers** — Jul 17, 4,444, floor peaked ~13 ETH | **Free mint** |
| Chain Mancers | whitelist via burning HOODL/SLOP/Slonk |
| The Saudis (unlaunched) | whitelist via holding NFTs / posting |
| Chog (upcoming) | tiered whitelist by $CHOG holdings |

This cuts in an unexpected direction and matters for the product, not just the adapter:

- For **open/free mints**, there is no allowlist to be locked out of. Detection *speed* is the entire
  game, and the timing objection above does not apply.
- For the **allowlist-gated** ones on this chain, the gate is **token holdings or social activity** —
  burning tokens, holding NFTs, posting — which closes long before deploy and which no amount of
  on-chain deploy monitoring can help anyone pass.

Stated as inference, not evidence, because it rests on five data points: the allowlist objection is
probably fatal for allowlist-gated drops and probably irrelevant for open mints, and Robinhood Chain
currently skews toward open mints.

---

## Deliberately not claimed
- That deploy precedes announcement. Unmeasured.
- That the ERC-165 interface ids quoted in the research are correct — the researcher flagged them as
  recalled, not verified against the EIPs. Verify before use.
- That factory-deploy coverage via Blockscout internal transactions is sufficient on 4663. Untested.
- Existing-tool survey (Reservoir, SimpleHash, Moralis, Nansen, Mintify, OpenSea API access) did not
  complete. Alchemy NFT API + Webhooks being live on 4663 is the most promising off-the-shelf path
  found, but its fit is unassessed.

## What would settle it
Pull 20–30 recent Ethereum and Base collections, compare contract-creation block timestamps against
announcement times, and check whether contracts land days early in a paused state awaiting
`setSaleState`. That measurement, not more infrastructure research, is the gate.

Cost: a few hours and free-tier API calls.

## Gate impact
On-chain **detection** is now measured, not assumed: it works, it is cheap, and on Robinhood Chain it
surfaces ~69,000 minting contracts per day.

On-chain **earliness** remains unmeasured, and the reason is now specific rather than vague: the
keyless endpoint cannot serve historical `eth_getCode`. A free key unblocks the measurement.

The more important shift is what the volume implies. Discovery was never the bottleneck this path was
meant to solve — filtering is. Any design that treats "we can see mints fastest" as the win condition
is answering a question the measurement says is already answered and cheap.
