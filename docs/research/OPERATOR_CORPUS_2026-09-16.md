# Operator Corpus Analysis — 2026-09-16

## What this is
The user shared five days of posts (2026-09-11 to 09-16) from a Korean Telegram alpha channel they
actually follow, and asked how that operator sees things.

This is the first **ground-truth corpus** in the project. Everything before it was provider
documentation, market statistics, or research about influencers in the abstract. This is a real
curator making real calls, with timestamps, and with their own money at stake — including the ones
they got wrong.

Note on method: this was pasted by the user for analysis. It is not collected data, and nothing here
changes `ADR-012`'s exclusion of Telegram as a runtime source. It is used as evidence about *what a
good curator does*, so the product can be designed to match.

---

## 1. Lead time is measured in DAYS, not seconds

This is the single most consequential finding, and it is directly measurable from the timestamps.

| Project | Announced in channel | Actionable moment | Lead |
|---|---|---|---|
| **Rare Friends** | 09-11 05:16 (WL invite link) | mint ~09-15 | **~4 days** |
| **The Standard Reserve** | 09-14 16:45 (full schedule) | WL mint 09-15 06:30 | **~14 hours** |
| **zkSNARKS** | 09-16 00:17 | auction opens 09-16 01:00 | ~45 min |
| **Zec Punks** | 09-15 18:59 | mint 09-15 22:00 | ~3 hours |

The operator's own Rare Friends outcome makes the point: they applied for the allowlist on 09-11,
forgot about it, and discovered on 09-15 that they had won and could mint — *"뭐지 이거 언제 민팅
시작했지.. 화리 당첨되어있길래 민팅했네요"*. Free mint, floor $960 the same day, and by 09-15 22:06
*"두들 5개를 살 수 있는 가격"*.

**The value was captured four days before the mint, by filling in a form.**

### What this does to our latency design
`ADR-010` chose `STREAM_PRIMARY` partly on a measured ~4.8 s X stream delivery versus polling "in
minutes". `METRICS_SLO.md:16` sets the product target at p95 ≤ 15 minutes.

Against a four-day window, the difference between 4.8 seconds and 15 minutes is **noise**. Blind spot
`BS-2` raised this; this corpus settles it. The remaining honest argument for stream over search is
cost shape, not latency — which is what `ADR-010` does *not* say.

This does not mean latency never matters: zkSNARKS had a 45-minute window and Zec Punks about three
hours. But nothing in five days required second-level detection.

---

## 2. The actionable object is the ALLOWLIST OPEN, not the mint

Every high-value outcome in this corpus came from entering a list days earlier, not from being fast
at the mint.

Our domain model already separates `Opportunity` (the action) from `MintStage` (the mint), and the
`Opportunity` flow already runs `REGISTRATION_PENDING → REGISTRATION_OPEN → REGISTRATION_CLOSED →
RESULTS_PENDING → MINT_SCHEDULED → MINT_OPEN`. That structure is **confirmed correct by this corpus**,
and the priority inside it is now evidenced: `REGISTRATION_OPEN` is the alert that matters most, and
its `registration_close_at` is the deadline that actually costs money when missed.

---

## 3. Holder-gated eligibility is the dominant WL mechanic — and it is the one miss

Repeatedly, allowlist access is determined by **what you already hold**:

- Rare Friends: *"Doodle, POOP 토큰, Stonkbroker, Quotron 등등 보유시 추가 포인트"*
- Yield Fields: *"OCH Ringbearers & Genesis Rings 보유자는 확정 화리"*, and separately
  *"현재 1 ETH 이상의 NFT 소유해야 확정 화리"*
- Chain Mancers (from `SPIKE-CHAIN-001`): whitelist via burning HOODL/SLOP/Slonk

**The operator's only recorded miss is exactly here.** On Yield Fields: *"살까 말까 했는데 아쉽스"* —
they considered buying the gating NFT, didn't, and the gating NFTs then rose on the WL announcement.

That is a product-shaped hole. A system that knows (a) the user's holdings and (b) that project X
grants guaranteed WL to holders of Y, can alert **"buy Y now to qualify for X"** — a decision with a
deadline, which is precisely what this product claims to produce.

It also has an obvious risk edge: that alert is a buy recommendation in all but name, and the gating
asset can be pumped by the announcement itself. It belongs behind the Risk gate, not in the happy path.

**Design check required:** `Opportunity.eligibility_ref` exists as a `string|null`. Holder-gating is
structured data — collection address, chain, minimum count or value, snapshot time — and a bare
string reference may not carry it. This needs review before the eligibility path is implemented.

---

## 4. The post structure maps almost exactly onto our schema

Every substantive post carries the same fields, in the same order:

```
프로젝트명 / 개수 / 가격 / 체인 / 일정(정확한 시각) / WL 링크 / X 링크 / 왜 핫한지
```

Against our model: supply, `AssetAmount` + `price_state`, `ChainIdentity`, `MintStage` open/close,
`official_action_url`, source identity, and evidence. The correspondence is close enough that the
schema was clearly designed for the right shape.

The Standard Reserve post is a textbook multi-stage campaign:

