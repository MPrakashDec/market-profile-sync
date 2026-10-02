# Git-backed ChatGPT ↔ Antigravity Bridge Research — 2026-10-02

## Question

Can ChatGPT, without local-agent execution capability, use the GitHub repository as a durable exchange layer to:

1. write a research/verification task;
2. have Google Antigravity discover and execute it locally;
3. have Antigravity write the real execution result back into the repository;
4. let a later ChatGPT session read that result and regain project situational awareness?

## Conclusion

Yes, with an important boundary: this is an **asynchronous Git-backed message/state channel**, not direct agent-to-agent RPC.

The capability is unusually well matched to the current iDSS setup because ChatGPT and Antigravity have complementary tool access:

- ChatGPT can perform external research, reason over repository state, and write repository files through the GitHub connector.
- Antigravity can operate the local Windows workspace, terminal, browser, local databases/processes, and project files.
- Git provides a shared durable artifact channel visible to both sides.
- The result can carry execution evidence back to ChatGPT without pretending ChatGPT itself performed the local operation.

## Evidence from current Antigravity documentation

Google Antigravity currently documents three mechanisms that matter:

### Rules

Antigravity automatically discovers workspace rules, including:

- `.agents/rules/*.md`
- `.agents/AGENTS.md`
- `AGENTS.md`
- `GEMINI.md`

Rules are injected according to scope and can be always-on or selectively activated.

Source:
https://antigravity.google/docs/rules/

### Skills

Workspace skills live under:

`.agents/skills/<skill-folder>/SKILL.md`

Antigravity sees skill names/descriptions at conversation start, reads the full skill when relevant, and then follows its procedure. Skills can include scripts and resources.

Source:
https://antigravity.google/docs/skills?app=antigravity-ide

### Workflows

Antigravity workflows are Markdown-defined sequences for repeatable agent tasks. The documentation currently says workflows are being migrated/deprecated in favor of skills by November 1, 2026.

Source:
https://antigravity.google/docs/ide/workflows/

Therefore the bridge should use **rules + skills**, not build a new workflow system around the soon-to-be-deprecated workflow mechanism.

## Important empirical caution

Repository context files are not magic project memory.

Two 2026 empirical studies found that repository context files do not reliably improve coding-agent task correctness. One controlled study across Claude Code and Codex found no measurable correctness improvement from full or selective AGENTS.md context, although context could improve process efficiency on some tasks. Another study found no task-success improvement and increased inference cost.

Sources:

- https://arxiv.org/abs/2607.27250
- https://arxiv.org/abs/2602.11988

This changes the design target.

The bridge should **not** try to stuff the entire project into an always-on prompt. It should make the right durable state discoverable, bounded, evidence-backed, and operationally retrievable.

## Relevant existing ecosystem mechanisms

Research found several useful patterns:

### Agent Handoff

AniruddhaHumane/handoff uses file-backed snapshots and summaries to transfer work across Codex, Claude and parallel agent workflows.

Useful pattern:
- explicit handoff object
- compact summary
- durable files
- next agent reads the handoff instead of reconstructing the conversation

Source:
https://github.com/AniruddhaHumane/handoff

### Cross-Agent Memory

VladimirGutuev/cross-agent-memory uses Git-tracked Markdown as shared project memory across Codex, Claude Code, Kimi Code, Antigravity and other agents.

Useful patterns:
- compact memory index
- topic files
- active handoffs
- verified evidence
- volatile/current facts treated as dated checkpoints
- benchmark retrieval before buying a more complex index

Source:
https://github.com/VladimirGutuev/cross-agent-memory

### Other memory systems

Agent-memory projects demonstrate that durable memory can be separated into lifecycle-managed records, searchable topics, temporal state, and audit history. They are useful research references but are not necessary for the first bridge implementation.

## Design decision for iDSS

Do **not** install a third-party memory framework merely to solve the immediate cross-model communication problem.

Start with a small Git-native protocol:

```
docs/agent-bridge/
  README.md
  inbox/
    <request-id>.md
  outbox/
    <request-id>.md
```

and:

```
.agents/
  rules/
    idss-chatgpt-bridge.md
  skills/
    idss-chatgpt-bridge/
      SKILL.md
```

### Request

A request is immutable in meaning and has explicit frontmatter:

```yaml
id: unique-request-id
status: PENDING
created_by: chatgpt
created_at: timestamp
priority: normal
scope: research|implementation|verification
```

### Result

The corresponding result records:

- actual local observations
- calculations
- inferences
- unknowns
- commands/tools run
- files changed
- tests/verification
- failures/dead ends
- evidence paths
- branch/commit information

This is deliberately closer to an evidence ledger than to a chat transcript.

