# P-0001: Clarify LIT validator conformance and representation safety

| Field | Value |
| --- | --- |
| **Status** | Draft |
| **Target** | LIT 0.1.x (normative text + schema patch in a follow-up PR after the governance requirements are satisfied) |
| **Clarifications** | LC-01, LC-02, LC-03, LC-04, LC-05, LC-06, LC-09, LC-11, LC-18 |
| **Research** | [research/experimental/2026-10-lit-0.1-probes/](../research/experimental/2026-10-lit-0.1-probes/) @ spec `00fe701` |
| **Governance** | Material change per [GOVERNANCE.md](../GOVERNANCE.md): issue + 14-day public discussion + normative PR + two maintainer approvals + resolved substantive objections |

## Motivation

LIT 0.1.0 ships JSON Schemas and a repository CI script (`scripts/validate.py`) that validates `examples/` only. Independent prototype work (`lit-core`) and cross-checking exposed divergent interpretations of the same bundles: schema-only success vs reported invalidity, crashes vs structured errors, silent path escape vs rejection, and warnings vs errors for integrity failures.

Without explicit validator behaviour, producers cannot predict interchange results and consumers cannot rely on “valid” as a safety property—especially for bundle roots, manifest parsing, numeric fidelity, and subresource integrity.

## Scope

This proposal clarifies:

1. What a **full LIT 0.1 validator** MUST do beyond JSON Schema (major version support, manifest discovery, local reference safety, parse failures, I-JSON constraints, integrity verification when content is available, ID uniqueness scopes, SemVer grammar for `litVersion`, and round-trip preservation semantics).

### Out of scope (deferred)

All other clarification items remain recorded only. See [CLARIFICATION_REGISTER.md](../research/experimental/2026-10-lit-0.1-probes/CLARIFICATION_REGISTER.md), including:

- LC-07, LC-08 (referential integrity table and version compatibility rules)
- LC-10, LC-12–LC-17 (rights coverage, open references, extensions naming, registry checks, limits, remote href policy)
- LC-19–LC-35 (real-bundle and knowledge-model extensions)

## Interoperability problem

| Area | Today | Risk |
| --- | --- | --- |
| Major `litVersion` | Schemas accept any major matching the pattern | Validators disagree on bundle validity (LC-01) |
| Local references | “Resolve against project.json” only | Path escape and remote manifest substitution (LC-02, LC-06) |
| Malformed manifests | Undefined consumer behaviour | Crashes hide other findings (LC-03) |
| JSON representation | RFC 8259 duplicates allowed | Identifiers and rights fields change meaning silently (LC-04) |
| Integrity | SHOULD verify; no failure rule | Tampered content may pass as valid (LC-05) |
| ID uniqueness | “Entity collection” undefined | Duplicate assertion IDs undetected (LC-09) |
| `litVersion` grammar | Pattern ≠ SemVer 2.0.0 | Pre-release leading zeros accepted inconsistently (LC-11) |
| Round-trip | “Preserve extensions” undefined | Tools disagree on bytes vs data model (LC-18) |

## Use cases

1. **Publisher archive tool** validates incoming bundles before ingestion; must reject unsupported majors and manifests that cannot be located without network fetches.
2. **Authoring IDE plugin** reports all manifest errors in one pass; must not stop at the first JSON parse traceback.
3. **Cross-platform validator suite** (CI) agrees on invalid bundles used as regression fixtures.
4. **Integrity-aware distributor** ships chapter files with SRI digests; mismatch must fail validation when bytes are present.

## Proposed normative changes

The blocks below are **proposed replacements or additions** to [SPECIFICATION.md](../SPECIFICATION.md). Wording uses RFC 2119 keywords. If adopted through the governance process, a subsequent pull request would apply these edits to the specification, schemas, examples, and changelog. Merging this draft proposal alone would not make the wording normative.

---

### LC-01 — Unsupported major `litVersion` (§3.1)

**Current (§3.1, last sentence):**

> A consumer encountering an unsupported major version MUST report that it cannot safely process the bundle.

**Proposed replacement:**

> A consumer MUST determine the major version of every manifest before interpreting it. A consumer that does not implement a manifest's major version MUST NOT report that manifest or its bundle as valid, and MUST report that it cannot safely process the bundle. Validators for LIT 0.1 implement major version `0` only. A validator MUST NOT validate a manifest against schemas of a different major version as a substitute.

