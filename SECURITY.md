# Security policy

## Supported versions

LIT is currently a pre-1.0 specification. Security fixes are applied to the latest published draft and the `main` branch.

| Version | Supported |
| --- | --- |
| `0.1.x` and `main` | Yes |
| Earlier drafts | No |

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue, discussion, or pull request.

Use [GitHub private vulnerability reporting](https://github.com/LLwedoIT/lit-spec/security/advisories/new) to report it privately. Include:

- the affected schema, specification section, or workflow;
- the security impact and realistic attack scenario;
- minimal reproduction steps or a proof of concept;
- any suggested mitigation, if known.

If private reporting is temporarily unavailable, open a public issue asking the maintainer to establish a private contact channel. Do not include vulnerability details in that issue.

The maintainer will aim to acknowledge complete reports within seven days. Timelines for validation, remediation, and disclosure depend on severity and complexity. Please allow a reasonable remediation period before public disclosure.

## Scope

Relevant reports include vulnerabilities in repository automation and specification or schema behavior that could predictably cause conforming implementations to execute untrusted content, access unintended resources, disclose sensitive data, or bypass declared rights constraints.

Ordinary specification disagreements, feature requests, and validation errors without a security impact belong in public issues.
