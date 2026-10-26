# Experimental research: LIT 0.1.0 conformance probes (October 2026)

> **Non-normative.** This directory records interoperability research. It does **not** change [SPECIFICATION.md](../../../SPECIFICATION.md), JSON Schemas, examples, or [scripts/validate.py](../../../scripts/validate.py).

## What this is

Cross-check between:

- Unmodified [`scripts/validate.py`](../../../scripts/validate.py) from this repository (Python + `jsonschema`), and
- An external TypeScript prototype validator (`@msp/lit-core`, not vendored here).

The work produced clarification items **LC-01..LC-35**, synthetic **probe fixtures**, and **recorded run logs** from 2026-10-22.

## Spec baseline

| Item | Value |
| --- | --- |
| Repository | `LLwedoIT-TEAM/lit-spec` |
| Commit | `00fe7014adf73dfff3cbb6ab3184f2de2531cd5c` |
| Version | LIT Specification 0.1 |

## Contents

| Path | Purpose |
| --- | --- |
| [PROPOSED_CLARIFICATIONS.md](./PROPOSED_CLARIFICATIONS.md) | Detailed LC-01..LC-18 analysis, proposed wording, and observed validator behaviour |
| [REAL_BUNDLE_CLARIFICATIONS.md](./REAL_BUNDLE_CLARIFICATIONS.md) | Generic LC-19..LC-35 definitions from real-bundle testing (no unpublished manuscript text) |
| [CLARIFICATION_REGISTER.md](./CLARIFICATION_REGISTER.md) | Index of all LC items, sources, and disposition |
| [make-probes.py](./make-probes.py) | Regenerates `probe-fixtures/` from [`examples/novel`](../../../examples/novel) |
| [probe-fixtures/](./probe-fixtures/) | Eight synthetic conformance and edge-case bundles, including intentionally invalid cases |
| [evidence/](./evidence/) | Scripts used for the original run and **unchanged** captured output |

Manuscript-specific reports that motivated LC-19..LC-27 were **not** committed (unreleased work). Only neutral summaries appear in `REAL_BUNDLE_CLARIFICATIONS.md`.

## Re-run probes (this repository only)

From the repository root:

```bash
python -m pip install -r requirements-dev.txt
python research/experimental/2026-10-lit-0.1-probes/make-probes.py
```

Validate each probe with the reference CI script (same layout as `examples/`):

```bash
PROBE=research/experimental/2026-10-lit-0.1-probes/probe-fixtures/crlf-bom
TMP=$(mktemp -d)
mkdir -p "$TMP/examples" "$TMP/scripts"
cp -r schema "$TMP/"
cp scripts/validate.py "$TMP/scripts/"
cp -r "$PROBE" "$TMP/examples/probe"
python "$TMP/scripts/validate.py"
rm -rf "$TMP"
```

Compare results to [evidence/probes-run.txt](./evidence/probes-run.txt). That log also includes `lit-core` runs, which require a separate checkout of the prototype (see below).

The repository's `Validate LIT` workflow invokes `scripts/validate.py` only against the standard `examples/` tree. It does not execute this probe loop or validate the captured `lit-core` results.

## Re-run full evidence capture (optional)

The recorded logs in `evidence/` were produced on a developer machine that also had:

- A Python virtualenv with `jsonschema[format]` (see [requirements-dev.txt](../../../requirements-dev.txt))
- A checkout of the `lit-core` prototype and a separate set of derived fixtures

The repository URL and commit SHA for that prototype, and the derived fixture contents, were not recorded here. The scripts under `evidence/` contain **historical absolute paths** under `/workspace/lit-core-prototype`; they are preserved verbatim as run artifacts. Consequently, the full cross-validator evidence cannot be reproduced from this repository alone.

If the original prototype checkout and derived fixtures are recovered, replay requires:

1. Set `LIT_SPEC_ROOT` to this repository root.
2. Set `LIT_CORE_ROOT` to that recovered `lit-core` prototype checkout (with `vendor/lit-spec` mirroring commit `00fe701`).
3. Set `PYTHON` to a Python interpreter with dependencies installed.
4. Edit or wrap the scripts to substitute those variables for the hard-coded paths, **or** reproduce the probe loop manually as above.

Do **not** edit `evidence/*-run.txt` when refreshing; add a new file such as `evidence/probes-run-YYYY-MM-DD.txt` and note the command in your commit message.

## Related proposal

Normative draft for LC-01, 02, 03, 04, 05, 06, 09, 11, and 18: **P-0001** (pull request B, stacked on the research import).
