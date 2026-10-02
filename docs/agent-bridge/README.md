# ChatGPT ↔ Antigravity Agent Bridge

This directory is the durable exchange layer between reasoning sessions that can read/write the GitHub repository and the local Antigravity agent that can execute against the workstation.

## Flow

```
ChatGPT
  |
  | writes request
  v
Git remote
  |
  | sync/pull
  v
Antigravity
  |
  | reads request + executes locally
  v
docs/agent-bridge/outbox/
  |
  | commit + push
  v
Git remote
  |
  | ChatGPT reads result
  v
ChatGPT
```

The bridge is deliberately boring. It is not a second project database and it is not an authority layer.

- `inbox/` = requests waiting for local execution
- `outbox/` = durable execution/research results
- `README.md` = protocol orientation
- `.agents/rules/idss-chatgpt-bridge.md` = automatic Antigravity discovery
- `.agents/skills/idss-chatgpt-bridge/SKILL.md` = execution procedure

## State model

`PENDING -> COMPLETED`

or

`PENDING -> BLOCKED`

A request is immutable in meaning. Status changes and factual corrections must be explicit.

## Why Git is useful here

Git is unusually well suited to this particular gap because the two sides already have asymmetric capabilities:

- ChatGPT can reason/research and write repository files through GitHub.
- Antigravity can operate the local workspace, browser, terminal, databases and other local resources.
- Both can exchange ordinary text files and commit history.
- Neither side has to pretend the other has its tools.

The bridge also gives ChatGPT a durable place to leave research notes and gives the agent a durable place to return execution evidence.

## Important limitation

The bridge cannot make ChatGPT continuously project-aware. It creates a reliable recovery path: current situation + pending work + verified results + Git history. ChatGPT still has to read those artifacts, and Antigravity still has to sync the repository.

Do not turn every chat message into memory. Store durable findings, decisions, failed approaches, corrections, and execution results.
