# Minimum Action Agent OS 적용 규칙

## 목적
이 문서는 `storm-credit/minimum-action-agent-os`의 **작업 방식** 가운데 NFT Mint Radar에 필요한 원칙만 채택한다.

가져오는 것은 도메인 설계가 아니라 다음 운영 규칙이다.
- 최소 Tool / 최소 Context / 최소 Authority
- 모델이 한 번에 선택하는 Local Action Space 제한
- Agent / Skill / Rule / Direct Work 구분
- 독립 검수
- Shadow Authority / Stale Derived Artifact 방지
- Projected / Observed 상태 분리
- Plan Drift 기록
- hard guarantee의 programmatic enforcement

`minimum-action-agent-os` 자체를 런타임 의존성으로 넣지 않는다. 이 프로젝트의 정본은 계속 이 저장소 안에 둔다.

---

## 1. Prime Directive — Minimum Necessary Agency

현재 작업에 필요한 권한과 정보만 제공한다.

1. **Least Tool** — 현재 노드가 실제로 써야 하는 callable만 노출한다.
2. **Least Context** — 현재 판단에 필요한 Evidence/Project/Stage bundle만 전달한다.
3. **Least Authority** — read-only로 충분하면 write/execute 권한을 주지 않는다.
4. **Isolation by Boundary** — context, permission, evidence regime, failure mode가 실제로 다를 때만 분리한다.
5. **Programmatic Guarantees** — 비용 상한, CTA 안전, idempotency, state transition, no-wallet-action 등 하드 보장은 프롬프트가 아니라 코드/스키마/CI/runtime에서 강제한다.

---

## 2. Local Action Space

프로젝트가 설계하는 **model-driven reasoning node**는 한 번에 의미 있는 선택지를 기본 5개 이하로 유지한다.

중요:
- 전체 Agent/Source/Tool 수가 5개라는 뜻이 아니다.
- deterministic dispatch table, schema-driven routing, scheduler rule처럼 **코드가 선택하는 경로**는 모델 선택지로 세지 않는다.
- 모델이 label/route를 내고 그 값으로 여러 callable 중 하나를 고르면 모델이 선택한 것이므로 선택지에 포함한다.
- open-ended shell/HTTP/SQL 하나로 많은 선택을 숨겨서 숫자를 줄인 것으로 취급하지 않는다.

### NFT Radar 적용
Production hot path에서 중앙 LLM orchestrator가 다음을 모두 직접 고르지 않게 한다.

```text
Source Adapter
  -> Normalization
  -> Verification
  -> Campaign/Stage State
  -> Scoring
  -> Decision
  -> Outbox
  -> Telegram
```

위 파이프라인의 기본 route는 **deterministic code**가 소유한다.

LLM은 필요한 좁은 노드에서만 호출한다.

권장 model-driven nodes:
1. `UNSTRUCTURED_SIGNAL_EXTRACT` — 비정형 X/웹/Discord 공지에서 claims 추출.
2. `AMBIGUOUS_ENTITY_RESOLVE` — deterministic identity rule로 결론이 안 날 때만.
3. `QUEST_PARSE` — Phase 2에서 비정형 WL 작업 파싱.
4. `INDEPENDENT_CRITIC` — 설계/프롬프트/fixture 변경 검수.

Scoring 산식, hard risk gate, Opportunity/MintStage transition, dedup, Telegram template, source scheduler는 기본적으로 deterministic service다.

---

## 3. Agent vs Skill vs Rule vs Direct Work

새 역할을 만들기 전에 가장 가벼운 메커니즘을 선택한다.

### Direct Work
- 단순 변환/검사
- 별도 context/permission/evidence regime 불필요

### Rule
- 짧고 안정적인 전역 불변조건
- 예: `wallet signing 금지`, `T3/T4 단독 CTA 금지`

### Skill / Procedure
- 다단계지만 동일 context/permission에서 수행 가능
- 예: blind-spot sweep, preflight trap check, four-option comparison, prompt compilation

### Agent
다음 중 하나 이상의 **실제 경계**가 있을 때만 사용한다.
- 독립 context 필요
- 별도 권한/도구 필요
- 독립적 판단 필요
- 다른 evidence/source regime
- 다른 failure mode

`Security Agent`, `Scoring Agent`, `Telegram Agent`처럼 이름만 다르고 같은 context/tool을 쓰는 persona-only agent는 만들지 않는다.

---

## 4. Harness 역할의 구현 메커니즘

`HARNESS_SPEC.md`의 역할 이름은 **논리 계약**이지, 모두 별도 Agent라는 뜻이 아니다.

| Logical role | Phase 1 기본 구현 | LLM 여부 |
| --- | --- | --- |
| Discovery extraction | adapter + narrow extraction skill | 조건부 |
| Verification | deterministic evidence rules + narrow ambiguity resolver | 조건부 |
| Entity resolution | deterministic first, ambiguous fallback | 조건부 |
| Campaign/Stage state | deterministic state machine | 아니오 |
| Scoring | versioned deterministic formula | 아니오 |
| Wallet intelligence | query/analytics adapter | 기본 아니오 |
| Quest parsing | Phase 2 skill | 예, 필요 시 |
| User progress | explicit user/provider state | 아니오 |
| Decision | deterministic rules + thresholds | 아니오 |
| Telegram rendering | deterministic template | 아니오 |
| Independent critique | isolated reviewer | 예 |

