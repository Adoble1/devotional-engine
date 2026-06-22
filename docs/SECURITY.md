# Security Notes

The current package has no network calls and no live model integration.

## Secrets

- Do not commit API keys, `.env` files, provider responses containing credentials, or production audit logs.
- Load credentials only inside a future real adapter.
- Keep mock fixtures deterministic and secret-free.

## Prompt Injection

Future adapters must treat source text, commentary, ledger entries, and model outputs as untrusted data.

- Do not let source text override role instructions or validation contracts.
- Validate structured output before passing it to later states.
- Fail closed on malformed role outputs, invalid evaluator scores, unknown contradiction verdicts, or missing source grounding.

## Logs

Audit records should store trace, checks, metadata, and approval status. Avoid storing private user notes, secrets, or unpublished pastoral details unless there is an explicit retention policy.