| Stage | Window | Price |
|---|---|---|
| Allowlist mint | 06:30–09:30 | 0.15 ETH |
| Public Dutch auction | 09:30–10:00 | **1.25 → 0.15 ETH over 30 min** |
| Token liquidity | 10:00 | — |

Sold out immediately at **1.2353 ETH** — the top of the Dutch curve.

### Two price mechanics our model should be checked against
- **Dutch auction**: price declines on a schedule. `price_state = VARIABLE` exists, but a Dutch
  auction has a *known start, known floor and known decay* — that is more structured than "variable",
  and the difference matters because the alert should say what the price will be when the user can act.
- **Blind auction with clearing price** (zkSNARKS): top 8,000 bids win, all pay the same clearing
  price, losers refunded. Not a price at all in the current model's sense.

Neither is exotic; both appeared within five days.

---

## 5. What the operator actually adds is the "왜", not the calendar

The calendar is cheap — `SPIKE-CHAIN-001` measured ~69,000 minting contracts per day on Robinhood
Chain alone. This operator posts roughly two or three calls a day. **The compression ratio is the
product.**

Their stated reasons for Standard Reserve being hot:
- Uniswap Foundation funded the audit, and the founder commented publicly;
- multiple X influencers were posting their WL allocations (*"WL 자랑"*, ~450 allocated);
- therefore the public Dutch auction would likely clear high.

That second item is the **convergence signal** `ADR-012` describes, observed in the wild: independent
accounts posting allowlist screenshots. It is X-observable and author-scoped, exactly the shape we can
legitimately read.

### And they filter *out* as often as in
On Standard Reserve they analysed it and declined:

> *"NFT 출시시 Soulbound라서 전송 & 거래 불가능"* … *"퍼블릭 옥션 참여하여 NFT를 구매했으면 토큰을
> 구매해서 폰지 구조에 무조건 참여해야함"* … *"안오겠지만 0.5 ETH 이하 정도면 들어가볼듯"*

Three things there we do not currently model:
1. **Soulbound / non-transferable** — you cannot exit. A first-class risk flag, absent from our Risk list.
2. **Structural obligation** — owning the NFT forces continued token participation. A mechanism risk,
   not a link-safety or identity risk.
3. **A price at which the answer changes** — not "avoid", but "avoid above 0.5 ETH". Our
   `DecisionResult` is action plus severity; it has no concept of a conditional entry price.

They also flagged a clone outright: Otomate is *"QUOTRONS 짭"* — a copy. Derivative-of-a-successful-
project is a recognisable negative signal.

---

## 6. Chain distribution over five days

| Chain | Projects mentioned |
|---|---|
| **Robinhood** | Rare Friends, The Standard Reserve, Yield Fields, Yield Farm |
| Ethereum | Argonauts, zkSNARKS |
| Ink | Otomate |
| Zcash | Zec Punks (via Zec Bit launchpad) |
| Solana | Jupiter reclaim, Frontier Traders |
| Hyperliquid | Hypurr Genesis |
| **Base** | **zero** |

Robinhood Chain leads this operator's NFT mint attention, which supports keeping it first-class.

**Base appears zero times in five days.** That is independent confirmation of the deprioritisation in
`ADR-012`, arrived at from a completely different direction than the OpenSea probes.

Ink, Zcash and Hyperliquid are all out of our Phase 1 scope, and real activity happened on them. That
is a live coverage gap, not a hypothetical one — `ADR-007`'s revalidation trigger should be judged
against data like this.

---

## 7. The channel is broader than NFT mints
Pokémon 30th anniversary boxes, Nike x One Piece sneaker raffles, KREAM resale prices, a crypto-tax
petition, token launchpads, airdrops. Perhaps half the posts are not NFT mints at all.

Relevant because it means a human curator's feed is not a clean signal either — the filtering problem
exists for them too, and they solve it by being a person with taste rather than by having better
coverage.

---

## Design implications, ranked

1. **Latency optimisation is answering the wrong question.** Four-day lead times make the
   stream-versus-search argument in `ADR-010` cost-shaped, not latency-shaped. Revisit its rationale.
2. **`REGISTRATION_OPEN` and `registration_close_at` are the highest-value alert and deadline**, above
   mint timing. Weight accordingly.
3. **Holder-gated eligibility needs a structured representation**, not a bare `eligibility_ref` string,
   and it unlocks the "buy Y to qualify for X" alert — which must sit behind the Risk gate.
4. **Add Soulbound / non-transferable as a Risk flag.** It is an exit-liquidity risk with no current
   home in the model.
5. **Add derivative-of-existing-project ("짭") as a negative Quality signal.**
6. **Consider a conditional entry price** in the decision output. "Avoid above X" is the form a real
   call takes, and the current action/severity pair cannot express it.
7. **Check Dutch-auction and blind-auction pricing against `price_state`.** Both appeared in five days.
8. **Base's zero showing corroborates its deprioritisation from an independent direction.**

## What this corpus does not establish
- It is one operator over five days. Their hit rate is not measurable from it, and survivorship is
  obvious — wins are posted more visibly than misses, though at least one miss was recorded honestly.
- It does not tell us whether *our* system could have surfaced these before they did. That comparison
  needs the same window replayed through our sources, which we cannot do retroactively.
- It does not validate any seed account in `ADR-012`. This operator is not on that list.