Production hot path에서 한 LLM이 위 역할 전체를 orchestration하지 않는다.

---

## 5. Minimum Context Bundles

Deep repository graph와 runtime prompt를 분리한다.

### Signal extraction bundle
- one `RawEvent`
- source identity/tier
- small `ProjectIdentity` candidate set
- claim schema
- forbidden inference rules

### Verification bundle
- one claim group
- directly relevant Evidence only
- current Project official identity
- current campaign/stage refs when relevant
- link-safety rules

### Quest parsing bundle
- one campaign/stage
- source text/payload containing requirements
- Quest schema
- current deadline/timezone context

### Independent critic bundle
- artifact under review
- requirements
- constraints
- acceptance criteria
- evidence needed for verification

Builder rationale/self-justification은 기본적으로 critic에게 전달하지 않는다.

---

## 6. Source of Truth / Shadow Authority

한 사실에는 한 정본만 둔다.

Authority map:
- `CLAUDE.md` — 프로젝트 운영 헌법/Gate
- `docs/PROJECT_STATUS.md` — 현재 상태/Blocker/Next action
- `docs/DEEP_DESIGN.md` + Accepted ADR — 도메인/아키텍처 의미
- `docs/HARNESS_SPEC.md` — 실행 역할/게이트 계약
- `docs/HARNESS_SCHEMAS.md` — typed I/O 계약
- `docs/EVAL_FIXTURES.md` — golden acceptance cases
- `docs/PRODUCTION_CODING_START_GATE.md` — 본 코딩 시작 권한

요약 문서가 정본 내용을 손으로 다시 복제해 별도 truth가 되지 않게 한다.

### Stale propagation
상위 authority가 바뀌면 영향을 받는 파생 문서를 같은 변경에서 찾는다.

예:
`ADR/DEEP_DESIGN schema change`
-> `HARNESS_SCHEMAS`
-> `EVAL_FIXTURES`
-> `PROMPT_CONTRACTS`
-> `SPIKE mapping`
-> `PROJECT_STATUS`

영향받은 파생 문서를 갱신하지 못하면 `STALE`로 명시하고 Gate를 통과시키지 않는다.

---

## 7. Projected vs Observed

다음을 절대 동일 상태로 기록하지 않는다.

- `DESIGNED`
- `PAPER_VALIDATED`
- `SPIKE_VALIDATED`
- `PRODUCTION_VALIDATED`

Provider 문서에 있다고 실제 접근/비용/latency가 검증된 것이 아니다.
Estimate/projected cost도 measured cost와 분리한다.

---

## 8. Independent Critique

중요 설계/Prompt/Schema/Fixture 변경은 필요 시 독립 검수를 한다.

Reviewer 기본 입력:
- artifact
- requirements
- constraints
- acceptance criteria
- verification evidence

Reviewer가 builder의 rationale에 먼저 anchor되지 않게 한다.
특히 허용/금지 규칙의 **정의되지 않은 단어**를 찾아 가장 약한 해석에서도 안전 규칙이 유지되는지 검사한다.

---

## 9. No Premature Runtime

Agent OS를 구현하는 별도 framework를 먼저 만들지 않는다.

- Markdown/spec으로 충분한 것은 spec으로 유지.
- runtime은 실제 hard-enforcement gap이 있을 때만 추가.
- 현재 spike runner는 provider feasibility 검증용 disposable artifact이며 production orchestration framework가 아니다.

---

## 10. State / Plan Drift

대화 기록을 source of truth로 쓰지 않는다.

의미 있는 작업 뒤 `PROJECT_STATUS.md`에는 필요한 것만 유지한다.
- current milestone
- completed
- approved decisions
- constraints
- blockers
- next action
- verification state

계획이 바뀌면 `docs/deviations/CHANGELOG_DECISIONS.md`에 실제 divergence를 기록하고 과거를 새 계획처럼 다시 쓰지 않는다.

---

## 11. Completion Gate

Minimum Action 적용이 완료됐다고 말하려면:
- [ ] model-driven node별 local action space가 측정/설계되어 있음
- [ ] 중앙 God Agent가 없음
- [ ] 논리 역할과 실제 Agent가 분리되어 있음
- [ ] production hot path가 deterministic-first임
- [ ] LLM context bundle이 역할별로 제한됨
- [ ] independent critique 입력이 builder rationale과 분리됨
- [ ] hard safety/cost/state guarantees가 programmatic enforcement 대상으로 지정됨
- [ ] source-of-truth map이 존재함
- [ ] upstream schema 변경 시 stale propagation 규칙이 있음
- [ ] 현재 stale derived artifact가 0이거나 명시적으로 Gate를 막고 있음

## 현재 적용 판정

`ADOPTED_IN_DESIGN`

현재 동기화 상태의 authority는 이 문서가 아니라 `docs/PROJECT_STATUS.md`다. 아래 항목은 이 문서를 작성한 시점의 기록이며, 그 시점 이후 해소되었다.

이 문서를 만든 시점의 확인 사항:
- ADR-007/008은 accepted 상태다.
- `PROJECT_STATUS.md`는 이를 반영한다.
- 그러나 `DEEP_DESIGN.md`와 `HARNESS_SCHEMAS.md` 일부가 ADR-007/008 이전 표현을 아직 포함하므로 Shadow Authority/Stale Derived Artifact 정리가 필요하다.

따라서 다음 작업은 새 Agent를 추가하는 것이 아니라 **정본/파생 계약 동기화**다.
