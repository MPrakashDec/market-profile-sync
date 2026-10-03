# Discovery-First Research Protocol

## Status

Research constraint recorded 2026-10-03.

This document governs how iDSS landscape research should be conducted. It is a process constraint, not an architecture conclusion.

## Failure mode to prevent

A recurring failure mode is:

USER OBSERVATION
→ assistant constructs an interpretation
→ interpretation becomes the problem definition
→ search is optimized around that interpretation
→ relevant work outside that vocabulary disappears.

This is unacceptable for discovery work whose purpose is to find concepts, mechanisms, systems, or disciplines that neither the user nor the assistant has already named.

## Discovery search vs confirmation search

### Discovery search

Start from the underlying problem rather than the user's current terminology or preferred solution.

Search broadly across:
- multiple vocabularies for the same underlying problem;
- adjacent disciplines;
- different technical traditions;
- academic and practitioner work;
- software, protocols, products, papers, datasets, and research systems;
- unexpected neighboring categories.

The objective is to discover candidates that can change the problem definition itself.

### Confirmation / implementation search

Only after the landscape and candidate concepts are understood should search narrow toward:
- implementation details;
- repositories;
- APIs;
- concrete products;
- integration mechanisms;
- engineering choices.

Do not confuse this with discovery.

## iDSS application

For example, do not reduce:

> "How can a machine understand an evolving market auction?"

to:

> "How do we automate Prakash's Market Profile method?"

Market Profile may emerge as one representation among several. The discovery process must be able to find alternatives, adjacent representations, or deeper mechanisms that were not part of the original framing.

Likewise, a question about shared AI context should not automatically become an "agent memory" search. Search the broader underlying problem: cross-agent continuity, shared working context, versioned knowledge, multi-agent collaboration, project-state persistence, provenance, etc.

## Required research loop

USER OBSERVATION / RAW PROBLEM
→ broad multi-vocabulary landscape
→ adjacent-domain expansion
→ unexpected candidate discovery
→ forensic inspection
→ capability / mechanism extraction
→ comparison with existing iDSS understanding
→ bounded candidate set + gap map
→ only then implementation/architecture decisions

## Human knowledge must not become the search boundary

Prakash's observations and hypotheses are valuable research specimens, but they must not silently become:
- requirements;
- ontology;
- search vocabulary;
- feature lists;
- validation criteria;
- architecture assumptions.

They should be preserved as a separate human track and compared later with independent discovery.

Desired outcomes include:
1. confirmation of an existing human observation;
2. rejection or qualification of the human explanation;
3. discovery of something neither the human nor the assistant had previously considered.

Outcome 3 is a primary success condition, not an edge case.

## Operational rule

Before narrowing a research question, explicitly ask:

> What other vocabularies, disciplines, mechanisms, or problem formulations could describe the same underlying phenomenon?

If that question has not been explored, the research is not yet discovery-complete.

## Epistemic status

This protocol is a process rule for research, not a claim about any particular external system or technology.
