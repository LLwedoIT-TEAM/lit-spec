# LIT clarification register (LC-01..LC-35)

> **Status: EXPERIMENTAL / NON-NORMATIVE.** Tracks clarification items discovered during LIT 0.1.0 conformance research. Does not change the specification.

**Spec tested:** `LLwedoIT-TEAM/lit-spec` @ `00fe7014adf73dfff3cbb6ab3184f2de2531cd5c` (LIT Specification 0.1).

| ID | Title | One-line summary | Source | Status |
| --- | --- | --- | --- | --- |
| LC-01 | Unsupported major `litVersion` must fail validation | Schema-only checks accept wrong majors; §3.1 requires reporting unsafe bundles. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-02 | Local references must stay inside the bundle | Path escape and remote manifest references are undefined; security-critical for consumers. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-03 | Unparseable manifests must be reported, not crash | Invalid UTF-8, BOM, malformed JSON, and missing required members need structured validator behaviour. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-04 | Duplicate JSON keys and non-interoperable numbers | I-JSON uniqueness and JS number precision affect identifier stability across tools. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-05 | Integrity digest mismatch | SHOULD verify vs MUST on failure is unclear; byte scope for `encoding` unset. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-06 | Manifest location via `project.json` | Relocated manifests vs hard-coded names; remote manifest dereference undefined. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-07 | Referential integrity field list and severity | SHOULD vs CI error; which fields are bundle references is unspecified. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-08 | Compatible versions across manifests | “Compatible” undefined for 0.x minors; schema selection for undeclared minors unclear. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-09 | Entity collection scope for ID uniqueness | Duplicate assertion IDs not checked consistently; collections not enumerated. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-10 | Rights coverage and explicit exceptions | “Distributed component” and machine-readable exceptions undefined. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-11 | SemVer grammar for `litVersion` | Schema pattern looser than SemVer 2.0.0 (leading zeros in pre-release). | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-12 | Activity inputs/outputs “intended local” | Cannot distinguish dangling local IDs from external URIs with scheme-like prefixes. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-13 | Canon subject/object/scope/evidence resolution | Story-world entities vs bundle references; evidence targets unclear. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-14 | Remote `content.href` handling | Whether validators fetch remote content and how “valid” is reported. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-15 | Extension key naming | “Collision-resistant prefix” not defined for SHOULD-level tests. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-16 | BCP 47 / IANA media types vs schema pattern | Well-formed vs registry-valid tags and types. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-17 | Minimum resource limits | §9 SHOULD limit size/recursion without normative floors. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | recorded, deferred |
| LC-18 | Round-trip “preserve” meaning | Bytes vs JSON data model vs member order for extensions. | [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | in proposal P-0001 |
| LC-19 | Content fragments | Href cannot select reader-text ranges inside a multi-section file. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-20 | Versions and alternatives | No standard selected/archived revision model for sibling files. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-21 | Renditions | Master vs shipped/retail text not linked for drift detection. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-22 | Version-specific provenance references | Activity I/O cannot pin exact component bytes/version. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-23 | Review state richer than boolean | Required-but-pending human review cannot be represented honestly. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-24 | Time precision | Date-only sources forced into full date-time placeholders. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-25 | Unknown or TBD license | Incomplete grants rely on free-text license names. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-26 | Intentional withholding in canon | Deliberately unstated facts need a status distinct from `ambiguous`. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-27 | Integrity mismatch severity gap | Reference CI script ignores integrity; prototype warns only (extends LC-05). | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-28 | Knowledge / epistemic events | Agent knowledge state over time lacks a first-class manifest. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-29 | Story time vs reading order | Narrative chronology separate from component sequence. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-30 | Component POV metadata | POV/presence checks need component-level viewpoint fields. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-31 | Assertion conflicts | Paired tensions lack machine-readable `conflictsWith` links. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-32 | Text-quote selectors | Line-only evidence drifts; quotes stabilize spans (pairs with LC-19). | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-33 | Author-intent provenance | Author intent statements need a distinct provenance tier. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-34 | Extended knowledge-state vocabulary | Silence, avoidance, and rationalization states for continuity rules. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |
| LC-35 | Deliberate ambiguity | Intentionally open artifacts should not surface as hard continuity errors. | [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | recorded, deferred |

**Proposal P-0001** (`proposals/P-0001-validator-conformance-and-representation-safety.md`) is introduced in pull request B stacked on this research import.
