<!-- template-version: 2026-07.31 -->

# Facilitated sessions — UX reference

Full reference for the `facilitated-session` constraint profile. The hard
rules live in CLAUDE.md's `Domain Rules` section and in the
`designing-facilitated-sessions` skill; this page carries the reasoning, the
worked example and the traps — the material that would rot a lean CLAUDE.md.

## Why this is its own domain

An ordinary web UI negotiates with its reader: they scroll, zoom, sit closer.
A facilitated surface cannot. It is read at a distance it does not control,
often projected, often simultaneously with a second view (paper handout,
phone, a role-specific screen) that must NOT show the same things. Two
consequences follow, and both are layout decisions, not settings:

- **No scroll on a projected view.** Density is not a preference here; it is
  the medium's demand. What does not fit is cut or moved to another view.
- **Divergent visibility.** The moment two participants may not see the same
  state, the shared screen is the one that has to go quiet. A "hide for role
  X" filter applied to a layout designed for full disclosure leaks by
  accident — the layout must be designed for the quiet case.

## Worked example: the thesis determines everything

A crisis-response drill. The thesis — *"the emergency starts out banal"* — is
not a design decision; it is a finding about the subject. It determined the
rest: no Matrix green (which would have made participants take the scenario
LESS seriously, not more), but a sober protocol in which the clock runs. The
tension is carried by contrast, not by decoration.

The signature followed from the thesis: a 72-hour bar that IS the statutory
reporting deadline, made physical. That is why, by the end, the room
understands why a timestamp in the first situation report was not
bureaucracy. A generic progress widget could not have taught that.

The typeface followed from the subject: DIN 1451 is the face of German road
and rating plates — the formal language in which this country labels its
emergencies. That Windows ships it (as Bahnschrift) was luck; that it was
looked for at all was the constraint doing its work. "No CDN" forced system
fonts, and system fonts produced a better answer than any web font would
have. **When a constraint hurts, it is usually the road to the better
solution.**

## Traps that cost real time

### Verified in the browser window instead of the target resolution
A 1036px browser window and a 1920x1080 projection are two different layouts.
The check was green and the projection was wrong. **Rule**: screenshot at the
real target resolution (and, for print views, as a print render). This is the
domain's version of "browser verification IS the build".

### Locale-dependent date formatting
`strftime("%B")` returns "July" on a German Windows box. Anything the room
reads aloud — dates, weekdays, month names — must be formatted explicitly,
not left to the platform locale. Verify the string, not the call.

### A CSS class colliding silently between two output media
The same class name (`.url`, `.note`, `.header`) styled once for the
projected view and once for the paper view will collide the moment both
stylesheets load. It fails silently: one medium looks right, the other
quietly loses a rule. **Rule**: namespace per medium (`.beamer-…`,
`.print-…`) or scope with a media query — never share a bare class across
two media by accident.

### Tests that assert HTML formatting instead of behavior
Tests that match rendered markup as a substring (attribute order, exact tag
soup) break on every redesign while testing nothing that matters. **Rule**:
cut out the element and assert its CLASSES and its text — the behavior —
never the attribute order of the surrounding HTML. This is what makes a
redesign cheap instead of a two-day regression hunt.
