# Contributing to LIT

Thank you for helping improve literary-project interoperability. Contributions are welcome from authors, editors, publishers, archivists, implementers, researchers, and tool builders.

## Before opening an issue

- Search existing issues and pull requests for related work.
- Use private vulnerability reporting for security concerns; do not disclose them publicly.
- Keep questions and proposals focused on the LIT specification and its implementations.

## Proposing a change

Material changes should begin with an issue that explains:

1. the interoperability problem;
2. concrete use cases;
3. alternatives considered;
4. compatibility and migration impact;
5. any privacy, security, rights, or author-agency implications.

Breaking changes follow the process in [GOVERNANCE.md](GOVERNANCE.md).

## Pull requests

Keep each pull request focused on one change. Update all affected layers together:

- normative language in `SPECIFICATION.md`;
- JSON Schemas in `schema/`;
- at least one valid example in `examples/`;
- design or workflow documentation where relevant;
- `CHANGELOG.md`.

Before submitting:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

Pull requests must pass the repository validation workflow. Review discussions should be resolved before merge. The project uses squash or rebase merges to keep `main` linear.

## Editorial changes

Small corrections may omit schema and example changes when they do not alter normative meaning. Explain why a change is editorial in the pull request.

## AI-assisted contributions

You remain responsible for every contribution you submit. Review AI-assisted material for accuracy, originality, confidential information, hidden instructions, licensing conflicts, and unwanted personal data. Disclose material AI involvement when it helps reviewers evaluate provenance or rights.

## Licensing

By intentionally submitting a contribution, you agree that it is provided under the repository's [Apache License 2.0](LICENSE) and that you have the right to submit it.

## Conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Critique ideas precisely and treat people with respect.
