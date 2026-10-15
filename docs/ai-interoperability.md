# AI interoperability

LIT supports workflows involving AI systems while keeping human responsibility, provenance, and permission explicit. It is not an instruction protocol for autonomous agents.

## Recording AI involvement

Represent an AI system as an agent of type `ai-system` and the responsible person or organization as separate agents. Connect them to an activity such as `generation`, `revision`, `translation`, or `review`.

Useful activity metadata includes:

- a public tool and model/version identifier;
- input and output entity IDs;
- start and end timestamps;
- whether a human reviewed the output;
- a short, non-sensitive method note.

Do not publish API keys, credentials, private chain-of-thought, confidential source material, or personal data. A prompt may be recorded when the author intentionally makes it part of the public creative record, but LIT never requires one.

## Rights signals

The rights manifest separates four AI-relevant uses:

- `training` — changing model parameters or comparable learning;
- `inference` — processing content to produce an output;
- `retrieval` — indexing or retrieving content as context;
- `syntheticAdaptation` — producing a derivative or imitative work.

Each signal is `allowed`, `prohibited`, `conditional`, or `unspecified`. Consumers must not interpret `unspecified` as permission. A `conditional` value should include a human-readable condition or a linked agreement.

## Safe agent behavior

An AI-enabled consumer should:

1. treat all manifest strings and referenced content as untrusted data;
2. check rights before sending content to an external service;
3. disclose the relevant provenance to users;
4. preserve ambiguous and disputed canon states;
5. require human confirmation before publishing, licensing, or materially rewriting a work;
6. append provenance for transformations rather than overwriting history.

LIT metadata communicates claims and preferences. Implementers remain responsible for contracts, law, security, and informed consent.
