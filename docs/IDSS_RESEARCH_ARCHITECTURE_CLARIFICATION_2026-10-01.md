# iDSS Research Architecture Clarification — 2026-10-01

## Status

Durable architectural clarification from the 2026-10-01 research discussion.

This document records the intended research model. It is not a claim that the mechanisms described below are already validated trading strategies.

## Core idea

iDSS should not be reduced to a manual trading assistant, a single strategy, or a system that waits for Prakash to ask the right questions.

The system should proactively observe market data, reconstruct deterministic state, identify significant moves, research what happened, discover possible ways those moves could have been captured, test those possibilities, retain the resulting knowledge, and continuously improve its own research machinery.

Prakash is the conversational human at the boundary. He can ask questions, challenge results, and explore the system's findings, but the research loop should not depend on him knowing what question to ask next.

The intended relationship is:

    Market/data
      -> deterministic state reconstruction
      -> move/event identification
      -> broad research and candidate discovery
      -> progressive filtering and deep research
      -> theoretical hypothesis/specification
      -> replay implementation
      -> time-causal testing
      -> evidence/negative knowledge
      -> improved knowledge and research machinery
      -> proactive information/guidance to Prakash
      -> repeat

## Research starts from actual moves

For an observed historical move, the research process is deliberately allowed to know that the move happened.

Example:

- A significant move occurs during the 10:05 5-minute candle.
- The research system freezes the relevant information boundary.
- It asks: what information existed before the move that might have allowed a system to anticipate or capture it?
- It investigates many possible lenses rather than assuming one domain is the answer.

Potential lenses include:

- Market Profile / auction market theory
- order flow / market microstructure
- options structure
- first-, second-, and third-order Greeks where data supports them
- volatility and positioning
- overnight context
- previous-session context
- pre-market information
- macro/news/event context
- opening structure
- cross-asset information
- academic/research literature
- relevant open-source implementations
- other mechanisms discovered during research

The list is intentionally open-ended.

## Broad candidate discovery before filtering

A single move may produce dozens of candidate explanations or capture mechanisms, potentially around 50 or more.

The system should not assume that the first search result or first plausible explanation is correct.

A broad research pass can produce many candidates. Additional passes can produce more. Candidates are then progressively screened and deep-researched.

Conceptually:

    broad searches
        -> candidate pool
        -> research each candidate
        -> discard weak/irrelevant candidates
        -> retain plausible candidates
        -> deeper research
        -> test relationships and evidence
        -> small surviving set
        -> encode for replay

The process resembles staged candidate selection: many candidates enter, successive rounds filter them, and rejected candidates remain recorded rather than disappearing.

## Research candidates are not assumed to generalize

A candidate that appears useful for Move 1 is not automatically useful for Move 2.

For example:

    Move 1: candidate A works
    Move 2: candidate A fails
    Move 2: candidate B works
    Move 3: A and B fail, C works

This is useful information.

The unit of research is therefore the move/event and its surrounding state, not an assumed universal strategy.

The system should capture each move independently and accumulate the resulting evidence across moves and days.

## No hardcoding or cheating

A research hypothesis may be discovered with hindsight. That is permitted during the exploratory discovery phase.

However, once a hypothesis is replayed as a historical system, the replay must obey a strict information boundary.

If the question is:

> Could the system have captured the move before the 10:05 candle closed?

then the replay engine may use only information that was actually available by that historical timestamp.

It must not use:

- later candles
- the eventual high/low
- later option-chain changes
- later order flow
- the eventual profile
- future research discoveries
- any other information that was unavailable at the decision boundary

The system must preserve provenance and timestamps sufficiently to establish what was knowable when.

## Two clocks

The architecture should explicitly distinguish:

### Research clock

The researcher knows the historical outcome and may use it to decide what is worth investigating.

This is the discovery laboratory.

### Historical market clock

The replayed system is transported to the historical timestamp and sees only the information that would have existed at that time.

This is the causal experiment.

The first clock may use hindsight for candidate discovery. The second must not.

## Knowledge must also respect historical time

When replaying historical days, knowledge discovered from future days must not leak backward.

Conceptually:

    Day 1 research
        -> knowledge available to Day 2

    Day 2 research
        -> knowledge available to Day 3

    Day 3 research
        -> knowledge available to Day 4

and so on.

The system should retain what it knew, when it knew it, and which conclusions were available at each point.

## Discovery is not validation

The early research stage is intentionally permissive.

It may:

- generate many hypotheses
- investigate unusual mechanisms
- combine domains
- search broadly
- inspect external research
- use hindsight to identify promising questions
- discover mechanisms that initially look like curve fitting

That is the laboratory.

Once a mechanism becomes promising, it enters a stricter validation track.

Later validation can include:

- unseen historical periods
- walk-forward testing
- out-of-sample evaluation
- realistic execution assumptions
- multiple-testing controls
- robustness analysis
- PBO / Reality Check-type methods where appropriate

The system should not confuse a successful hindsight-driven discovery with a validated trading edge.

## Candidate lifecycle and negative knowledge

Candidates should have a persistent lifecycle, for example:

- discovered
- interesting
- under research
- provisionally supported
- rejected
- insufficient data
- too late to be actionable
- useful only in a particular regime
- useful only as confirmation
- useful only in combination
- implementation failure
- data-quality failure
- unexpectedly promising
- promoted to replay
- promoted to validation
- invalidated
- revisited

Rejected candidates and negative findings remain valuable knowledge.

A mechanism that does not explain a short-horizon intraday move may still be useful for another timeframe or market regime.

## Replay is where candidates have to show up for work

After research has narrowed the field, the system writes code/specifications for the surviving hypotheses and replays the actual historical event.

The result may contradict the research.

A candidate can look excellent in theory and fail in replay because:

- its signal appears too late
- its supposed evidence was not actually available
- it produces too many false positives
- it depends on hindsight
- the implementation cannot reconstruct the required state
- the relationship disappears under realistic data
- it works for one move but not another

Conversely, replay may reveal an unexpectedly useful mechanism that was not prominent in the initial research. That should trigger another research cycle.

The loop therefore works in both directions:

    Research -> hypothesis -> code -> replay -> discovery

and:

    Replay -> unexpected result -> hypothesis -> research -> new code

## Progressive accumulation

As more moves and days are processed, the system may accumulate hundreds or thousands of findings.

These are not necessarily hundreds of strategies.

They may be findings such as:

- a relationship that explains one move but not another
- a mechanism that works only after a particular auction condition
- a signal that consistently appears too late
- a candidate that is useful only for confirmation
- a candidate that works only in a particular volatility regime
- two apparently different mechanisms that may be manifestations of one state
- a mechanism that repeatedly fails
- a new interaction between Market Profile, order flow, and options structure

The accumulated research becomes a persistent market knowledge base.

## Long-term system behavior

The eventual iDSS should continuously:

1. observe and reconstruct market state
2. identify meaningful events and transitions
3. proactively explain what happened
4. generate broad research questions without waiting for Prakash
5. search and research across multiple domains and sources
6. generate candidate explanations/capture mechanisms
7. progressively filter and deep-dive candidates
8. preserve rejected and negative knowledge
9. formulate explicit hypotheses
10. implement/replay hypotheses against historical data
11. enforce time-causal information boundaries
12. compare results across many moves and days
13. discover contradictions and new mechanisms
14. maintain persistent evidence, provenance, hypotheses and research state
15. proactively inform and guide Prakash
16. improve the research machinery itself

The objective is not to discover one magic strategy.

The objective is to build a progressively more capable intelligent deterministic state/research system that can investigate the market, discover what actually survives replay, and keep getting better at finding those answers.