## Why this is stronger than simply writing a README

A README is passive documentation.

The bridge has an operational state transition:

```
PENDING
   |
   v
local agent discovers request
   |
   v
verify -> execute -> record
   |
   +---- BLOCKED
   |
   v
COMPLETED
```

The result is therefore both:

- a message to the next reasoning session;
- a durable record of what actually happened.

## Why Git is particularly useful here

Git provides properties that ordinary model memory does not:

- commit identity
- chronological history
- diffs
- rollback
- branch isolation
- immutable historical objects
- human inspectability
- cross-machine synchronization
- compatibility with repository-aware agents

It also naturally separates **claim** from **verification**.

ChatGPT can write:

> investigate X

The local agent can return:

> X was observed in file Y; command Z produced result Q; claim A was false.

That distinction is central to iDSS.

## Critical limitation

Git does not remove the synchronization boundary.

The actual loop is:

```
ChatGPT
  -> GitHub commit
  -> local git sync
  -> Antigravity reads request
  -> Antigravity executes locally
  -> result committed/pushed
  -> ChatGPT fetches result
```

Therefore:

- a ChatGPT commit does not automatically appear in the local workspace;
- an Antigravity local change is invisible to ChatGPT until committed/pushed or otherwise exposed;
- the bridge cannot provide real-time process awareness;
- the bridge cannot give ChatGPT access to local browser sessions, Windows processes, databases or Des files;
- the bridge cannot make an LLM intrinsically remember hidden context.

What it can do is make **the evidence needed to recover that context durable and machine-readable**.

## Project-awareness implication

The most useful long-term architecture is not:

```
ChatGPT memory
+ Antigravity memory
+ random notes
```

It is:

```
                 persistent project state
                         |
        +----------------+----------------+
        |                |                |
      evidence         current          history
        |              situation          |
        |                |                |
        +----------------+----------------+
                         |
                  bounded retrieval
                    /           \
              ChatGPT         Antigravity
              reasoning       execution
                    \           /
                     contributions
                         |
                 verified Git state
```

The repository can therefore become one durable **control/evidence plane**, while native model memories remain secondary caches.

## Current implementation

Installed on `main`:

- `.agents/rules/idss-chatgpt-bridge.md`
- `.agents/skills/idss-chatgpt-bridge/SKILL.md`
- `docs/agent-bridge/README.md`
- `docs/agent-bridge/inbox/2026-10-02-chatgpt-bridge-bootstrap-001.md`

Also updated:

- `PROJECT_SITUATION_INDEX.md`

The bootstrap request deliberately asks Antigravity to perform a harmless local verification and return evidence rather than merely acknowledge the protocol.

## What this proves so far

**Proven from the ChatGPT side:**

- repository is writable;
- repository permissions include push;
- bridge rule/skill can be committed;
- request can be committed to the inbox;
- project situation index can be updated;
- ChatGPT can subsequently fetch files and commit history from the same repository.

**Not yet proven from the ChatGPT side alone:**

- that the specific Antigravity installation currently opens this workspace with the new rule;
- that the local workspace has synchronized the request;
- that Antigravity will execute the request;
- that Antigravity can push its result back;
- that the complete round trip works end-to-end.

Those are deliberately left to the actual local agent rather than claimed from repository writes.

## Current test request

`docs/agent-bridge/inbox/2026-10-02-chatgpt-bridge-bootstrap-001.md`

The request asks Antigravity to:

1. read the situation index;
2. read the bridge rule and skill;
3. verify local Git state;
4. perform a harmless local verification;
5. write an evidence-backed result;
6. update status;
7. commit and push.

If that result appears in `docs/agent-bridge/outbox/`, the first end-to-end bridge has been demonstrated.

## Design principles retained from iDSS

The bridge follows existing iDSS constraints:

- information before transport;
- no fabricated system boundaries;
- OBSERVED / CALCULATED / INFERRED / UNKNOWN separation;
- historical vs current distinction;
- negative knowledge retained;
- no clean-room replacement of messy historical work;
- persistent state should outlive any particular reasoning model;
- model outputs are contributions to the state layer, not the state-of-truth.

## Bottom line

The answer to the original architectural question is **yes**.

Git can serve as a surprisingly effective low-level memory/message substrate between ChatGPT and Antigravity because it solves exactly the capability gap: ChatGPT can write durable instructions/research, while Antigravity can execute locally and return evidence.

The important part is not the Markdown itself. The important part is the **closed request → execution → evidence → commit → retrieval lifecycle**.

The bridge should remain small until actual use demonstrates where retrieval, concurrency, stale state, or volume become the bottleneck. Only then should it acquire databases, indexes, MCP servers, or more elaborate memory machinery.
