# LIT Specification

LIT is an open, implementation-neutral interchange format for literary projects. It gives authors, publishers, archives, and AI-assisted tools a shared way to describe a work's structure, canon, provenance, and rights without prescribing how the prose itself must be written or stored.

> **Status:** Draft v0.1.0. The format is suitable for experimentation; backward compatibility is not guaranteed until v1.0.0.

## Why LIT?

Literary projects increasingly move between writing tools, editorial systems, archives, publishing pipelines, and generative systems. Ordinary document formats preserve text, but rarely preserve the decisions around it. LIT separates five concerns:

- `project.json` — project identity and entry points
- `components.json` — ordered or related narrative components
- `canon.json` — explicit facts, constraints, and intentional ambiguities
- `provenance.json` — who or what created and transformed material
- `rights.json` — licenses, permitted uses, and AI-specific permissions

## Repository layout

```text
schema/      Normative JSON Schemas (Draft 2020-12)
examples/    Complete example bundles for common project shapes
docs/        Design rationale and workflow guidance
```

The normative requirements are in [SPECIFICATION.md](SPECIFICATION.md). Governance and contribution rules are in [GOVERNANCE.md](GOVERNANCE.md).

## Quick start

1. Copy the closest directory under `examples/`.
2. Give every entity a stable URI or project-scoped identifier.
3. Replace the sample content and metadata.
4. Validate each JSON document against its matching file in `schema/`.
5. Publish the five manifest files with, or alongside, the referenced content.

Example validation with any Draft 2020-12-compatible validator:

```bash
check-jsonschema --schemafile schema/project.schema.json examples/novel/project.json
check-jsonschema --schemafile schema/components.schema.json examples/novel/components.json
```

To run the repository's complete schema and cross-reference checks:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

## Design commitments

- **Human agency:** authorship, review, and consent are representable rather than inferred.
- **Portable identifiers:** relationships survive movement between tools and repositories.
- **Progressive disclosure:** small projects can use minimal records; complex projects can add detail.
- **Explicit uncertainty:** canon may be disputed, provisional, or intentionally ambiguous.
- **Rights travel with content:** permissions are machine-readable but do not replace legal advice.
- **AI neutrality:** provenance can describe AI involvement without requiring or forbidding it.

## Versioning

LIT uses Semantic Versioning. Each manifest declares `litVersion`. Implementations should reject unsupported major versions and preserve unknown fields when safely round-tripping documents.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a proposal or pull request. Breaking changes begin with an issue describing the interoperability problem. Pull requests should update the specification, affected schemas, examples, and changelog together. See [AGENTS.md](AGENTS.md) for repository-specific checks and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations.

Report security concerns through the private process in [SECURITY.md](SECURITY.md), not through a public issue.

## License

Licensed under the [Apache License 2.0](LICENSE).