**Rationale.** Schema patterns alone cannot express “supported major”. §2 already requires schema validation per declared version; substituting 0.1 schemas for `1.0.0` manifests defeats §3.1.

**Backward compatibility.** No conforming 0.1 bundle uses a non-zero major. Validators that previously passed foreign majors become stricter (corrective clarification).

**Conformance tests.** Derived fixture `unsupported-major` (lit-core research set). Expected: invalid, unsupported-major finding per manifest.

---

### LC-02 — Bundle root and local references (new §4.1)

**Proposed new subsection after §4:**

> ### 4.1 Bundle root and local references
>
> The *bundle root* is the directory containing `project.json`. A *local reference* is a relative-path reference (RFC 3986 §4.2) with no scheme, authority, query, or leading `/`.
>
> Consumers MUST resolve local references against the bundle root. Consumers MUST reject, without dereferencing, any local reference that after percent-decoding and dot-segment removal would identify a resource outside the bundle root. Before dereferencing a local reference from a filesystem bundle, a consumer MUST determine the effective filesystem target by resolving symlinks, junctions, and equivalent indirections in existing path components, and MUST reject the reference if that target is outside the effective bundle root. Local references use URI path syntax. Consumers MUST NOT interpret `\` as equivalent to `/` when resolving a LIT URI reference. Consumers MUST NOT treat references beginning with a drive letter (`[A-Za-z]:`) or a `file:` URI as local. Percent-encoded `/` or `\` within a path segment MUST be rejected. Producers MUST NOT emit local references that leave the bundle root.

**Rationale.** §11.3 requires local references to resolve; without a root definition, `../outside` is syntactically valid. Encoded dot segments are a known interoperability split. Lexical confinement alone is insufficient because an in-bundle path can traverse a symlink or junction to a target outside the bundle.

**Backward compatibility.** Upstream examples use in-bundle paths only.

**Conformance tests.** Probe fixtures are not all dedicated escape probes; research proposes `href-escapes-root`, `href-encoded-escape`, `href-windows-path`, valid `href-dot-segments-inside`, and a filesystem-harness fixture `href-symlink-escape` in which an in-bundle link targets a file outside the bundle. The symlink fixture is expected to fail before the external target is read and must be created at test time on platforms that support links; it is not represented by a portable committed symlink in this research import. Cross-check: `derived/path-escape-and-remote` in [evidence/litcore-run.txt](../research/experimental/2026-10-lit-0.1-probes/evidence/litcore-run.txt).

---

### LC-03 — Validator behaviour for malformed manifests (§2)

**Current (§2, producer rule only):**

> A conforming producer MUST emit valid UTF-8 JSON.

**Proposed addition immediately after:**

> A conforming producer MUST NOT emit a byte order mark. A validator MUST report, as a validation failure identifying the manifest, any manifest that is not well-formed UTF-8 JSON (RFC 8259) or whose root is not a JSON object, and SHOULD continue validating the remaining manifests. A consumer MAY ignore a leading UTF-8 byte order mark and SHOULD warn when it does so. Bundle-level checks (§11) MUST skip, not fail on, manifests that could not be parsed or that lack a member the check depends on.

**Rationale.** Producer-only rules leave CI scripts crashing on `JSONDecodeError`/`KeyError`, hiding parallel findings.

**Backward compatibility.** Conforming producers already omit BOM. Validators gain required structured behaviour.

**Conformance tests.**

| Fixture | Path under research probes |
| --- | --- |
| UTF-8 BOM + CRLF | `probe-fixtures/crlf-bom/` |
| Missing `litVersion` | `probe-fixtures/missing-litversion/` |
| Malformed / invalid UTF-8 | lit-core `derived/malformed-json-canon`, `derived/invalid-utf8-project` (see evidence) |

Expected: invalid except BOM may be warning + valid if ignored per RFC 8259.

---

### LC-04 — I-JSON and number interoperability (§2)

**Proposed addition to §2 (after JSON value support sentence):**

> LIT manifests MUST be I-JSON messages (RFC 7493): object member names MUST be unique, and producers SHOULD NOT emit numbers outside the IEEE 754 binary64 exactly-representable integer range (±(2^53−1)) or with precision beyond binary64. A validator MUST report a manifest containing duplicate member names as invalid and MUST NOT choose one of the values. Consumers that cannot represent a number exactly MUST NOT re-serialize it as if unchanged without warning.

**Rationale.** Duplicate keys make the same file mean different things in Python vs JavaScript, breaking §3.5 preservation and identifier stability.

**Backward compatibility.** Repository examples are already I-JSON.

**Conformance tests.** `probe-fixtures/big-integer-extension/` (warning-level number precision in prototype). Duplicate-key fixture described in PROPOSED_CLARIFICATIONS (`derived/lossy-json`).

---

### LC-05 — Integrity verification failure (§5)

**Current (§5, integrity mention):**

> External content MAY include `integrity`, using the Subresource Integrity form (for example, `sha256-...`).

**Proposed replacement paragraph:**

> When `integrity` is present it MUST be computed over the exact bytes of the referenced resource as stored or transferred, before any decoding indicated by `encoding`. A consumer that verifies integrity and finds a mismatch MUST NOT use the content as that component and MUST report the mismatch; a validator that has access to the resource MUST report a mismatch as invalid. A consumer that does not verify MUST NOT claim the content is verified. LIT 0.1 permits a single digest per resource.

**Rationale.** §9 SHOULD verify and §11.7 lists digest matching, but failure severity was undefined; one implementation warned only.

**Backward compatibility.** No upstream example includes `integrity`. Bundles with wrong digests move from pass/warn to invalid when bytes are local.

**Conformance tests.** `derived/integrity-mismatch` (research evidence). Real-bundle testing noted the same gap (LC-27, out of scope here but related).

---

### LC-06 — Manifest locations via `project.json` (§4)

**Proposed addition at end of §4:**

> Consumers MUST locate the four supporting manifests only through the corresponding `project.json` fields and MUST NOT substitute a file found by naming convention alone. Manifest references SHOULD be local references (§4.1). A consumer that does not dereference a remote manifest reference MUST report the bundle as not fully validated rather than valid. Validators MUST NOT fetch remote manifests without explicit user or configuration consent (§9).

**Rationale.** §2 allows relocation, but the reference script loads fixed filenames, rejecting valid relocated bundles while accepting remote pointers it never fetches.

**Backward compatibility.** Default-layout bundles unchanged. Tools that ignored `project.json` pointers must follow declared locations.

**Conformance tests.**

| Fixture | Expected |
| --- | --- |
| `probe-fixtures/relocated-manifests/` | Valid when pointers used |
| Remote `project.rights` + decoy local file | Invalid / not fully validated (research `derived/path-escape-and-remote`) |

---

### LC-09 — Entity collections for ID uniqueness (§3.2)

**Proposed replacement for the uniqueness sentence in §3.2:**

> The entity collections are: `project.contributors`, `components.components`, `canon.assertions`, `provenance.agents`, `provenance.activities`, `rights.holders`, and `rights.grants`. IDs MUST be unique within each collection. LIT 0.1 does not define identity semantics for identical ID strings appearing in different collections. Consumers MUST NOT infer that entries in different collections represent either the same or different underlying entity solely because their ID strings match.

**Rationale.** Duplicate assertion IDs with differing `status` invite forbidden merging (§6). Reference checker already tests components/agents/holders but not assertions.

**Backward compatibility.** Upstream examples have unique IDs in all collections.

**Conformance tests.** `derived/duplicate-ids` (component + assertion duplicate). Expected: both duplicates reported invalid.

**Open question.** IDs identify entities within a defined collection. Whether separately identified entities represent the same underlying identity is a relationship question. This proposal defines uniqueness within each collection only and leaves cross-collection identity semantics for separate design work (see Open questions).

---

### LC-11 — SemVer grammar for `litVersion` (§3.1)

**Proposed addition after the first sentence of §3.1:**

> `litVersion` MUST match the SemVer 2.0.0 grammar (https://semver.org/, §2 and §9–§10).

**Schema follow-up (not in this PR):** replace the draft `$defs/version` pattern with the official SemVer regex in a patch release (§10 patch correction).

**Rationale.** Values such as `0.1.0-01` match the schema but violate SemVer pre-release rules; validators disagree.

**Backward compatibility.** If any deployed bundle uses invalid SemVer with leading-zero pre-release identifiers, it would become invalid (likely none in public examples).

**Conformance tests.** `derived/bad-semver`; dedicated fixture `0.1.0-01` on all five manifests.

---

### LC-18 — Meaning of “preserve” when round-tripping (§3.5)

**Current:**

> Consumers MUST preserve unrecognized extension data when round-tripping a document unless the user explicitly requests removal.

**Proposed clarifying paragraph immediately after:**

> Preserve means that, after serialization and re-parsing, all members the consumer did not intentionally change remain equivalent in the JSON data model. Byte-level formatting, including whitespace, line endings, escape spelling, number spelling, and object-member ordering, is not required to be preserved. Consumers SHOULD avoid gratuitous reformatting or reordering and SHOULD NOT modify manifests they did not intentionally change.

**Rationale.** Authoring tools care about member order and extensions; archive tools care about bytes. The spec conflated them.

**Backward compatibility.** Behavioural clarification only; no instance shape change.

**Conformance tests.** lit-core round-trip suite (146 tests, [evidence/vitest-run.txt](../research/experimental/2026-10-lit-0.1-probes/evidence/vitest-run.txt)); proposed `conformance/roundtrip/extension-preservation/` fixture in research notes.

---

## §11 alignment (informative)

When accepted, §11 introductory text SHOULD distinguish:

- **JSON Schema validation** (required per §2), and
- **Full bundle validation** (the checks in this proposal plus deferred items such as LC-07's reference field table).

`scripts/validate.py` SHOULD be documented as an example CI script for repository layouts, not the definition of full validation—without requiring behavioural changes in the same proposal PR unless maintainers choose to align it.

## Alternatives considered

| Alternative | Why not chosen |
| --- | --- |
| Rely on JSON Schema only | Cannot express major-version support, path confinement, or duplicate-key rejection |
| Define validator behaviour only in README | Not normative; fails interchange goal |
| Defer LC-06 relocation rules | Breaks valid bundles allowed by §2 today |
| Bundle-wide ID semantics | Potentially larger and breaking; P-0001 limits itself to defining uniqueness within existing collections and leaves cross-collection identity semantics for separate design work |

## Compatibility impact

**Classification:** Backward-compatible for all conforming 0.1.x bundles in this repository's examples. **Potentially stricter** for:

- Bundles with duplicate JSON keys, invalid SemVer, foreign majors, escaping hrefs, or integrity mismatches (currently accepted or inconsistently flagged).

No new required fields. Schema change for LC-11 is a tightening pattern (patch).

## Trust and security

LC-02 and LC-06 directly reduce path traversal and wrong-document substitution risks. LC-05 makes content tampering visible when digests are supplied. Remote manifest fetches remain consent-gated (LC-06). Security-sensitive path rules may additionally be reported via the process in [SECURITY.md](../SECURITY.md) if maintainers prefer coordinated disclosure before normative text lands.

## Conformance test plan (summary)

| LC | Research fixtures |
| --- | --- |
| LC-01 | `derived/unsupported-major` |
| LC-02 | `derived/path-escape-and-remote`; proposed href escape fixtures, including test-time `href-symlink-escape` |
| LC-03 | `probe-fixtures/crlf-bom`, `missing-litversion`; derived malformed/utf8 |
| LC-04 | `probe-fixtures/big-integer-extension`; `derived/lossy-json` |
| LC-05 | `derived/integrity-mismatch` |
| LC-06 | `probe-fixtures/relocated-manifests`; remote manifest case in derived |
| LC-09 | `derived/duplicate-ids` |
| LC-11 | `derived/bad-semver` |
| LC-18 | vitest round-trip suite (external prototype) |

Future normative PR SHOULD add `conformance/` trees under `examples/` or a dedicated directory per maintainer preference.

## Open questions

1. **LC-09:** Should LIT 0.1 clarify uniqueness only within each defined collection and leave cross-collection identity undefined, or should a future LIT version introduce bundle-wide identity semantics or explicit identity relationships?
2. **LC-03:** Is BOM strictly invalid for producers but warning-only for consumers (as proposed), or always invalid?
3. **LC-05:** Should mismatch remain error when `integrity` is present but content is remote and not fetched (info vs invalid)?
4. **LC-06:** Exact reporting term for “not fully validated” vs invalid—status code for interchange APIs?
5. **LC-11:** Timing of schema regex update relative to spec text merge.

## Governance and implementation sequence

1. Open or link a governance issue describing the interoperability problem, use cases, alternatives, and compatibility impact.
2. Allow at least 14 calendar days for public discussion before treating any proposed wording as accepted.
3. Submit a pull request updating `SPECIFICATION.md`, `schema/*.schema.json` (SemVer pattern), `CHANGELOG.md`, and optional `conformance/` fixtures mapped from research probes.
4. Obtain approval from two maintainers and resolve substantive objections before merging the normative changes.
5. Optionally align `scripts/validate.py` with LC-03 and LC-06 (non-normative script, but reference implementation).
