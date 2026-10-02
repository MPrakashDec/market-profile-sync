# Fragmented Persistent Memory Pipeline

Status: active direction, 2026-10-02

## Purpose

Do not collapse the iDSS project's growing history into one giant persistent-memory file. Build a layered, fragmented system that can grow while actual research continues.

## Pipeline

Historical chat/source corpus
-> artifact memories
-> knowledge memories
-> selected persistent-memory fragments
-> operational rules / skills where knowledge becomes reusable procedure

## Working rules

- Process historical material in chunks rather than attempting a one-shot reconstruction.
- Preserve provenance so a memory fragment can be traced back to its source/artifact.
- Repeated or contradictory chats should be synthesized rather than copied forward indefinitely.
- Redundant, superseded, or obsolete material may be removed from the persistent layer while remaining recoverable in source/artifact layers.
- Let useful categories and folder structure emerge from the corpus; do not impose rigid topic silos prematurely.
- Keep knowledge distinct from instructions/rules/skills. A discovered fact does not automatically become an operational rule.
- Persistent memory is the small working layer, not the complete historical archive.
- The historical corpus remains valuable for later retrieval and re-analysis.
- Do not delay actual iDSS research while designing this architecture.

## Parallel agent workflow

ChatGPT can extract/synthesize research and write durable artifacts to GitHub. Antigravity can read those artifacts, compare them against its local conversation history and project state, perform local investigation/execution, and write reconciliation/results back through the established Git bridge.

The bridge is a coordination/state channel, not a claim that either agent is the sole source of truth.

## Immediate direction

Begin processing the chat_history corpus in chunks into artifact memories while continuing substantive iDSS research in parallel. After enough artifacts exist, synthesize them into knowledge memories and then select only what needs to remain persistent.