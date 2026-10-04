# PROJECT SITUATION INDEX — iDSS

> Cross-chat orientation file. Read this before proposing research, architecture, cleanup, or implementation.
> This is a situational index, not a transcript and not a substitute for source evidence.

## 1. Identity and scope

iDSS is Prakash's private trading decision-support/research workbench and deterministic replay instrument.

It is NOT:
- an AI trader
- an execution bot
- a chatbot
- a generic trading terminal
- a HUD/dashboard-first product

Core loop: **Observe → Compare → Test → Decide → Build**

Primary design principle: **information before transport**.

## 2. Historical workspace rule

Historical workspace: E:\A New folder\Des

Des is a messy historical continuation containing old code, databases, captures, logs, exports, renamed/duplicate/obsolete artifacts.

Rule: **What stays in Des stays in Des.**

Do not clean-room redesign, delete historical evidence merely for neatness, rebuild from scratch because the tree is messy, or assume the newest-looking artifact is authoritative.

Current direction is to establish a smaller/current implementation surface while preserving and reusing historical DBs/data where justified.

## 3. Current architecture direction

Desired system:
- deterministic dual live + replay engine
- full snapshots plus delta/event ledger
- provenance for every material observation/derivation
- projections and explicit invalidations
- immutable journal
- historical replay with no look-ahead
- evidence classes: OBSERVED / CALCULATED / INFERRED / UNKNOWN

The AI/LLM is a language/reasoning interface over structured state. It must not become the state-of-truth by inventing observations or silently promoting inference to fact.

## 4. ChatGPT's role and situational-awareness boundary

ChatGPT is a **reasoning/chat component, not the iDSS agent, project authority, or system of record**.

Current ChatGPT sessions have limited persistent project knowledge and are not continuously attached to:
- E:\A New folder\Des
- live processes/databases/market feeds
- every repository change
- every Antigravity/local-agent action
- the complete historical project state

Therefore ChatGPT can reason deeply about supplied/retrieved project state, but must not pretend to have continuous situational awareness of the project.

The desired architecture is the reverse dependency:

**Persistent iDSS state/research/control layer**
→ current situation, history, evidence, negative knowledge, hypotheses, experiments, code/system state, live state, unresolved questions

then:

**Interchangeable reasoning models**
→ ChatGPT / Claude / other models provide research, criticism, hypothesis generation, synthesis and review

and:

**Agent/builder layer**
→ Antigravity/local agent operates Des, code, experiments and implementation

The intelligence should live primarily in the **persistent research/state machinery and validated evidence**, not inside any one model. Models should be replaceable components that query and contribute to that state.

A future system should allow the persistent iDSS layer to determine what it knows, does not know, what changed, which hypotheses are active, what experiments have been run, what failed, and which reasoning model/agent should be asked next.

## 5. Market Profile / Auction Reasoning direction

Market Profile is treated as a structural lens into the developing auction, not a prediction machine.

The MP domain engine should evolve from a rigid state machine into a deterministic Auction Reasoning Engine that maintains observations, events, hypotheses, supporting/contradicting evidence, temporal relationships, context, unresolved questions, explicit invalidations, and preserved historical interpretations.

Multiple interacting models are expected:
- OPEN MODEL
- VALUE MODEL
- OTF MODEL
- DAY DEVELOPMENT
- INVENTORY / CONTEXT

Opening classifications remain hypotheses until evidence develops. Example hypotheses include OTD_UP, OTD_DOWN, ORR_UP, ORR_DOWN, OAIR.

Questions are first-class objects, e.g.:
- Has the upper probe earned acceptance?
- Is this repair or genuine reversal?
- Is the day becoming directional or balanced?

The engine must preserve earlier interpretations rather than overwrite them. Trade/strategy logic remains separate from MP reasoning.

## 6. Live data lineage

Canonical desired live source: **FYERS Versova L3 TBT**.

Do not assume a filename containing 'fyers_tbt' proves TBT. Verify the actual API/data contract and captured payload.

Other known sources/roles:
- Upstox spot/derivatives as comparison/fallback where appropriate
- retail API/quotes for fallback, backfill, or offline work
- legacy ZMQ 5555 sink
- Telegram Market Profile listener is not source of truth

Known historical probe evidence:
- NIFTY26SEPFUT
- 178 candles
- futures LTP 23224.70
- Upstox spot 23204.75
- VIX 11.41
- Versova DB: 602 protobuf frames
- Telethon MP listener PID 6848, archive 944 rows

These are historical probe results, not current live facts.

## 7. Agent-control / project-memory requirements

Existing control substrate:
- AI_OPERATIONAL_LAWS 1–32
- Law31: Information Before Transport
- Law32: No Fabricated System Boundaries
- proposed Rule33 / PROJECT_SITUATION_INDEX
- SEED_EVIDENCE_REGISTER EV-001..EV-015
- RESEARCH_HYPOTHESIS_REGISTER RH-001..RH-012
- date-tree / archaeology approach

Recurring agent failure mode: **regression/reinvention**. An agent enters the project, reads a convenient subset, mistakes historical/obsolete material for current truth, and starts implementing from a false starting point.

