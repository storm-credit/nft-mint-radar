# Public mint contention — measured, 2026-09-17

**Validation state:** `SPIKE_VALIDATED` (direct on-chain measurement, two live mints)
**Question answered:** When a free/cheap public mint stage opens, can a human-in-the-loop path win a unit — and how should the radar score such an opportunity?

This is observational evidence gathered while operating two live mints. It is not production code and defines no contract. It exists to give scoring and alerting a measured baseline instead of an assumption.

> **Measurement-reliability warning.** A first pass at §1 used JSON-RPC *batch* calls against the Arc public RPC. Batches silently dropped requests and returned partial results, producing wrong counts (an earlier revision of this file claimed "2,105 attempts / 708 pre-open / 2.8 % success"). Those numbers are withdrawn. Arc also prunes historical state fast enough that `eth_call` at past blocks became unreliable within ~30 minutes. Everything below comes from **sequential, retried** receipt lookups, which are stable. Treat any count gathered by RPC batching as unverified.

---

## 1. AKARII (Arc, chainId 5042) — the contention measurement

Public stage opened at **02:00:00 KST**, in block `21189390`. Arc block time ≈ 0.507 s.
(The stage start was originally inferred as 02:00:03 by back-dating 4 h from the first observed mint transaction. That was wrong by 3 s — the first mint landed 3 s after the stage actually opened. **Never infer a stage start from the first mint; read it from the contract.** Arc's minter exposes no stage view, which is why this had to be inferred at all.)

**The opening block, verified tx by tx:**

| | |
|---|---|
| mint transactions in block `21189390` | **374** |
| succeeded | **7** (transaction indices 9–15, one contiguous run) |
| units taken by those 7 | **9** |
| every other tx in the block | reverted (sampled idx 2, 20, 40, 80, 150, 250, 350 — all revert) |
| succeeded in any later block | 0 |

**The seven winners:**

| idx | from | qty | gasPrice |
|---|---|---|---|
| 9 | `0xfeb4188e…` (nonce 1) | 2 | 203,020 gwei |
| 10 | `0xcf666b83…` (nonce 0) | 1 | 203,020 gwei |
| 11 | `0xd5e33fc3…` (nonce 0) | 1 | 203,020 gwei |
| 12 | `0x303aabc1…` (nonce 0) | 1 | 203,020 gwei |
| 13 | `0x28bb1ea8…` (nonce 0) | 2 | 203,020 gwei |
| 14 | `0xf439ec43…` (nonce 0) | 1 | 203,020 gwei |
| 15 | `0x021164ef…` (nonce 0) | 1 | 203,020 gwei |

**Findings**

1. **Arc orders by gas price.** A normal AKARII mint earlier that evening paid 243 gwei and cost 0.05 USDC. The winners paid **203,020 gwei — ~833× normal, roughly 43 USDC of gas to win a 50 USDC NFT.** They occupied the front of the block; 367 transactions behind them reverted. Arc is Circle's own L1 (Malachite consensus), **not** an Arbitrum Orbit chain, and the FCFS assumption does not transfer to it.
2. **Identical gasPrice across all seven, all from fresh wallets (nonce 0–1).** One operator running a fleet, or one tool with a shared default. Either way, not seven independent humans.
3. **Hundreds of `buy()` calls landed before the stage was active**, every one reverting `StageNotActive()`. Sampled pre-open blocks: 180/180 reverted, 180/180 used selector `0xd96a094a` (`buy(uint256)` — the *public* function), 167 distinct senders. These are not leftover allowlist mints (`0xc24860e5`, zero occurrences); they are contenders burning gas to be queued when the stage flips.
4. The opening block ended it. No transaction in any later block succeeded.

**Conclusion:** a human-in-the-loop path (wallet dialog + manual approve) cannot win this shape of mint. Not "unlikely" — structurally excluded, whichever ordering rule the chain uses.

## 1b. Chain ordering is per-chain and must be measured

Robinhood Chain (4663) was tested the same way — 40 blocks with ≥4 transactions, checking whether in-block `gasPrice` is monotonically descending:

| ordering | blocks |
|---|---|
| descending gasPrice (priority auction) | **0** |
| ascending | 5 |
| unordered (arrival order / FCFS) | **35** |

e.g. block `65316712`: `[0.0, 0.048, 0.049, 0.3, 0.117, 0.048, …]` — a 0.3 gwei transaction sits fourth. Robinhood Chain **is** FCFS; Arc is **not**. The two behave oppositely, and guidance given for one was wrong when carried to the other. **Measure ordering per chain before advising on gas.**

## 2. Rare Friends Genesis (Robinhood Chain, 4663) — the valuation trap

Free mint, 1,024 supply, public stage 2026-09-17 23:00:20 KST, ~57 units remaining.

| Time (KST) | Floor | Actual clears |
|---|---|---|
| 09-16 19:45 | $5,890 | ~$5,300–5,950 |
| 09-17 01:25 | $3,200 | **$2,402–2,777** |

−55 % in 5.5 hours. Mechanism, verified in tx `0x911996afb4973c124ccf5ac030aac7856e244888db7a5d4367e0f5c7a7205dc7`
(status 1, 97 logs, 24,252,185 `$RAREFRIENDS` transferred across 35 events): buy token → activate Genesis → claim ~900 k tokens per NFT → dump, all in one transaction.

**Finding:** the NFT's price is a *derivative* of a claimable token. Each new mint adds ~900 k tokens of sell pressure, so minting is reflexively dilutive. A floor price snapshot is a lagging, misleading input for such collections.

## 3. Operator mutability

Observed 2026-09-16 ~20:40: the public stage `startTime` moved from 1789567220 (09-16 23:00:20) to 1789653620 (09-17 23:00:20) — exactly +86400 s. OpenSea surfaced only a "Configuration Changed" banner and rounds displayed times to the minute; the `:20` second offset exists only on-chain. Allowlist and public `endTime`/`startTime` are coupled, so one edit shifts both.

## 4. Implications for the radar

- **Score a "human-reachable" flag, not just an opportunity score.** Inputs: units remaining at stage open, chain ordering (FCFS vs priority auction — **measured, not assumed**), block time, observed pre-open queue depth for comparable drops. A drop failing this flag should be alerted as *information*, not as an action item with a deadline.
- **Alert lead time should be sized to preparation, not to mint time** — but do not assume funding is the binding constraint. Here it was not: the funded wallet was ready at 00:34, 86 minutes before the 02:00:00 open, and a second wallet's bridge landed at 01:59:19, 41 s before. Both were in time. The loss came entirely from contention.
- **Re-read stage config from chain immediately before any deadline-bearing alert, and never infer a start time from the first observed mint.** That inference was off by 3 s here. Marketplace UIs round to the minute and lag; operators move times. Selector reference: SeaDrop `getPublicDrop(address)` = `0xbc6a629c`, `getMintStats(address)` = `0x840e15d4`. When a minter exposes no stage view (AKARII), treat the derived start as ±seconds and say so in the alert.
- **Validate call shape with `eth_call` before asserting a mint is actionable.** A `NotActive(now,start,end)` / `StageNotActive()` revert proves the calldata is correct and only the clock is wrong. `eth_call` state override (balance) lets this run before funds are in place.
- **For token-backed NFTs, track the underlying token, not the NFT floor.** Treat floor as derived and stale.

## 5. Method notes (reusable)

- Remaining supply must come from the **mint contract**, not the NFT. AKARII's DN404 mirror `nft.totalSupply()` swung 606 → 1,633 from ordinary transfers; `minter.remaining()` (`0x55234ec0`) was the only correct source.
- Allowlist membership for AKARII was served as public static files (`/gtd-proofs.json`, `/fcfs-proofs.json`) — 401 and 4,041 addresses. Eligibility was checkable offline, with no wallet connection and no site interaction.
- Arc public RPC `https://rpc.mainnet.arc.io` prunes aggressively: `eth_getLogs` over a 700-block window returned `requested data not available`, and `eth_call` at blocks ~30 min old began failing mid-analysis. Per-block `eth_getBlockByNumber(_, true)` plus **sequential, retried** `eth_getTransactionReceipt` is what produced §1 and is the only combination that gave repeatable answers.
- **Do not use JSON-RPC batch calls for measurement.** Against this endpoint, batches returned partial results without error — the same block reported 7 successes on one pass and 0 on another. Every withdrawn number in the warning at the top of this file came from a batch.
- Chain ordering is testable cheaply and should be: pull ~40 blocks with ≥4 transactions and check whether in-block `gasPrice` is monotonically descending (§1b).
- Windows/Git-Bash note: long JSON payloads passed via `curl -d` hit `WinError 206` (command line too long). Write the payload to a file and use `curl -d @file`.
