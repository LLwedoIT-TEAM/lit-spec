# Repository guidance for agents

This repository contains a format specification. Correctness means that normative prose, JSON Schemas, and examples agree.

## Working rules

- Read `SPECIFICATION.md` before changing a schema.
- Treat files in `schema/` as normative and examples as conformance fixtures.
- Use JSON Schema Draft 2020-12 and two-space JSON indentation.
- Keep identifiers stable. Renaming a property or changing its meaning is a breaking change.
- Put experimental metadata in `extensions`; do not add unconstrained top-level fields.
- Update `CHANGELOG.md` for user-visible changes.
- Do not add executable behavior to conditions, extensions, or example content.
- Never include secrets, private prompts, personal addresses, or real access tokens in examples.

## Required checks

Before proposing a change:

1. Install the pinned development dependency with `python -m pip install -r requirements-dev.txt`.
2. Run `python scripts/validate.py`.
3. Check Markdown links and keep terminology consistent with `SPECIFICATION.md`.
4. Keep GitHub Actions permissions read-only unless a documented workflow requirement needs more access.
5. Pin every external GitHub Action to a full commit SHA.

If a validation tool is unavailable, state exactly which checks were performed and which remain.
