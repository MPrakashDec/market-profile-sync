# Market Profile Landscape Research Direction

## Status

Research direction recorded 2026-10-03.

This document is a research constraint, not an architectural conclusion.

## Core premise

Market Profile / Auction Market Theory appears potentially powerful as a structural representation of the developing auction.

However, iDSS must not assume that Market Profile is the correct final foundation merely because it is familiar or useful to the human researcher.

The purpose of the next landscape scan is to discover what is already known and implemented before deciding what iDSS should become.

## Critical research question

The important question is not:

> What Market Profile software exists?

It is:

> How far has existing work gone toward computationally reconstructing the auction and discovering changing states, transitions, recurring phenomena, and competing explanations without simply encoding a trader's existing interpretation?

## Scope of landscape scan

Search systematically across:

1. Market Profile / Auction Market Theory implementations
2. TPO and volume-profile systems
3. Footprint / order-flow / delta / DOM / liquidity systems
4. Market-microstructure research
5. Computational auction reconstruction
6. Options OI / IV / Greeks / dealer-positioning systems
7. Quantitative research modelling market states and transitions
8. AI systems performing market-structure research
9. Products attempting automated auction interpretation rather than visualization alone
10. Research/evidence systems that could preserve discoveries and competing explanations

## Capability decomposition

Every candidate should be classified by what it actually does:

- visualization / analytics primitives
- deterministic state reconstruction
- structural-event detection
- state-transition modelling
- recurring-phenomenon discovery
- hypothesis generation
- competing explanation generation
- replay / falsification
- look-ahead-safe validation
- out-of-sample validation
- persistent research/evidence memory
- provenance and correction/supersession

Do not treat a sophisticated visualization product as equivalent to an autonomous auction-research system.

## Anti-contamination requirement

Prakash's current market interpretations must not become hidden requirements for the discovery engine.

Human observations and hypotheses may be recorded separately, but independent research must be able to reconstruct the same phenomena without being seeded by those hypotheses.

Desired separation:

RAW MARKET DATA
→ independent reconstruction
→ states / transitions
→ recurring phenomena
→ competing explanations
→ replay / falsification
→ research findings
→ human review

Separate human track:

HUMAN OBSERVATION
→ HUMAN HYPOTHESIS
→ later comparison with independent findings

The system must remain capable of producing:

- confirmation of something already observed;
- rejection of a current human explanation;
- discovery of an explanation or phenomenon not previously considered.

## Output requirement

The landscape scan should produce a bounded candidate set and gap map.

It should not become an ever-growing list of repositories.

For every serious candidate, record:

- what it actually provides;
- evidence for the claim;
- maturity;
- limitations;
- license / reuse constraints where relevant;
- whether it is visualization, reconstruction, discovery, or research infrastructure;
- mechanisms potentially reusable by iDSS;
- mechanisms that conflict with iDSS's deterministic/provenance/anti-look-ahead requirements.

Existing leads such as Quantower, GoCharting, Auction Edge, and recent academic AMT/state-representation work are research leads only. They require independent verification before adoption or architectural conclusions.

## Epistemic status

Market Profile as a powerful iDSS foundation: **HYPOTHESIS**.

Existing external mechanisms: **RESEARCH LEADS** until independently verified.

No external product, repository, paper, model, or human interpretation becomes project truth merely by being mentioned or implemented.

The goal is to learn what the research community and existing systems already know before constraining iDSS's future architecture.
