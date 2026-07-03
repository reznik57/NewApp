---
name: ultrathink
description: Adversarial multi-perspective design review run BEFORE complex or high-risk changes — architecture decisions, new subsystems, security-sensitive or performance-critical paths, LLM-powered features, irreversible data/schema changes. Output is saved as an ADR. Not for single-file edits, typo fixes, or trivial config changes.
---

<!-- template-version: 2026-07.5 -->

# UltraThink Protocol

An adversarial design review run **before** building anything non-trivial.
Surfaces architecture, correctness, and edge-case risk while it's still
cheap — on paper, not in a failed deploy.

**When to run**: the trigger list lives in CLAUDE.md → Deep-Analysis Protocol
(sole home — do not restate it here; the skip list lives in this skill's
description). If a spec exists in `docs/specs/`, review THE SPEC, not a
finished diff.

## Phase 0: Clarification Gate

Identify 1–2 critical unknowns. Ask only if genuinely ambiguous:

- **Scope**: production-grade or proof-of-concept?
- **Trade-off**: optimize for speed, memory, simplicity, or maintainability?
- **Integration**: which existing component should own this?

**Skip** if requirements are unambiguous from context.

## Phase 1: Critical Rejection Check

Open CLAUDE.md and read the **⛔ Critical Invariants now** — every one of
them is a stop condition here. STOP and challenge the user if the request
implies violating one, or any universal red flag:

- Untrusted input reaching a shell, query, or interpreter without sanitization.
- Secrets/credentials logged, hardcoded, or committed.
- Irreversible data loss or unsafe migration without a backout path.
- Breaking a public contract (API shape, schema, file format) without
  versioning.
- An externally reachable endpoint, route, or action added or changed
  without an explicit authn/authz decision.

**Minor concerns**: flag them in the synthesis; don't stop.

## Phase 2: Multi-Perspective Debate

Simulate the debate internally — reason, don't tick boxes.

### The Architect — system design, performance, maintainability

| Question                                                | Why it matters                                |
| ------------------------------------------------------- | --------------------------------------------- |
| Which existing component should own this?               | Reuse before inventing                        |
| Does it fit the established data/control flow?          | Don't bypass layer boundaries                 |
| What's the performance/memory cost at scale?            | Hot paths and large inputs                    |
| Simplest design that's still correct?                   | Complexity is debt; justify every abstraction |
| {{STACK-SPECIFIC DESIGN QUESTION — or delete this row}} | {{why}}                                       |

### The User / Domain Advocate — utility, trust, workflow

| Question                                               | Why it matters                   |
| ------------------------------------------------------ | -------------------------------- |
| Does this solve the user's real problem?               | Don't build the wrong thing well |
| Is it discoverable and predictable?                    | Surprising behavior erodes trust |
| Can the user verify what happened?                     | Don't hide state behind magic    |
| Does it match existing patterns and visuals?           | Consistency over novelty         |
| {{DOMAIN-SPECIFIC USER QUESTION — or delete this row}} | {{why}}                          |

### The Devil's Advocate — edge cases, failures, security, entropy

| Question                                             | Why it matters                                    |
| ---------------------------------------------------- | ------------------------------------------------- |
| Malformed / hostile / empty input?                   | Graceful degradation, not a crash                 |
| Largest realistic input — still holds?               | Memory, timeouts, back-pressure                   |
| Concurrency / race conditions?                       | Shared state, ordering, cancellation              |
| Retried, replayed, or double-fired — still correct?  | Idempotency; duplicated side effects              |
| Is failure observable, or silently swallowed?        | Errors must surface                               |
| Is cancellation / timeout honored throughout?        | No orphaned work                                  |
| Does this add an abstraction the task doesn't need?  | Speculative structure is debt                     |
| Any defensive boilerplate for impossible conditions? | Noise that buries real handling                   |
| Does it pull in a NEW dependency?                    | Apply CLAUDE.md → Standing Rules                  |
| Does it lean on a deprecated or legacy API?          | Agents reproduce stale idioms; check current docs |

## Phase 3: Debate Output

- **Synthesis**: ONE non-obvious key concern + its resolution per
  perspective. Skip perspectives with nothing non-obvious to say.
- **Options Considered**: Option A (selected) — why it wins. Option B
  (discarded) — why it lost.
- **Architecture Decision**: owner (component/layer), integration point,
  data flow (source → transform → sink).

**Save it**: write Phase 3 as `docs/adr/NNNN-<slug>.md` (next free number,
status: proposed) BEFORE implementation starts. See `docs/adr/README.md`.

## CHECKPOINT

Present Phase 3 via plan mode. **Plan approval IS the checkpoint** — it also
flips the ADR to accepted.

## Phase 4: Implementation Plan

Only after approval.

- New external dependency? Apply CLAUDE.md → Standing Rules.
- Existing pattern to reuse? Search before creating.
- Derive integration points fresh from CLAUDE.md → Architecture — do NOT
  maintain a copy of that map here.
- 3–7 atomic steps, each written as `[step] → verify: [check]`.

## Phase 5: Design-Review Gates

- [ ] Input validation covers any new entry point.
- [ ] Cancellation / timeout propagated throughout.
- [ ] Thread-safe where state is shared.
- [ ] Failures surface to the user (no silent catch).
- [ ] {{PROJECT-SPECIFIC PERFORMANCE/SAFETY GATE — or delete}}

## Phase 6: Verification

Governed by CLAUDE.md → ⛔ Critical Invariants (Verification Gate + Test
Integrity).

---

If this protocol missed something, update this file — cite symbols, never
counts or line numbers (CLAUDE.md Invariant 4).

**Flow**: Clarify → Reject-Critical → Debate → Output+ADR → Approve → Plan → Gates → Verify
