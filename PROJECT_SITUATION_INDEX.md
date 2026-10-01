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

Historical workspace: E:\\A New folder\\Des

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

## 4. Market Profile / Auction Reasoning direction

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

## 5. Live data lineage

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

## 6. Agent-control / project-memory requirements

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

## 7. Public ecosystem research already performed

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

## 8. Mechanism decomposition

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

## 9. GitHub capability established

Repository: MPrakashDec/market-profile-sync

Experimental branch: mp-expert-v0

ChatGPT's connected GitHub surface was tested for repository mutation. Proven operations included create file, update file, delete file, and lower-level blob/tree/commit/ref operations.

Temporary capability-test artifacts were created, fetched, updated, and deleted; they are not intended as project content.

The MP branch contains an initial v0 skeleton:
- mp_expert/__init__.py
- mp_expert/engine.py
- mp_expert/model.py

This v0 is intentionally incomplete and must not be mistaken for the finished MP reasoning engine.

## 10. Current research frontier

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

## 11. Session-start protocol

A new ChatGPT or agent session should treat this file as the orientation anchor, then verify current facts against the repository and relevant evidence.

Do not assume this file is perfectly current. It is a map of the situation and continuity mechanism, not ground truth.

Before implementation:
**Orient → verify → identify failure locus/frontier → research if needed → act → test → record result.**

When the project materially changes, update this index so the next chat does not have to reconstruct the project from scratch.
