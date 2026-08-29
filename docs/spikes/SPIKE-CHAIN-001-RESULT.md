# SPIKE-CHAIN-001 Result — On-chain discovery feasibility

## Status
**INFRASTRUCTURE VIABLE / DECISION BLOCKED ON AN UNRESOLVED TIMING QUESTION**

Opened by `ADR-012` as the fallback discovery path if allowlist-platform APIs prove inaccessible.
Research only, zero cost, no code.

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

## The question that decides it — UNRESOLVED

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
On-chain monitoring is **cheap, buildable, and infrastructure-unblocked**. It is **not** established
as early. Do not build the discovery path on it until the timing question is measured.