Every new session should establish:
1. where the project currently is
2. what is historical vs current
3. what is proven vs inferred vs unknown
4. what has already been tried and failed
5. what machinery already exists
6. what the active frontier/question is
7. what the next justified action is

Negative knowledge is valuable and must be retained.

## 8. Public ecosystem research already performed

Research is not limited to Prakash's own repositories. Public GitHub repositories are discovery sources for reusable mechanisms.

Important external mechanisms identified:

### Engram — Gentleman-Programming/engram
Persistent local-first project memory for coding agents; SQLite/FTS5; MCP/CLI/HTTP/TUI; explicit orient/search/retrieve/save/handoff workflow; supports multiple coding agents including Antigravity.

Useful mechanisms: orient before writing; search before repeating; progressive retrieval; deliberate durable memory; stable topic keys; session handoff; compaction recovery.

### Agent-Memory-Bridge — zzhang82/Agent-Memory-Bridge
Governed local-first project memory separating durable memory/WHY, repository knowledge/WHAT, dynamic state, compiled context, transient bounded context, metadata attestation, run authority, and verified outcomes. Explicitly avoids silently turning transcripts or agent interpretations into durable truth.

### agent-memory-mcp — ipiton/agent-memory-mcp
Local memory/docs/repository context with typed memory, repo-aware indexing, duplicate/conflict/stale detection, temporal validity and supersession, session checkpoints, and context recovery.

### vartiainen1/agent-memory
Local governance-oriented memory with a human approval boundary: agents may suggest memory but cannot independently promote suggestions to trusted memory.

### project-context-map-mcp — tamojit-123/project-context-map-mcp
Repository topology/context mapping: index first, query topology, inspect sparse relevant files, avoid wandering and rebuilding context from scratch.

### Other public repos identified for further comparative research
- xChuCx/agent-memory
- nova-land/coding-agent-memory-mcp
- mikeylong/agent-memory-mcp
- Threesided-Studios/Agent-Memory
- jcyamacho/agent-memory
- rzem-ai/agent-memory
- additional repository-map/context/world-model projects surfaced during GitHub search

These are **research references, not adopted dependencies**.

## 9. Mechanism decomposition

Do not collapse 'memory' into one product. iDSS needs to distinguish:

### WHAT — repository intelligence
- topology
- dependency/file relationships
- current repository baseline
- change detection
- sparse retrieval

### WHY — project memory
- decisions
- rationale
- durable constraints
- discoveries
- failed approaches
- session handoffs

### NOW — situational awareness
- current project state
- active frontier
- unresolved questions
- blockers
- active hypotheses
- recent changes
- next justified action

### AUTHORITY — governance
- provenance
- evidence class
- trust/status
- supersession
- correction
- derived vs authoritative state
- human approval boundaries
- prevention of agent-generated fiction becoming project truth

Immediate research objective: determine which mechanisms can be reused or adapted, not install a framework merely because it exists.

## 10. GitHub capability established

Repository: MPrakashDec/market-profile-sync

Experimental branch: mp-expert-v0

ChatGPT's connected GitHub surface was tested for repository mutation. Proven operations included create file, update file, delete file, and lower-level blob/tree/commit/ref operations.

Temporary capability-test artifacts were created, fetched, updated, and deleted; they are not intended as project content.

The MP branch contains an initial v0 skeleton:
- mp_expert/__init__.py
- mp_expert/engine.py
- mp_expert/model.py

This v0 is intentionally incomplete and must not be mistaken for the finished MP reasoning engine.

## 11. Current research frontier

The next work should focus on the **control plane that lets different chats/agents recover the same project situation**, while continuing MP engine research in parallel.

Research questions:
1. What is the minimum durable situation record needed for a new session to orient correctly?
2. Which parts should be Markdown/Git-native vs structured DB/state?
3. How should current state differ from historical evidence?
4. How should supersession and correction work?
5. How can an agent prove it read the situation index before acting?
6. How can repository topology and project memory be compiled into bounded working context?
7. How do we prevent stale memory from becoming current truth?
8. How do live iDSS state, replay state, project state, and agent-session state remain separate?
9. Which external mechanisms are worth borrowing, and which conflict with iDSS's evidence/provenance model?
10. How should multiple reasoning models communicate with the persistent iDSS state and with the coding agent without any one model becoming the authority?

The desired long-term loop is:

**LIVE MARKET → deterministic observation/state engine → evidence ledger → event/change → hypothesis generation → historical case retrieval → replay/backtest → failure analysis → hypothesis revision → more replay/out-of-sample → validated mechanism → paper/live observation → only eventually execution layer**

Execution remains a future gated layer, not the current objective.

## 12. Session-start protocol

A new ChatGPT or agent session should treat this file as the orientation anchor, then verify current facts against the repository and relevant evidence.

Do not assume this file is perfectly current. It is a map of the situation and continuity mechanism, not ground truth.

Before implementation:
**Orient → verify → identify failure locus/frontier → research if needed → act → test → record result.**

