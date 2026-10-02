---
name: idss-chatgpt-bridge
description: Processes pending ChatGPT research or execution requests stored in docs/agent-bridge/inbox, verifies them against the live iDSS repository, executes justified work, and writes a durable evidence-based result to docs/agent-bridge/outbox.
---

# iDSS ChatGPT Bridge

## Purpose

This skill makes Git the durable message/state channel between ChatGPT and the local Antigravity agent.

ChatGPT can write a request to the repository but cannot execute local commands, inspect E:\A New folder\Des, or observe Antigravity's local browser/process state. Antigravity can execute those operations and write the resulting evidence back to Git. A later ChatGPT session can fetch that result.

## Protocol

### 1. Orient

Read, in this order:

- `PROJECT_SITUATION_INDEX.md`
- the selected pending request in `docs/agent-bridge/inbox/`
- only the additional project files needed for that request

Do not reconstruct the whole project from the request alone.

### 2. Verify

Separate:

- claims supplied by the request;
- facts observed in the current workspace;
- calculations performed by the agent;
- inferences;
- unresolved/unknown items.

If the request points to historical work, preserve the historical/current distinction.

### 3. Execute

Perform the requested research, inspection, coding, experiment, or verification when it is within the local agent's available capabilities.

Do not stop at a plan when the request asks for execution.

Do not ask the human to relay information that can be obtained from the workspace, repository, tools, or commands available to the agent.

If execution is impossible, record exactly why.

### 4. Record

Create:

`docs/agent-bridge/outbox/<request-id>.md`

The result should contain:

- request ID
- source
- agent/session identifier if available
- started/completed timestamps
- repository branch and starting/ending commit when available
- concise outcome
- OBSERVED / CALCULATED / INFERRED / UNKNOWN sections as applicable
- commands/tools actually used
- files created/changed
- tests/verification actually run
- failures/dead ends
- remaining uncertainty
- links/paths to evidence
- exact next machine-action only if execution genuinely remains incomplete

Do not write imagined results.

### 5. Close

Update the request's frontmatter:

- `PENDING` -> `COMPLETED` after successful result verification
- `PENDING` -> `BLOCKED` when a concrete blocker prevents completion
- `PENDING` -> `SUPERSEDED` only when a newer request explicitly replaces it

Never delete a completed request as a cleanup step.

## Request format

Use Markdown with YAML frontmatter:

```yaml
---
id: unique-request-id
status: PENDING
created_by: chatgpt
created_at: 2026-10-02T00:00:00Z
priority: normal
scope: research|implementation|verification
---
```

The body is the complete task.

## Result integrity

The result is evidence from the local agent, not a continuation of the ChatGPT prompt.

If a result is later corrected, create a correction record or update the result with an explicit correction section. Do not erase the historical claim without documenting the correction.

## Why this is intentionally file/Git based

The first version must be inspectable without a database or MCP dependency. Git gives:

- durable history
- diffable changes
- commit identity
- rollback
- cross-machine synchronization
- human inspection
- access by any repository-aware agent

A future structured store can be added behind this protocol if retrieval volume requires it. It should not replace the durable evidence trail.

## Critical operational detail

A remote Git commit is not automatically visible to the local Antigravity workspace. The local workspace must fetch/pull/sync the repository before the agent can see newly written bridge requests. Likewise, ChatGPT can only see an agent result after the agent has committed/pushed it to the remote repository (or otherwise made it available through the connected repository surface).

This is an asynchronous message bus, not a live RPC channel.
