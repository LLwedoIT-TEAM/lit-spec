# Proposed clarifications to LIT 0.1.0 (from lit-core ↔ `scripts/validate.py` cross-check)

> **Status: PROPOSALS ONLY.** Nothing here is normative. No issue, PR or change has been made to `LLwedoIT-TEAM/lit-spec` or any other repository. The wording below is a draft for discussion.
>
> - **Spec baseline:** `LLwedoIT-TEAM/lit-spec` `main` @ `00fe7014adf73dfff3cbb6ab3184f2de2531cd5c` (`SPECIFICATION.md` "LIT Specification 0.1", five draft 2020-12 schemas, `scripts/validate.py`). Mirrored unmodified in the lit-core prototype's `vendor/lit-spec/`.
> - **Implementations compared:**
>   - `scripts/validate.py`, unmodified. Python 3.13.5 and `jsonschema[format]` 4.26.0 (the version in lit-spec's `requirements-dev.txt`). Each fixture was run alone in a temp copy laid out as `examples/<fixture>/`.
>   - The `@msp/lit-core` prototype (TypeScript, Node 20.19.2): `scripts/validate-bundle.ts`, run in default mode, `--strict-references` mode and `--proposed` mode.
> - **Re-run on 2026-10-22, ~21:00 MDT (UTC-6).** Every "Observed" line below comes from that run, not from earlier notes. Raw logs are in `evidence/`.
> - **Fixtures:**
>   - `derived/*` are the lit-core prototype's derived fixtures (`packages/lit-core/test/fixtures/derived`).
>   - `probe/*` are small extra probes built for this write-up by `make-probes.py` from the unmodified upstream `novel` example (`probe-fixtures/`).
>   - None of these are upstream fixtures.
> - **About `validate.py`:** it is lit-spec's repository CI script for `examples/`. It isn't presented as a general-purpose bundle validator. Several disagreements below come from that narrower role rather than from a misreading of the spec. They still matter, because it is currently the only reference checker, so the spec should say what a *full* validator does (§11).
> - **Severity terms:** *Impact* is how much harm or divergence the ambiguity can cause. *Suggested severity* is the level a validator would report under the proposed wording: **error** means the bundle is not conforming / MUST, **warning** is a SHOULD, and **info** is advisory.

## Summary

| ID | Title | Spec § | validate.py (observed) | lit-core default (observed) | Impact | Suggested severity |
| --- | --- | --- | --- | --- | --- | --- |
| LC-01 | Unsupported major `litVersion` must fail validation | §3.1, §10 | **pass** | error (×5) | High | error |
| LC-02 | Local references must stay inside the bundle | §4, §9, §11.3 | **pass** | error `policy.ref.rejected` (×2) | High | error |
| LC-03 | Unparseable / non-UTF-8 / BOM / shape-broken manifests must be reported, not crash | §2, §3.1 | **crash** (traceback, exit 1) ×4 probes | structured error (BOM: warning) | High | error (BOM: warning) |
| LC-04 | Duplicate JSON member names and non-interoperable numbers | §2, §3.5 | **pass** (last value wins silently) | error (dup key); warning (big int) | High | error (dup); warning (number) |
| LC-05 | Integrity digest mismatch | §3.4, §5, §9, §11.7 | **pass** (not checked) | warning | High | error |
| LC-06 | Manifests are located via `project.json`; remote manifests | §2, §4, §9 | relocated: **fail**; remote `rights`: **pass** (ignores pointer) | relocated: valid; remote: error | Medium–High | error (unlocatable) |
| LC-07 | Referential integrity: which fields, and how severe | §3.2, §11.3, §11.5 | **fail** (4 findings) | 5 warnings, valid; strict: 4 errors + 1 warning | Medium | error for listed fields |
| LC-08 | "Compatible versions" across manifests; schema for other 0.x minors | §2, §3.1, §11.1 | **fail** | 2 warnings, valid (strict too) | Medium | error across majors / 0.x minors; warning across patches |
| LC-09 | Scope of "entity collection" for ID uniqueness | §3.2, §11.2 | flags component dup only | flags component **and** assertion dup | Medium | error |
| LC-10 | Rights coverage and its "explicit exception" | §8, §11.6 | **fail** | warning, valid | Medium | warning unless exception mechanism defined |
| LC-11 | Which SemVer grammar `litVersion` follows | §3.1 | `0.1.0-01` accepted | `0.1.0-01` rejected | Low–Medium | error |
| LC-12 | "Intended to be local" activity inputs/outputs | §3.2, §7, §11.5 | `node:ghost` output not checked | warning | Low–Medium | warning |
| LC-13 | Canon `subject`/`object`/`scope`/`evidence` resolution | §3.2, §6 | not checked | not checked (proposed rule: evidence only) | Low–Medium | info/warning (opt-in) |
| LC-14 | Remote `content.href` handling | §3.4, §9 | **pass** (silent) | info, valid, not fetched | Low–Medium | warning/info |
| LC-15 | Extension keys and custom properties | §3.5, §10 | schema `additionalProperties` only | schema + spec errors + namespacing warning | Low | error / warning |
| LC-16 | BCP 47 and IANA media types: pattern vs registry | §3.4 | **pass** | valid, no finding | Low | warning (opt-in registry check) |
| LC-17 | Minimum resource limits | §9 | none | none | Low (untested) | — |
| LC-18 | What "preserve when round-tripping" means (bytes vs JSON data) | §2, §3.5 | n/a (no serializer) | semantic preservation tested; bytes only for unchanged manifests | Low–Medium | — |

---

## LC-01 — Unsupported major `litVersion` must fail validation

**Spec.**
- §3.1: "A consumer encountering an unsupported major version MUST report that it cannot safely process the bundle."
- §10: "Major releases may make breaking changes."
- §2: "Each document MUST validate against the schema for its declared `litVersion`."
- The schema `$defs/version` pattern `^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)…` accepts any major.

**Observed (`derived/unsupported-major`: every manifest `litVersion: "1.0.0"`, novel otherwise unchanged).**
- validate.py: `Validated 5 schemas and all example bundles; cross-reference checks passed.`, exit 0.
- lit-core (all modes): 5 × `ERROR spec.version.unsupported-major`, `INVALID`, exit 1.

**Why it's ambiguous.**
- The schemas are the only machine check shipped, and they accept `1.0.0`. So a schema-only validator reports a bundle valid even though §3.1 says it cannot be safely processed.
- The spec doesn't say whether "report" means *validation failure* or a side note.
- It also doesn't say which majors a 0.1 validator "supports".
- §2 requires validating against "the schema for its declared `litVersion`", but no 1.x schema exists. Validating against 0.1 schemas is meaningless, and that isn't stated.

**Proposed wording (§3.1, replace the last sentence).**
> A consumer MUST determine the major version of every manifest before interpreting it. A consumer that does not implement a manifest's major version MUST NOT report that manifest or its bundle as valid, and MUST report that it cannot safely process the bundle. Validators for LIT 0.1 implement major version `0` only. A validator MUST NOT validate a manifest against schemas of a different major version as a substitute.

**Suggested severity:** error. **Compatibility:** no valid 0.1 bundle changes meaning, and only bundles that were never 0.1 are affected.

**Proposed conformance fixture:** `conformance/invalid/unsupported-major/` is the novel example with all five `litVersion: "1.0.0"`. Expected: invalid, one "unsupported major" finding per manifest. A variant with only `rights.json` at `1.0.0` should also be invalid (see LC-08).

---

## LC-02 — Local references must stay inside the bundle

**Spec.**
- §4: "The `components`, `canon`, `provenance`, and `rights` fields are URI references. Relative references are resolved against the location of `project.json`."
- §5: "`content.href`, referring to an external resource."
- §9: "MUST treat … referenced content as untrusted input"; "SHOULD limit recursion, document size, URI schemes, and network access".
- §11.3: "local references resolve".
- Schema: `href` and `manifestReference` are `format: uri-reference`.

**Observed (`derived/path-escape-and-remote`: `components[0].content.href = "../outside.md"`, `components[1].content.href = "content/%2e%2e/%2e%2e/secret.md"`, `project.rights` set to an `https://` URL).**
- validate.py: pass, exit 0. It never reads `href`, and it loads `rights.json` from the directory regardless of `project.rights` (see LC-06).
- lit-core (all modes): `ERROR policy.ref.rejected … "../outside.md" (escapes-root)`, `ERROR policy.ref.rejected … "content/%2e%2e/%2e%2e/secret.md" (escapes-root)`, `ERROR policy.ref.remote-manifest`, `INVALID`, exit 1. In lit-core these are *implementation policy* (`policy.*`), not spec rules, because the spec doesn't forbid escaping.

**Why it's ambiguous.**
- "Local" is undefined.
- The spec doesn't say what the bundle root is, whether `..` may leave it, or whether percent-encoded dot segments count.
- It doesn't say whether absolute paths, `file:` URIs, Windows drive letters (`C:` parses as a URI scheme) and backslashes are allowed.
- A literal reading lets a bundle point a consumer at `../../.ssh/id_rsa`. RFC 3986 dot-segment removal happens *after* percent-decoding only in some implementations, so `%2e%2e` is a known divergence point.

**Proposed wording (new §4.1 "Bundle root and local references").**
> The *bundle root* is the location containing `project.json`. A *local reference* is a relative-path reference (RFC 3986 §4.2) with no scheme, authority, query, or leading `/`. Consumers MUST resolve local references against the bundle root and MUST reject, without dereferencing, any local reference that after percent-decoding and dot-segment removal would identify a resource outside the bundle root. Consumers MUST NOT treat `\` as a path separator, and MUST NOT treat references beginning with a drive letter (`[A-Za-z]:`) or a `file:` URI as local. Percent-encoded `/` or `\` within a path segment MUST be rejected. Producers MUST NOT emit local references that leave the bundle root.

**Suggested severity:** error. **Compatibility:** none of the upstream examples use such references. **Security note:** `CONTRIBUTING.md` says to use private vulnerability reporting for security concerns. This is a spec ambiguity rather than a known exploit in a shipped tool, but maintainers may prefer that LC-02, LC-14 and LC-17 go through that channel.

**Proposed conformance fixtures:** `conformance/invalid/href-escapes-root/` uses `../outside.md`. `…/href-encoded-escape/` uses `content/%2e%2e/%2e%2e/secret.md`. `…/href-windows-path/` uses `C:\x.md` and `content\x.md`. `conformance/valid/href-dot-segments-inside/` uses `content/../content/a.md` with the file present. Expected: the first three invalid, the last valid.

---

## LC-03 — Unparseable, non-UTF-8, BOM-prefixed or shape-broken manifests must be reported, not crash

**Spec.** §2: "A conforming producer MUST emit valid UTF-8 JSON." §3.1: "Every manifest MUST contain `litVersion` …". No text covers what a *consumer/validator* does with input that breaks these rules. RFC 8259 §8.1 says implementations "MUST NOT add a byte order mark" and "MAY ignore the presence of a byte order mark rather than treating it as an error".

**Observed.**

| Fixture | validate.py | lit-core |
| --- | --- | --- |
| `derived/malformed-json-canon` (truncated) | traceback, `json.decoder.JSONDecodeError: Expecting ',' delimiter: line 26 column 4 (char 686)`, exit 1 | `ERROR spec.json.malformed`, `INFO policy.json.syntax-position canon.json:26:4`, INVALID |
| `derived/invalid-utf8-project` (0xFF byte) | traceback, `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 149`, exit 1 | `ERROR spec.json.invalid-utf8`, plus 4 × INFO default-location, INVALID |
| `probe/crlf-bom` (UTF-8 BOM + CRLF, same JSON as novel) | traceback, `JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig)`, exit 1 | 5 × `WARNING policy.json.bom`, VALID |
| `probe/missing-litversion` (rights.json lacks `litVersion`) | schema error is computed, then traceback `KeyError: 'litVersion'` at line 63, exit 1 | `ERROR schema.required`, `ERROR spec.version.missing`, INVALID |

validate.py's non-zero exit does fail CI. But the crash stops all other findings for the bundle (and for any later example directory), and it gives no file/location in the normal report format.

**Why it's ambiguous.**
- The spec constrains producers only.
- It doesn't say whether a BOM makes a manifest non-conforming.
- It doesn't say whether a validator must keep going after one manifest fails to parse.
- It doesn't say whether bundle-level checks run when a required member is missing.

**Proposed wording (§2, after the producer sentence).**
> A conforming producer MUST NOT emit a byte order mark. A validator MUST report, as a validation failure identifying the manifest, any manifest that is not well-formed UTF-8 JSON (RFC 8259) or whose root is not an object, and SHOULD continue validating the remaining manifests. A consumer MAY ignore a leading UTF-8 byte order mark and SHOULD warn when it does so. Bundle-level checks (§11) MUST skip, not fail on, manifests that could not be parsed or that lack a member the check depends on.

**Suggested severity:** error for invalid UTF-8 or JSON. Warning for a BOM (ignored per RFC 8259). **Non-normative recommendation:** `scripts/validate.py` catch `JSONDecodeError`/`UnicodeDecodeError`/`KeyError` and report them as findings.

**Proposed conformance fixtures:** `conformance/invalid/malformed-json/`, `…/invalid-utf8/`, `…/missing-litversion/`, and `conformance/warning/utf8-bom/`.

---

## LC-04 — Duplicate JSON member names and non-interoperable numbers

**Spec.**
- §2: "A conforming consumer MUST support JSON values exactly as defined by the schemas and MUST NOT silently reinterpret identifiers."
- §3.5: "Consumers MUST preserve unrecognized extension data when round-tripping …".
- Extension objects are `additionalProperties: true`, and `value` is `true` (any JSON).

**Observed (`derived/lossy-json`: canon extension object containing `"zeta": 1 … "zeta": 2`, integer-like keys `"10"`, `"2"`, and `12345678901234567890`).**
- validate.py: pass, exit 0. I confirmed separately with Python's `object_pairs_hook` that the parser sees both `zeta` values `[1, 2]`, and `json.load` keeps only `2`, silently.
- lit-core (all modes): `ERROR policy.json.duplicate-key … "zeta"`, `WARNING policy.json.number-precision … 12345678901234567890`, `WARNING policy.json.key-order-not-preserved … (10, 2)`, INVALID.
- `probe/big-integer-extension` (big integer only): validate.py pass; lit-core `WARNING policy.json.number-precision`, VALID.

**Why it's ambiguous.**
- RFC 8259 §4 says names "SHOULD be unique" and leaves the behaviour for duplicates implementation-defined. So the same bundle means `zeta: 1` to one consumer and `zeta: 2` to another.
- That defeats §3.5 preservation and can change `id`, `status` or AI-permission values (`rights.json` `ai.*`) between tools.
- Integers above 2^53 change value in JavaScript consumers. The spec doesn't say whether that counts as "support JSON values exactly".

**Proposed wording (§2).**
> LIT manifests MUST be I-JSON messages (RFC 7493): object member names MUST be unique, and producers SHOULD NOT emit numbers outside the IEEE 754 binary64 exactly-representable integer range (±(2^53−1)) or with precision beyond binary64. A validator MUST report a manifest containing duplicate member names as invalid and MUST NOT choose one of the values. Consumers that cannot represent a number exactly MUST NOT re-serialize it as if unchanged without warning.

**Suggested severity:** error for duplicate names. Warning for non-interoperable numbers. **Compatibility:** all upstream examples are already I-JSON.

**Proposed conformance fixtures:** `conformance/invalid/duplicate-member-name/` (put the duplicate on `assertions[0].status` with `"canonical"` then `"ambiguous"`, so the divergence is visible) and `conformance/warning/large-integer-extension/`.

---

## LC-05 — Integrity digest mismatch

**Spec.**
- §3.4: "Text referenced by `href` … SHOULD be distributed with integrity metadata …".
- §5: "External content MAY include `integrity`, using the Subresource Integrity form (for example, `sha256-...`)."
- §9: "SHOULD verify `integrity` values before using external content".
- §11.7: "integrity digests match referenced resources."
- Schema: `^(sha256|sha384|sha512)-[A-Za-z0-9+/]+={0,2}$`.

**Observed (`derived/integrity-mismatch`: `content/*.md` added; one correct sha256, one wrong).**
- validate.py: pass, exit 0 (it doesn't read content or integrity).
- lit-core (all modes): `WARNING spec.content.integrity-mismatch … declared sha256-U4p0…, actual sha256-ImOl…`, VALID.

**Why it's ambiguous.**
- Verifying is a SHOULD, but the spec doesn't say what happens when verification *fails*. lit-core chose a warning only because the keyword is SHOULD.
- Under SRI (W3C), a mismatch means the resource MUST NOT be used.
- The spec doesn't say which bytes are hashed: raw file bytes, or decoded content when `content.encoding` is `base64`.
- The SRI form allows several space-separated hashes, but the schema pattern doesn't.
- "external content" vs bundle-local `href` content isn't distinguished.

**Proposed wording (§5).**
> When `integrity` is present it MUST be computed over the exact bytes of the referenced resource as stored or transferred, before any decoding indicated by `encoding`. A consumer that verifies integrity and finds a mismatch MUST NOT use the content as that component and MUST report the mismatch; a validator that has access to the resource MUST report a mismatch as invalid. A consumer that does not verify MUST NOT claim the content is verified. LIT 0.1 permits a single digest per resource.

**Suggested severity:** error when the resource is available and doesn't match. Info when it's unavailable or unverified. **Compatibility:** no upstream example carries `integrity`.

**Proposed conformance fixtures:** `conformance/valid/integrity-match/` and `conformance/invalid/integrity-mismatch/` (the same as `derived/integrity-mismatch`, but with only the mismatched component).

---

## LC-06 — Manifests are located via `project.json`; remote manifest locations

**Spec.**
- §2: "A bundle MAY store the documents under other names or locations when `project.json` points to them."
- §4: "`project.json` is the bundle entry point. It declares: … the locations of the four supporting manifests."

**Observed.**
- `probe/relocated-manifests` (the four manifests under `manifests/`, and `project.json` points there): validate.py fails with `components.json: required manifest is missing` ×4. lit-core is VALID with 0 issues.
- `derived/path-escape-and-remote` (`project.rights` is `https://example.org/remote/rights.json`, and a local `rights.json` is still present): validate.py loads the local `rights.json` and passes. lit-core reports `ERROR policy.ref.remote-manifest … was not fetched`, does not load the local file, and returns INVALID.

**Why it's ambiguous.**
- §2 allows relocation, but the only reference checker hard-codes `<name>.json`.
- The spec doesn't say whether a manifest location may be remote.
- If it may, the spec doesn't say whether a validator must fetch it, which conflicts with §9's limits on network access.
- It doesn't say whether a same-named local file may be used as a fallback. That fallback silently validates a different document from the one the bundle declares.

**Proposed wording (§4).**
> Consumers MUST locate the four supporting manifests only through the corresponding `project.json` fields and MUST NOT substitute a file found by naming convention. Manifest references SHOULD be local references (§4.1). A consumer that does not dereference a remote manifest reference MUST report the bundle as not fully validated rather than valid. Validators MUST NOT fetch remote manifests without explicit user or configuration consent (§9).

**Suggested severity:** error for an unlocatable or unfetched manifest. **Non-normative recommendation:** have `scripts/validate.py` read the locations from `project.json`.

**Proposed conformance fixtures:** `conformance/valid/relocated-manifests/` (= `probe/relocated-manifests`) and `conformance/invalid/remote-manifest-not-fetched/`, with a decoy local `rights.json` that is *invalid*, so a naming-convention fallback is detectable.

---

## LC-07 — Referential integrity: which fields are references, and how severe a dangling one is

**Spec.**
- §3.2: "References are resolved first against IDs in the current bundle and then as URIs. Schema validation does not guarantee referential integrity; producers and validators SHOULD perform that additional check."
- §11.3: "local references resolve".
- §11.5: "activity inputs and outputs reference known entities when intended to be local".

**Observed (`derived/dangling-references`: relationship target `node:missing`, agent `person:nobody`, output `node:ghost`, holder `org:unknown-holder`, asset `node:phantom`).**
- validate.py: `Validation failed`, exit 1, 4 findings: relationship target, unknown agents, unknown holder, unknown assets. It does **not** report `node:ghost` (it never checks activity `inputs`/`outputs`).
- lit-core default: 5 warnings (4 × `reference-checker.*` + `spec.provenance.io-unresolved` for `node:ghost`), VALID, exit 0.
- lit-core `--strict-references`: the 4 reference-checker findings become ERROR. `node:ghost` stays a WARNING. INVALID, exit 1.
- `derived/project-id-not-uri`: both report the project-ID format error. validate.py also reports `project reference mismatch` ×4 as failures. lit-core reports those as warnings by default and errors in strict.

**Why it's ambiguous.**
- The spec says SHOULD (warning), but lit-spec's own CI treats dangling references as failures (error). Two conforming validators therefore disagree on validity.
- The spec never lists which fields are references.
- validate.py checks: `*.project` = `project.id`, component `contributors` ⊆ project contributors, relationship `source`/`target`, activity `agentIds`, grant `holder` and grant `assets`.
- It doesn't check activity `inputs`/`outputs` (§11.5), canon `object`/`evidence` (§6, see LC-13), or anything else.
- "Resolved … then as URIs" is unclear about when an unresolved value is a dangling reference versus a legitimate external URI. Under §3.2, `person:nobody` is both a valid project-scoped ID and a syntactically valid URI.

**Proposed wording (§11, new table "Reference fields").**
> The following fields are *bundle references* and MUST resolve to an entity of the stated collection in the same bundle: `components.project`, `canon.project`, `provenance.project`, `rights.project` → `project.id`; `components[].contributors[]` → `project.contributors[].id`; `relationships[].source`/`target` → `components[].id`; `activities[].agentIds[]` → `agents[].id`; `grants[].holder` → `holders[].id`; `grants[].assets[]` → `components[].id`. A full validator MUST report an unresolved bundle reference as invalid. Other entity-valued fields (activity `inputs`/`outputs`, canon `subject`/`object`/`scope`/`evidence`) are *open references*; see LC-12 and LC-13.

**Suggested severity:** error for the listed fields, which matches current lit-spec CI. **Compatibility:** every upstream example already passes.

**Proposed conformance fixtures:** `conformance/invalid/dangling-<field>/`, one fixture per listed field, so each check is independently testable, rather than one combined fixture.

---

## LC-08 — "Compatible versions" across manifests, and schema choice for other 0.x minors

**Spec.**
- §3.1: "All manifests in a bundle SHOULD use the same version."
- §11.1: "all five manifests declare compatible versions".
- §2: "Each document MUST validate against the schema for its declared `litVersion`."
- §10: "Patch releases correct mistakes … Minor releases add backward-compatible optional fields …".

**Observed (`derived/version-mismatch`: `rights.litVersion = "0.2.0"`, others `0.1.0`).**
- validate.py: `inconsistent litVersion values`, fail, exit 1. It requires string-identical versions and validates rights against the 0.1 schema with no comment.
- lit-core, in **both** default and `--strict-references` modes: `WARNING spec.version.no-matching-schema` and `WARNING spec.version.mismatch`, VALID, exit 0.
- Correction to the earlier summary: lit-core does *not* escalate version mismatch in strict mode. Strict mode only changes `reference-checker.*` rules.

**Why it's ambiguous.**
- "Same" (§3.1, SHOULD) and "compatible" (§11.1) are different tests, and "compatible" is undefined. Under SemVer 2.0.0 §4, anything may change in 0.y.z, so 0.1 and 0.2 can't be assumed compatible.
- §2 requires a schema "for its declared `litVersion`" that doesn't exist for 0.2.0, and the spec doesn't say what a validator does then.

**Proposed wording (§3.1).**
> Versions are *compatible* when they share the same major version and, while the major version is `0`, the same minor version. All manifests in a bundle MUST declare compatible versions and SHOULD declare identical versions. A validator that has no schema for a manifest's declared major.minor version MUST NOT report that manifest as valid against a different minor's schema; it MUST report the manifest as unvalidated.

**Suggested severity:** error for incompatible versions (a different major, or a different minor while major is 0). Warning for a patch-only difference. **Compatibility:** stricter than lit-core today, and consistent with validate.py's failure for the 0.1/0.2 case.

**Proposed conformance fixtures:** `conformance/invalid/version-minor-mismatch-0x/` (= `derived/version-mismatch`) and `conformance/warning/version-patch-mismatch/` (`0.1.0` and `0.1.1`).

---

## LC-09 — Scope of "entity collection" for ID uniqueness

**Spec.**
- §3.2: "Entity IDs MUST be unique within their entity collection."
- §11.2: "IDs are unique in their defined scopes".

**Observed (`derived/duplicate-ids`: `components[0]` duplicated as `components[2]`, `assertions[0]` duplicated as `assertions[2]` with `status: disputed`).**
- validate.py: `duplicate component ID chapter:arrival` only, exit 1. It checks components, agents and holders.
- lit-core (all modes): `ERROR spec.id.duplicate` for `chapter:arrival` **and** `canon:lighthouse-status`. It checks contributors, components, assertions, agents, activities, holders and grants.

**Why it's ambiguous.** "Entity collection" is never enumerated, and §11.2's "defined scopes" are never defined. The duplicate assertion is the dangerous case. Two assertions with one ID and different `status` invite a consumer to merge them, which conflicts with §6 ("MUST NOT collapse `ambiguous` or `disputed` assertions").

**Proposed wording (§3.2).**
> The entity collections are: `project.contributors`, `components.components`, `canon.assertions`, `provenance.agents`, `provenance.activities`, `rights.holders`, and `rights.grants`. IDs MUST be unique within each collection. LIT 0.1 does not define identity semantics for identical ID strings appearing in different collections. Consumers MUST NOT infer that entries in different collections represent either the same or different underlying entity solely because their ID strings match.

**Suggested severity:** error.

**Open question.** IDs identify entities within a defined collection. Whether separately identified entities represent the same underlying identity is a relationship question. This proposal defines uniqueness within each collection only and leaves cross-collection identity semantics for separate design work (see Open questions).

**Proposed conformance fixtures:** `conformance/invalid/duplicate-id-<collection>/`, seven fixtures, one per collection.

---

## LC-10 — Rights coverage and its "explicit exception"

**Spec.**
- §8: "It MUST identify at least one rights holder and one grant."
- §11.6: "rights grants cover every distributed component or explicitly document an exception."

**Observed (`probe/uncovered-component`: the grant covers only `chapter:arrival`).**
- validate.py: `components without a rights grant ['chapter:signal']`, fail, exit 1.
- lit-core (all modes): `WARNING spec.rights.component-not-covered`, VALID.

**Why it's ambiguous.** §11 is a SHOULD list, but CI treats it as a failure. "Distributed component" is undefined: a bundle can hold planning-only or undistributed components. And there is no machine-readable field for "explicitly document an exception". The only places to put one are free text (`rights.notice`, `grants[].note`) or `extensions`, because `rights.json` and `grant` are `additionalProperties: false`. So no validator can tell a documented exception from an omission.

**Proposed wording (§8).**
> Every component SHOULD be listed in the `assets` of at least one grant. A component intentionally not covered MUST be listed in `rights.exceptions[]` (new optional array of `{ assets[], reason }`). A validator MUST report a component that is neither covered nor listed as an exception. *(Alternative without a schema change:* every component MUST be covered by a grant; use a grant with `license.name: "All rights reserved"` for reserved material.)

**Suggested severity:** warning until an exception mechanism exists, then error. **Compatibility:** `exceptions[]` is an optional field (a minor change). The alternative needs no schema change.

**Proposed conformance fixtures:** `conformance/warning/uncovered-component/` (= probe) and, if `exceptions[]` is adopted, `conformance/valid/uncovered-with-exception/`.

---

## LC-11 — Which SemVer grammar `litVersion` follows

**Spec.** §3.1: "Every manifest MUST contain `litVersion` as a semantic version string." The schema pattern allows `-[0-9A-Za-z.-]+` for the pre-release part.

**Observed (`derived/bad-semver`: components `0.1`, canon `0.1.0-01`).**
- validate.py: reports the `0.1` pattern failure and `inconsistent litVersion values`. `0.1.0-01` is accepted.
- lit-core: `schema.pattern` for `0.1`, plus `ERROR spec.version.not-semver` for **both** `0.1` and `0.1.0-01`, plus `WARNING spec.version.mismatch`.

**Why it's ambiguous.** SemVer 2.0.0 §9 forbids leading zeros in numeric pre-release identifiers, and empty identifiers. The schema pattern (`0.1.0-01`, `0.1.0-..`) is looser, so "semantic version" and the schema disagree.

**Proposed wording.**
> `litVersion` MUST match the SemVer 2.0.0 grammar (semver.org §2, §9–§10).

Also replace the schema pattern with the official SemVer regex in a patch release. That is a patch-level correction under §10.

**Suggested severity:** error. **Proposed conformance fixture:** `conformance/invalid/semver-leading-zero-prerelease/` (`0.1.0-01` on all five manifests, so it isn't masked by a version mismatch).

---

## LC-12 — "Intended to be local" activity inputs and outputs

**Spec.**
- §7: "… links input and output entity IDs."
- §11.5: "activity inputs and outputs reference known entities when intended to be local."
- §3.2: entity IDs "MAY be absolute URIs or project-scoped strings".

**Observed (`derived/dangling-references`: output `node:ghost`).** validate.py: not checked. lit-core: `WARNING spec.provenance.io-unresolved` in both modes. lit-core's test is a heuristic: a value that matches the project-scoped pattern and isn't found counts as intended-local and gets a warning. Anything else counts as an external URI and gets `spec.ref.external-uri` info.

**Why it's ambiguous.** Intent isn't expressible. Every project-scoped ID (`node:ghost`, `character:silas`) is also a syntactically valid absolute URI with scheme `node:`/`character:`, so no rule can tell "local, but dangling" from "external" apart.

**Proposed wording (§7).**
> An activity input or output that is not an absolute URI with a scheme registered with IANA, or that equals an ID in the bundle, is a local reference and SHOULD resolve to an entity in the bundle. *(Alternative:* require external inputs/outputs to be `http`/`https`/`urn` URIs.)

**Suggested severity:** warning. **Proposed conformance fixture:** `conformance/warning/activity-output-unresolved/` (`node:ghost`) plus `conformance/valid/activity-output-external/` (`https://example.org/x`).

---

## LC-13 — Canon `subject`/`object`/`scope`/`evidence` resolution

**Spec.**
- §6: "exactly one of `object` (an entity reference) or `value` (a JSON literal)"; "Assertions MAY specify scope, supporting evidence …".
- §3.2 resolution order.

**Observed (`probe/canon-unresolved-entities`: subject `character:nobody`, evidence `chapter:does-not-exist`, object `place:nowhere`, scope `branch:unknown`).**
- validate.py: pass.
- lit-core default and strict: VALID, 0 issues.
- lit-core `--proposed`: only `WARNING proposed.canon.evidence-unresolved … "chapter:does-not-exist"`. Subject, object and scope are not checked even in proposed mode.

**Why it's ambiguous.** §6 calls `object` "an entity reference", but LIT 0.1 has no collection for story-world entities (characters, places, events). The upstream examples use `place:lighthouse` and `event:midnight-signal`, which are defined nowhere, so a resolution requirement would make every upstream example invalid. `evidence` *looks* like it should point at components or activities, but the spec doesn't say so.

**Proposed wording (§6).**
> `subject`, `object`, and `scope` identify story-world entities and are not required to resolve within the bundle in LIT 0.1. `evidence` items SHOULD identify a component, assertion, or activity in the bundle, or be an absolute URI.

Optionally, a future minor could add an `entities` collection.

**Suggested severity:** info/warning, opt-in, for `evidence` only. **Proposed conformance fixture:** `conformance/valid/canon-open-world-subjects/` (= probe minus the evidence change) and `conformance/warning/canon-evidence-unresolved/`.

---

## LC-14 — Remote `content.href` handling

**Spec.**
- §3.4: "Text referenced by `href` is outside the manifest …".
- §9: "SHOULD limit … URI schemes, and network access"; "SHOULD warn before resolving remote references".
- §11.3: "local references resolve".

**Observed (`probe/remote-content-href`: `href: https://example.org/remote/arrival.md`).**
- validate.py: pass, silent.
- lit-core (all modes): `INFO spec.ref.remote-not-fetched`, VALID. It never fetches. Only `http`/`https` are treated as remote. Any other scheme is rejected as `policy.ref.rejected` (lit-core assumption 3).

**Why it's ambiguous.**
- The spec doesn't say whether a validator should fetch remote content to satisfy §11.3/§11.7.
- It doesn't list which schemes are allowed.
- It doesn't say whether "bundle valid" implies remote content was checked.

**Proposed wording (§9).**
> Validators MUST NOT dereference remote references by default. A bundle whose remote content was not retrieved MAY be reported valid, but the report MUST state that the content's existence and integrity were not verified. Producers SHOULD use only `https` for remote `href` values.

**Suggested severity:** info, or a warning when `integrity` is absent. **Proposed conformance fixture:** `conformance/valid/remote-href-unverified/` (= probe), with expected output "valid, unverified".

---

## LC-15 — Extension keys and custom properties

**Spec.**
- §3.5: "Custom properties MUST be placed in an `extensions` object. Extension keys SHOULD be absolute URIs or use a collision-resistant prefix."
- §10: "Producers MUST NOT place experimental fields at the top level".

**Observed (`derived/custom-property-outside-extensions`: top-level `mspDraft`, `extensions.draftFlag`, component `wordCount`).**
- validate.py: the two `Additional properties are not allowed` schema errors, exit 1. There is no finding for `draftFlag`.
- lit-core: the same 2 schema errors, plus `ERROR spec.extensions.top-level-field`, `ERROR spec.extensions.custom-property` and `WARNING spec.extensions.key-not-namespaced` (`draftFlag`). INVALID.

**Why it's ambiguous.** "Collision-resistant prefix" is undefined, so the SHOULD can't be tested. `draftFlag` might be acceptable or not. The MUST is already enforced by `additionalProperties: false`, so it isn't really ambiguous. The open point is only how to recognise a conforming extension key.

**Proposed wording (§3.5).**
> An extension key SHOULD be an absolute URI (RFC 3986) or a `prefix:name` string whose prefix is a reverse-DNS name or registered in the project's documentation.

**Suggested severity:** warning. **Proposed conformance fixture:** `conformance/warning/extension-key-unnamespaced/` (just `extensions: {"draftFlag": true}`, nothing else invalid).

---

## LC-16 — BCP 47 language tags and IANA media types: pattern vs registry

**Spec.** §3.4: "Language tags SHOULD follow BCP 47. Media types SHOULD use IANA-registered values." Schema: `language` `^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8})*$`, and `mediaType` `^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+$`.

**Observed (`probe/unregistered-language-media-type`: component `language: "qqqqq-zz"`, `mediaType: "text/x-not-registered"`, project `language: "english"`).** validate.py: pass. lit-core (all modes): VALID, 0 issues. Neither consults the registries.

**Why it's ambiguous.** `english` and `qqqqq-zz` are *well-formed* under the RFC 5646 ABNF (5–8-letter primary subtags are syntactically allowed), but they aren't *valid* BCP 47 tags, because they aren't registered. The schema pattern is also looser than RFC 5646 in places. For example, `en-a`, a lone singleton, matches the pattern but is not well-formed. The spec doesn't say whether well-formedness is enough or registry validity is expected, or whether `x.`/`vnd.` media types count.

**Proposed wording.**
> Language tags MUST be well-formed per RFC 5646 §2.1 and SHOULD be valid per §2.2.9. Media types MUST be syntactically valid per RFC 6838 and SHOULD be registered; unregistered `x.`/`vnd.` subtypes are permitted.

Tightening the schema pattern to RFC 5646 well-formedness would be a patch-level fix.

**Suggested severity:** error for malformed values. Warning (opt-in, registry-backed) for unregistered ones. **Proposed conformance fixture:** `conformance/invalid/language-not-well-formed/` (`en-a`; this needs an RFC 5646-aware pattern to fail), `conformance/warning/language-not-registered/` (`english`) and `conformance/warning/media-type-unregistered/` (`text/x-not-registered`).

---

## LC-17 — Minimum resource limits

**Spec.** §9: "SHOULD limit recursion, document size, URI schemes, and network access".

**Observed:** **not re-run.** No fixture exists, and neither implementation sets limits (`validate.py` has none; lit-core's ASSUMPTIONS_AND_GAPS: "no size or recursion limits yet"). This item rests on reading the code, not on a test.

**Why it's ambiguous.** Without minimum values, a producer can't know what every consumer will accept. For example, deeply nested extension data can break stack-based parsers.

**Proposed wording (§9).**
> Consumers MUST accept manifests up to 16 MiB and nesting depth 64; they MAY reject larger or deeper input and MUST report rejection rather than truncating.

The numbers are placeholders for maintainers to choose.

**Suggested severity:** error on rejection. **Proposed conformance fixture:** `conformance/valid/nesting-depth-64/` and `conformance/limits/nesting-depth-10000/`, where rejection is allowed but must be reported.

---

## LC-18 — What "preserve when round-tripping" means

**Spec.**
- §3.5: "Consumers MUST preserve unrecognized extension data when round-tripping a document unless the user explicitly requests removal."
- §2: "MUST NOT silently reinterpret identifiers."

**Observed.**
- validate.py has no serializer (n/a).
- lit-core's test suite was re-run: `vitest run` gave **146/146 passed** (5 files). Those tests assert semantic preservation (deep equality, key order, ID/order lists, extensions) on all fixtures.
- Byte identity from the model holds for LF fixtures, but not for Day One (CRLF) under `canonical`. It holds in `source-style` and in `preserve-unchanged` (README "Byte-for-byte" table, from `test-results/byte-roundtrip.json`). I did not re-derive that table separately.
- The CRLF Day One fixture passes both validators (`day-one/day-one-stress-test`: validate.py exit 0; lit-core VALID, 0 issues).

**Why it's ambiguous.**
- "Preserve" could mean bytes, the JSON data model, or the data model plus member order.
- Member order matters for authors diffing files, and JS reorders integer-like keys (see LC-04).
- The spec says nothing about line endings, indentation, BOM or number spelling (`1.0` vs `1`).

**Proposed wording (§3.5).**
> *Preserve* means the re-emitted document is equal in the JSON data model (RFC 8259 values, with object member order retained where the consumer's platform permits) to the input for all members the consumer did not intentionally change. Byte-level formatting (whitespace, line endings, escapes, number spelling) is not required to be preserved. Consumers SHOULD NOT modify manifests they did not change.

**Suggested severity:** n/a (behavioural). **Proposed conformance fixture:** `conformance/roundtrip/extension-preservation/` with nested unknown extension data, CRLF line endings and `\u00e9` escapes. Expected: data-model equality after load → serialize → reload.

---

## Open questions

1. **LC-09:** Should LIT 0.1 clarify uniqueness only within each defined collection and leave cross-collection identity undefined, or should a future LIT version introduce bundle-wide identity semantics or explicit identity relationships?

## Not raised as clarifications
These were found, but no spec change is proposed:
- `derived/assertion-object-and-value`, `content-inline-and-href`, `duplicate-sequence`, `missing-manifest`, `wrong-types`, `project-id-not-uri`: **both validators reject** these, with the same underlying findings.
- §7 "Secrets, personal data, or confidential prompts MUST NOT be placed in public provenance records", and the §10 `CHANGELOG.md` deprecation rule: these can't be checked mechanically. They are process rules.

## Reproducing

See [README.md](./README.md) in this directory.

Recorded outputs (2026-10-22 run, unmodified):

- `evidence/validate-py-derived-run.txt`: validate.py on upstream, Day One and derived fixtures (via lit-core's `scripts/crosscheck-validate-py.sh`).
- `evidence/litcore-run.txt`: lit-core default and `--strict-references` on the same fixtures (`evidence/run-litcore.sh`).
- `evidence/probes-run.txt`: validate.py and lit-core default/strict/proposed on the probe fixtures (`evidence/run-probes.sh`, built by `make-probes.py`).
- `evidence/vitest-run.txt`: the lit-core test suite.
