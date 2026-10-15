# LIT Specification 0.1

## 1. Status and scope

This document defines LIT, a portable metadata format for literary projects. LIT describes a project's identity, narrative components, canon, provenance, and rights. It does not define a prose markup language, rendering engine, digital-rights-management system, or proof of legal ownership.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described by RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## 2. Conformance

A conforming LIT bundle MUST contain these JSON documents:

| Document | Schema | Purpose |
| --- | --- | --- |
| `project.json` | `schema/project.schema.json` | Identity, descriptive metadata, and manifest locations |
| `components.json` | `schema/components.schema.json` | Narrative units and their relationships |
| `canon.json` | `schema/canon.schema.json` | Facts, constraints, and intentional uncertainty |
| `provenance.json` | `schema/provenance.schema.json` | Agents and creation or transformation activities |
| `rights.json` | `schema/rights.schema.json` | Rights holders, licenses, uses, and AI permissions |

Each document MUST validate against the schema for its declared `litVersion`. A bundle MAY store the documents under other names or locations when `project.json` points to them.

A conforming producer MUST emit valid UTF-8 JSON. A conforming consumer MUST support JSON values exactly as defined by the schemas and MUST NOT silently reinterpret identifiers.

## 3. Common data model

### 3.1 Versions

Every manifest MUST contain `litVersion` as a semantic version string. All manifests in a bundle SHOULD use the same version. A consumer encountering an unsupported major version MUST report that it cannot safely process the bundle.

### 3.2 Identifiers

The `id` of a project MUST be an absolute URI. IDs for entities within a project MAY be absolute URIs or project-scoped strings matching `^[A-Za-z][A-Za-z0-9._:-]*$`.

Entity IDs MUST be unique within their entity collection. References are resolved first against IDs in the current bundle and then as URIs. Schema validation does not guarantee referential integrity; producers and validators SHOULD perform that additional check.

### 3.3 Time

Timestamps MUST use RFC 3339 date-time syntax. Producers SHOULD emit UTC timestamps. Dates without a known time MAY use full-date syntax where permitted.

### 3.4 Languages and media types

Language tags SHOULD follow BCP 47. Media types SHOULD use IANA-registered values. Text referenced by `href` is outside the manifest and SHOULD be distributed with integrity metadata when the transport does not already provide it.

### 3.5 Extensions

Custom properties MUST be placed in an `extensions` object. Extension keys SHOULD be absolute URIs or use a collision-resistant prefix. Consumers MUST preserve unrecognized extension data when round-tripping a document unless the user explicitly requests removal.

## 4. Project manifest

`project.json` is the bundle entry point. It declares:

- a stable project `id` and human-readable `title`;
- the LIT version and project `type`;
- one or more credited contributors;
- the locations of the four supporting manifests;
- optional language, description, dates, identifiers, keywords, and extensions.

The `components`, `canon`, `provenance`, and `rights` fields are URI references. Relative references are resolved against the location of `project.json`.

Contributor roles are free-text tokens so communities can evolve their vocabularies. Producers SHOULD prefer recognizable terms such as `author`, `editor`, `translator`, `illustrator`, and `publisher`.

## 5. Components manifest

`components.json` contains the addressable units of a project. A component may be a chapter, scene, poem, essay, branch, fragment, paratext, media asset, or another declared type.

Each component MUST have an `id`, `type`, and `title`. It MUST provide exactly one of:

- `content.inline`, containing the material directly; or
- `content.href`, referring to an external resource.

`content.mediaType` is REQUIRED. External content MAY include `integrity`, using the Subresource Integrity form (for example, `sha256-...`).

Order MAY be expressed with integer `sequence` values. A producer using `sequence` MUST NOT assign the same value to two components in the same linear reading order. Nonlinear projects SHOULD use `relationships` with types such as `precedes`, `follows`, `branches-to`, `contains`, `references`, or a project-defined token.

Conditions on relationships are descriptive constraints. LIT does not define an execution language; tools MUST NOT execute condition text as code.

## 6. Canon manifest

`canon.json` makes story-world assertions explicit. An assertion MUST include:

- `id`, `subject`, and `predicate`;
- exactly one of `object` (an entity reference) or `value` (a JSON literal);
- a `status`: `canonical`, `provisional`, `disputed`, `retconned`, or `ambiguous`.

Assertions MAY specify scope, supporting evidence, notes, and effective dates. Conflicting assertions are valid when their status or scope explains the disagreement. Consumers MUST NOT collapse `ambiguous` or `disputed` assertions into a single fact without user direction.

Predicates are project-defined tokens or URIs. Projects intended for broad exchange SHOULD document their predicate vocabulary.

## 7. Provenance manifest

`provenance.json` records agents and activities using a deliberately small model inspired by W3C PROV.

An agent represents a person, organization, software tool, or AI system. An activity records a creation, edit, translation, import, generation, review, or other transformation and links input and output entity IDs.

AI-assisted activities SHOULD identify the model or service in `tool`, record a non-secret model/version identifier where known, describe the human review state, and identify the responsible human or organization as an agent. Prompts and private chain-of-thought are not required. Secrets, personal data, or confidential prompts MUST NOT be placed in public provenance records.

`humanReviewed` communicates workflow state, not truth or quality. Consumers MUST NOT present it as certification.

## 8. Rights manifest

`rights.json` expresses machine-readable claims and permissions. It MUST identify at least one rights holder and one grant.

A grant associates one or more assets with a rights holder and a license or rights statement. It may restrict territory, dates, languages, media, and permitted uses. The `ai` object separately expresses whether training, inference, retrieval, and synthetic adaptation are allowed, prohibited, conditional, or unspecified.

The value `unspecified` MUST NOT be interpreted as permission. Conflicts between this manifest and applicable law or a signed agreement are resolved by the law or agreement. LIT metadata is informative and is not legal advice, proof of ownership, or an enforcement mechanism.

## 9. Integrity and security

LIT documents are data, not executable instructions. Consumers:

- MUST treat text, conditions, prompts, extensions, and referenced content as untrusted input;
- MUST NOT execute embedded text as code or agent instructions;
- SHOULD verify `integrity` values before using external content;
- SHOULD limit recursion, document size, URI schemes, and network access;
- SHOULD warn before resolving remote references or disclosing private identifiers;
- MUST apply the same security policy to AI-generated and human-authored content.

Digital signatures and content-addressed packaging are outside v0.1 and may be added by compatible transports.

## 10. Compatibility and evolution

Patch releases correct mistakes without changing valid instance meaning. Minor releases add backward-compatible optional fields or vocabularies. Major releases may make breaking changes.

Consumers SHOULD ignore unknown enum-like extension values only when the relevant schema permits them. Producers MUST NOT place experimental fields at the top level; use `extensions` instead. Deprecations require documentation in `CHANGELOG.md` for at least one minor release before removal in a major release.

## 11. Validation beyond JSON Schema

The supplied schemas verify document shape. Full bundle validation SHOULD additionally check:

1. all five manifests declare compatible versions;
2. IDs are unique in their defined scopes;
3. local references resolve;
4. component sequences are unambiguous where used;
5. activity inputs and outputs reference known entities when intended to be local;
6. rights grants cover every distributed component or explicitly document an exception;
7. integrity digests match referenced resources.
