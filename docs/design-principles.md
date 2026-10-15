# Design principles

## Preserve decisions, not just documents

Prose formats already carry words well. LIT concentrates on the structure and decisions that disappear when a project changes tools: narrative order, story-world constraints, authorship, transformations, and permissions.

## Separate concerns

The five-manifest model lets access policies and workflows differ. A publisher can update rights without rewriting canon; an editor can add provenance without touching content; a reading application can load components without receiving private workflow detail.

## Make the small case easy

Every manifest has a deliberately small required core. A single-author novel should not need enterprise infrastructure. Complex anthologies and branching works can add relationships, scoped assertions, multiple agents, and detailed grants.

## Keep ambiguity intact

Fiction often depends on contradiction, unreliable narration, and unresolved possibilities. `disputed` and `ambiguous` canon states prevent a database-shaped format from flattening artistic choices into false certainty.

## Prefer explicit consent

Rights fields distinguish absent information from permission. AI uses are separate because training, retrieval, inference, and adaptation can involve different choices and agreements.

## Remain tool-neutral

LIT uses JSON, URIs, media types, language tags, and JSON Schema. It does not require a specific editor, model provider, publishing platform, storage system, or business model.

## Degrade safely

Unknown extensions can be preserved. Unsupported major versions cause an explicit failure. Conditions remain inert data. Remote resources are not fetched without the consumer's security policy.
