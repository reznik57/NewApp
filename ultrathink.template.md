<!--
  ============================================================================
  ULTRATHINK PROTOCOL TEMPLATE  (stack-agnostic deep-analysis / design review)
  ============================================================================

  HOW TO USE:
    1. Copy to your agent command dir (e.g. `.claude/commands/ultrathink.md`).
    2. Replace every <PLACEHOLDER>; act on every `> 📝 ADAPT:` note then delete it.
    3. Keep the Maintenance Contract verbatim — it is why this file stays useful.
    4. Delete this comment block.

  CONVENTIONS:  <PLACEHOLDER> — fill in.   > 📝 ADAPT: — tailoring guidance.
  ============================================================================
-->
---
description: Deep multi-perspective design review for complex/high-risk changes
---
# UltraThink Protocol

An adversarial design review run **before** building anything non-trivial.
Surfaces architecture, correctness, and edge-case risk while it's still cheap —
on paper, not in a failed deploy.

**Auto-trigger on**: multi-file changes, new subsystems, architecture decisions,
performance-critical or security-sensitive paths.
**Skip for**: single-file edits, typo fixes, trivial config changes.

---

## ⚠️ Maintenance Contract (read before editing this file)

This protocol deliberately contains **no statistics, counts, or line numbers**
(module counts, "N endpoints", file/LOC totals, `path/file:120`).

**Why:** embedded numbers rot within weeks — the doc ends up contradicting both
itself and the code. Numbers in prose are a liability; **symbol names a rename
would break are an asset.**

**Rule:** cite the *source of truth* (a class, a constant, a directory), never a
tally. The reasoning below works regardless of the exact count.

---

## Phase 0: Clarification Gate
Identify 1–2 critical unknowns. Ask only if genuinely ambiguous:
- **Scope**: production-grade or proof-of-concept?
- **Trade-off**: optimize for speed, memory, simplicity, or maintainability?
- **Integration**: which existing component/phase should own this?

**Skip** if requirements are unambiguous from context.

---

## Phase 1: Critical Rejection Check
**STOP and challenge the user** if the request implies any invariant violation.
Universal red flags:
- Untrusted input reaching a shell, query, or interpreter without sanitization.
- Secrets/credentials logged, hardcoded, or committed.
- Irreversible data loss or unsafe migration without a backout path.
- Breaking a public contract (API shape, schema, file format) without versioning.

Plus your project's own invariants:
- <PROJECT INVARIANT 1 — e.g. "buffering the full dataset instead of streaming">
- <PROJECT INVARIANT 2 — e.g. "coupling the UI layer directly to the data source">

> 📝 ADAPT: Mirror the "⛔ Critical Invariants" from your CLAUDE.md here as
> stop conditions. **Minor concerns**: flag in the summary, don't stop.

---

## Phase 2: Multi-Perspective Debate
Simulate the debate internally — reason, don't just tick boxes.

### The Architect — system design, performance, memory, maintainability
| Question | Why it matters |
|----------|----------------|
| Which existing component should own this? | Reuse before inventing; check before adding a new module |
| Does it fit the established data/control flow? | Avoid bypassing the layer boundaries |
| What's the performance/memory cost at scale? | <hot path / large-input concern for your domain> |
| Simplest design that's still correct? | Complexity is debt; justify every new abstraction |
| <STACK-SPECIFIC DESIGN QUESTION> | <why> |

### The User / Domain Advocate — utility, trust, workflow
| Question | Why it matters |
|----------|----------------|
| Does this actually solve the user's real problem? | Don't build the wrong thing well |
| Is it discoverable and predictable? | Surprising behavior erodes trust |
| Can the user verify / inspect what happened? | Don't hide state behind magic |
| Does it match existing patterns and visuals? | Consistency over novelty |
| <DOMAIN-SPECIFIC USER QUESTION> | <why> |

### The Devil's Advocate — edge cases, failure modes, security
| Question | Why it matters |
|----------|----------------|
| What happens on malformed / hostile / empty input? | Graceful degradation, not a crash |
| Largest realistic input — does it still hold? | Memory, timeouts, back-pressure |
| Concurrency / race conditions? | Shared state, ordering, cancellation |
| Is failure observable, or silently swallowed? | Errors must surface, never vanish |
| Is cancellation / timeout honored throughout? | No orphaned work or hung processes |
| <STACK-SPECIFIC FAILURE QUESTION> | <why> |

> 📝 ADAPT: Rename perspectives to fit your team's language, but keep the three
> stances: builds it / uses it / breaks it. Add 1–2 domain rows per perspective;
> resist adding counts.

---

## Phase 3: Debate Output
### Synthesis
| Perspective | Key concern | Resolution / mitigation |
|-------------|-------------|-------------------------|
| Architect | … | … |
| User Advocate | … | … |
| Devil's Advocate | … | … |

### Options Considered
- **Option A (selected)** — why it wins.
- **Option B (discarded)** — why it lost.

### Architecture Decision
- **Owner**: which component/layer?
- **Integration**: which phase, or standalone?
- **Data flow**: <source → transform → sink>.

### Recommendation
Primary path with justification citing the trade-offs above.

---

## CHECKPOINT: User Confirmation
**Ask:** "Proceed with this plan, or adjust?" — wait for confirmation before Phase 4.

---

## Phase 4: Implementation Plan
*Only after the user confirms Phase 3.*

### Dependency Verification
- [ ] New external dependency? Check license + compatibility before adding.
- [ ] Layer/ownership confirmed?
- [ ] Existing pattern to reuse? (Search before creating.)

### Integration Points
| Change type | Target |
|-------------|--------|
| <new data field> | <model + parser/serializer + tests> |
| <new business rule> | <which service/module> |
| <new UI surface> | <component pattern + wiring> |
| <needs persistence/caching> | <which layer; what's the invalidation rule> |

> 📝 ADAPT: Build this map once from your architecture; it pays back every feature.

### Atomic Steps (3–7 independently testable changes)
1. <verify the lowest-level assumption first>
2. <data/model layer>
3. <business logic / service>
4. <wiring / orchestration>
5. <UI / presentation>
6. <tests at each layer>

---

## Phase 5: Design-Review Gates
Before implementation, confirm the plan addresses:
- [ ] Input validation covers any new entry point.
- [ ] Cancellation / timeout propagated throughout.
- [ ] Thread-safe where state is shared.
- [ ] Failures surface to the user (no silent catch).
- [ ] <project-specific performance/safety gate>.

---

## Phase 6: Verification (MANDATORY — never skip)
Build + test verification is governed by **`CLAUDE.md → Critical Invariants`**.
Follow that single source of truth — do not restate the ritual here. In short:
a task is **not complete** until a verified build shows **0 errors / 0 warnings**
and tests pass.

---

## Post-Mortem (after implementation)
| Check | Pass criteria |
|-------|---------------|
| **Works?** | Tests pass, no runtime errors |
| **Good?** | Zero warnings, no silent failures, thread-safe, simple |
| **Right thing?** | Solves the user's real problem; discoverable |
| **Process?** | If this protocol missed something, update it (honor the Maintenance Contract) |

---

## Quick Reference
**Perspectives**: Architect (design/perf) · User Advocate (utility/trust) · Devil's Advocate (edge cases)
**Flow**: Clarify → Reject-Critical → Debate → Output → Confirm → Plan → Gates → Verify → Post-Mortem
**Stop for**: injection, leaked secrets, data loss, unversioned contract breaks, + your invariants
**Flag for**: minor perf concerns, non-critical style, future-refactor opportunities
