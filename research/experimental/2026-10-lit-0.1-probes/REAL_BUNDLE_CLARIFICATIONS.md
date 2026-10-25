# Clarification items from real-bundle packaging (LC-19..LC-35)

> **Status: EXPERIMENTAL / NON-NORMATIVE.** These items were identified while packaging a full-length fiction manuscript as a LIT 0.1.0 bundle and mapping a separate knowledge graph onto LIT. The manuscript-specific test report and mapping notes are **not** published in this repository (they contain unreleased work). This file records only the generic clarification definitions.

**Spec baseline:** `LLwedoIT-TEAM/lit-spec` @ `00fe7014adf73dfff3cbb6ab3184f2de2531cd5c` (LIT 0.1.0).

**Method (summary):** A TypeScript prototype validator (`lit-core`) and unmodified `scripts/validate.py` were run against a multi-chapter bundle with SRI integrity on every chapter file, rich provenance, and canon assertions tied to whole-chapter evidence.

---

## LC-19 — Content fragments

**Problem.** `content.href` addresses an entire file. When a single file mixes studio metadata headers, reader-facing text, and editorial notes, integrity and evidence pointers cover the whole blob. Producers cannot cite “chapter 9 line 57” or a named section without duplicating files.

**Proposed direction.** Allow `content.href` with a fragment or range selector (for example `#section=chapter-text`, or byte/line ranges with optional per-span integrity metadata) so metadata and reader text can share one stored file.

---

## LC-20 — Versions and alternatives

**Problem.** Multiple revisions of the same logical chapter may exist in one directory (for example `chapter-v5.md` and `chapter-v6.md`). Tags and extensions can record selection informally, but there is no standard way to mark which file is selected, archived, or superseded.

**Proposed direction.** Add optional `component.version` and lifecycle `status` (draft / candidate / selected / archived), and/or standard relationship types such as `alternative-of` or `supersedes`.

---

## LC-21 — Renditions (master vs shipped text)

**Problem.** The text distributed to retailers or readers may differ from the “master” components referenced in the bundle. Without a first-class link, validators cannot warn when shipped text drifts from the canonical master.

**Proposed direction.** Add standard relationships (`rendition-of`, `derived-from`) and a provenance pattern for “retail text ≠ master”.

---

## LC-22 — Version-specific provenance references

**Problem.** Activity `inputs` and `outputs` reference entity IDs only (for example `chapter:09`). When several file versions share one ID, provenance cannot point at the exact bytes an activity produced or consumed.

**Proposed direction.** Allow version-qualified references (for example `entityId@version` or `{ id, integrity }`) in activity inputs/outputs.

---

## LC-23 — Review state richer than a boolean

**Problem.** Provenance fields such as `humanReviewed` are boolean. When human review is required but not yet recorded, omitting the field is honest but triggers repeated “review missing” warnings; setting `false` or `true` would misstate the state.

**Proposed direction.** Introduce structured review metadata (for example `review: { required, status: pending|approved|rejected, by, at }`).

---

## LC-24 — Time precision for activity timestamps

**Problem.** Source records often provide calendar dates only. The schema requires full date-time strings, so producers invent midnight UTC placeholders.

**Proposed direction.** Allow date-only or partial timestamps, or add an explicit `timePrecision` field.

---

## LC-25 — Unknown or TBD license

**Problem.** Grants require a license object while publication details may still be undecided. Producers fall back to free-text in `license.name` (for example “to be confirmed”), which validators cannot classify.

**Proposed direction.** Allow `license: { status: "unknown" }` or a documented convention for incomplete rights records.

---

## LC-26 — Intentional withholding in canon

**Problem.** Some facts are deliberately unstated in the narrative. Mapping them with `ambiguous` and `value: null` does not tell AI consumers to avoid filling the gap.

**Proposed direction.** Add a canon status or flag (for example `withheld` / `intentionally-unstated`) distinct from `ambiguous`.

---

## LC-27 — Integrity mismatch severity (reference checker gap)

**Problem.** Extends LC-05. On a bundle where every chapter carries SRI digests, `scripts/validate.py` still does not verify integrity, while the prototype validator reports mismatches as warnings only. Cross-tool “valid” results diverge for the same tampered content.

**Proposed direction.** Align with LC-05 normative severity once accepted; until then, document that CI’s reference script is not a full bundle validator.

---

## LC-28 — Knowledge / epistemic events

**Problem.** Character knowledge (who knows what, when, and with what confidence) does not fit cleanly into canon assertions or provenance activities alone.

**Proposed direction.** Optional `knowledge` manifest (or canon subsection) linking agent × assertion × epistemic state × content span.

---

## LC-29 — Story time vs reading order

**Problem.** Reading order comes from component `sequence`, but narrative chronology is separate. Facts and events need story-time coordinates without overloading `sequence`.

**Proposed direction.** Optional `storyTime` on assertions, events, and components, with a certainty field when chronology is undetermined relative to other events.

---

## LC-30 — Component point-of-view metadata

**Problem.** Continuity checks (for example first-person narration reporting unavailable knowledge) need POV and scene presence, which LIT 0.1 does not model on components.

**Proposed direction.** Optional `pov: { mode: first|third|omniscient, agents: [...] }` per component or per content span.

---

## LC-31 — Assertion conflicts

**Problem.** Pairs of tensions between facts are modeled by marking one assertion `disputed` with no machine link to the counterpart assertion.

**Proposed direction.** Add `conflictsWith: [assertionId]` (or equivalent) between canon assertions.

---

## LC-32 — Text-quote selectors

**Problem.** Line-number evidence breaks when text edits shift lines. A quote plus range is more stable for anchoring.

**Proposed direction.** Standardize a text-quote selector (W3C Web Annotation style) alongside line ranges, with optional verification that the quote appears at the cited location.

---

## LC-33 — Author-intent provenance

**Problem.** Author statements about intent (planned scenes, deliberate gaps, resolution of review items) are neither text-derived canon facts nor ordinary AI provenance.

**Proposed direction.** Add `author-intent` as a provenance source type with structured metadata (`statedAt`, optional verbatim hash), `textStatus` (shown / partial / gap / planned / intended), and links from review items to assertions that resolve them.

---

## LC-34 — Extended knowledge-state vocabulary

**Problem.** Epistemic models need states beyond knows/suspects/unaware (for example deliberate silence, avoidance, rationalization) with rules for continuity checking.

**Proposed direction.** Extend knowledge-state enums; define which states count as “holding” a fact for ordering checks; allow markers when avoidance ends.

---

## LC-35 — Deliberate ambiguity for artifacts

**Problem.** Some in-story artifacts are intentionally open to reader inference. Continuity validators may flag conflicting interpretations as errors.

**Proposed direction.** First-class “intentionally open” marker on assertions or artifacts so validators demote certain conflict findings to informational “intended ambiguity” rather than errors.