When the project materially changes, update this index so the next chat does not have to reconstruct the project from scratch.


## 13. ChatGPT ↔ Antigravity Git bridge

A repository-native asynchronous bridge is now installed at `docs/agent-bridge/`.

- ChatGPT/reasoning sessions can write executable research or verification requests to `docs/agent-bridge/inbox/`.
- Antigravity discovers the bridge through `.agents/rules/idss-chatgpt-bridge.md` and the execution procedure in `.agents/skills/idss-chatgpt-bridge/SKILL.md`.
- Antigravity writes evidence-backed results to `docs/agent-bridge/outbox/` and commits/pushes them.
- A later ChatGPT session can fetch the result from Git and continue from the returned evidence.
- The protocol uses explicit request IDs and states (`PENDING`, `COMPLETED`, `BLOCKED`, `SUPERSEDED`) rather than treating chat history as the source of truth.

This is an asynchronous message/state channel, not live RPC. Remote changes must be synchronized into the local Antigravity workspace; local results must be committed/pushed before ChatGPT can read them.

The first live verification request is `docs/agent-bridge/inbox/2026-10-02-chatgpt-bridge-bootstrap-001.md`.


## 14. Prospective-evaluation boundary research checkpoint — 2026-10-04

### Verified repository evidence
Inspection of mp-expert-v0 shows the current mp_expert/engine.py implementation is **pull / preloaded-history / caller-indexed replay**, not an enforced prospective event boundary.

Key facts:
- AuctionEngine.__init__ stores self.bars = sorted(list(bars), ...), so the engine object can retain the complete history.
- snapshot_at(i) calculates from self.bars[:i+1]. This is a calculation convention, not an access-control boundary.
- A caller holding the engine can directly access future bars through engine.bars; therefore future data is physically available to the caller/strategy.
- AuctionSnapshot itself contains domain/scalar output and does not retain the full self.bars list; the primary demonstrated exposure is the engine object.
- The docstring claim that replay and live use the same snapshot_at() path is not sufficient evidence of a live push/event consumer. Repository inspection did not find a demonstrated on_tick, process_event, update(bar), or equivalent prospective consumer in this branch.
- No MP-specific tests were found in the inspected likely test paths.

### Consequence
Do **not** immediately rewrite/delete snapshot_at() or the existing v0. First prove the boundary failure and compare an event-consumer experiment against the existing calculations.

Recommended experiment sequence:
1. Add an explicit exploit proof showing future data is accessible through engine.bars.
2. Build a thin experimental event stream/consumer alongside the existing engine; do not rewrite the v0 yet.
3. Feed identical historical bars one event at a time and compare event-consumer output against snapshot_at(i) for every index.
4. If outputs match, the calculation logic may already be event-local and the primary defect is the information boundary.
5. If they diverge, locate the first divergence and identify the hidden pull dependency before refactoring.
6. Only then consider making update(bar) -> snapshot the canonical prospective transition path.
7. After that, test ambient external future access (global stores, caches, filesystem, network, module state). Removing self.bars alone is **not** a complete security boundary.

### Security-model conclusions
- A direct future-read test should initially be treated as an **exploit demonstration**, not a passing security test. The eventual boundary test should expect denial/provenance failure.
- Python metadata/taint attached to arrays/DataFrames is not a security boundary because arbitrary code can strip metadata, copy raw values, serialize them, or obtain future data elsewhere.
- For adversarial prospective evaluation, a push/event-stream contract is structurally safer than a caller-controlled as_of=t query, but process/address-space isolation may still be required.
- A true prospective runner should ideally receive only the current event, use a runtime-owned clock, expose no arbitrary historical query API, and have no future target object resident in its process.
- Physical process isolation does not automatically solve statistical governance or hidden search; execution integrity and research governance are separate concerns.

### Research-governance conclusions
- Virgin OOS is not virgin if an agent can generate/select many candidates against the same target data and submit only the winner. Emitted candidate count is not necessarily true search volume.
- Multiple-testing/search accounting must be deterministic, precommitted or otherwise auditable, and immutable/versioned before prospective validation.
- K_eff / spectral-decomposition correction is a possible methodology, not established universal truth. The correction method, estimator, dependence assumptions, and protocol version must be frozen before evaluation; the agent must not choose them after seeing results.
- Discovery/reconstruction and prospective evaluation are different information regimes. Hindsight is allowed for reconstruction/descriptive state, but prospective claims require a separately enforced no-look-ahead regime.
- A clean architecture likely uses a canonical event transition path for live and replay, with hindsight/reconstruction as a sidecar observer over replay output rather than a second competing state engine. This remains a design hypothesis until tested against the actual implementation.

### Immediate frontier
The next justified action is **runtime probing, not architecture debate**:
- prove direct future accessibility;
- build the minimal event-consumer comparison;
- identify the first divergence or establish equivalence;
- then probe ambient future-data channels;
- only afterward decide the refactor/isolation boundary.

This checkpoint is evidence from repository inspection as of 2026-10-04, not a claim that the wider Des workspace has no additional implementation.
