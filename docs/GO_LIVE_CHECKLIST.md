# Go-Live Checklist

This engine is safe for local deterministic testing. Public release requires these gates.

## Required Before Public Publishing

- Configure a real `AgentAdapter` with request timeouts, bounded retries, model pinning, and provider error handling.
- Store credentials outside the repository and never in mock fixtures, logs, artifacts, or audit records.
- Record model versions, prompt/template versions, source translation metadata, and run IDs for every generated artifact.
- Confirm Scripture translation rights, attribution, quotation scope, and any required copyright notice.
- Require human theological approval, editorial approval, Scripture-rights confirmation, and safety review before publication.
- Keep a persistent append-only audit log for every run and approval.
- Run CI on every change and block release on failing tests.
- Add deployment-level rate limits, kill switch, rollback plan, and incident-response ownership.

## Current Local Gates

- `python -m pytest`
- `python examples/run_psalm18_mock.py`
- `python examples/run_psalm19_mock.py`
- `python -m compileall -q devotional_engine examples`

## Human Review Standard

Reviewers should verify:

- The Scripture source and focus verses are correct and legally usable.
- The devotional does not invent quotations or detach claims from the chapter.
- Christological fulfillment follows the chapter logic instead of forcing a generic formula.
- Prayer and application avoid medical, legal, financial, crisis, or pastoral-care replacement claims.
- The poem and prose are not merely mechanically compliant.
- The poem's chosen structure matches a discernible creative flow rather than defaulting to a fixed meter.
