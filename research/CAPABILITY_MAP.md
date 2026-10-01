# Agent Capability & Research Map

Updated: 2026-10-01

## Proven in this ChatGPT GitHub surface

- Read repository metadata and permissions.
- Enumerate repositories visible to the linked GitHub account.
- Access the user's repositories: Dashboard, jarvis, opc, Fuel, market-profile-sync, Chatgpt, gpt, Dwork.
- Create branches.
- Create Git blobs, trees and commits.
- Create/update/delete repository files.
- Fetch files and repository contents.
- Compare refs/commits.
- Search public repositories and repository code where indexed.
- Inspect issues, pull requests and CI/workflow resources through exposed read APIs.
- Exposed write surface also includes PR creation/updates/reviews/merge, issue mutations and workflow reruns; these are capabilities exposed by the connector but not all have been independently tested here.

## Important boundary

Repository visibility and tool exposure are not the same as permission. The write lifecycle was actually tested on this branch: create -> read-back -> update -> delete. Higher-level create_file also works after authorization.

## Persistent project-state candidates

Use Git as durable project memory for artifacts that should be versioned and reviewable. Prefer explicit files such as:

- PROJECT_SITUATION_INDEX.md — current known state, active work, blockers, negative knowledge, next probes.
- CAPABILITY_MAP.md — proven/unproven tool and agent capabilities.
- RESEARCH_REGISTER.md — external projects, mechanisms, evidence, provenance and applicability.
- DECISION_LEDGER.md — durable architectural decisions and reversals.
- NEGATIVE_KNOWLEDGE.md — approaches tested and rejected, with reasons.
- HANDOFF.md — compact session restart state.

Do not treat these as hidden memory. They are explicit project memory and can be inspected, diffed and corrected.

## External mechanisms worth studying

- claude-mem: persistent cross-session observation capture, semantic compression/search, project context files, citations.
- Aider: repository map for structural codebase awareness; Git-native change tracking; automated lint/test loop.
- AGENTS.md: portable repository-local agent instruction/context convention.
- Superpowers: composable skills plus spec/plan/subagent/TDD workflow; useful as orchestration ideas, not as an iDSS dependency.
- Antigravity's existing skills/rules/MCP/project surfaces: already present in the user's local environment and should be audited before adding replacements.

## iDSS-specific interpretation

The target is not generic agent memory. iDSS needs situational awareness that distinguishes:

1. durable facts;
2. current project state;
3. hypotheses;
4. decisions and their rationale;
5. negative knowledge/failure modes;
6. unresolved questions;
7. historical evidence/provenance;
8. current work frontier;
9. capability boundaries of the tools/agents actually available.

A memory layer should retrieve the right context without becoming a second source of truth. Deterministic project artifacts remain authoritative.
