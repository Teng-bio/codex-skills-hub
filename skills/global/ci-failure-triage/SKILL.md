---
name: ci-failure-triage
description: "Diagnose CI/build/test pipeline failures and separate deterministic failures from flakes. Use when the user mentions CI 失败, pipeline failed, GitHub Actions, build failed, test failed in CI, flaky CI, 构建失败, or wants CI failure triage."
---

# CI Failure Triage

## Purpose
Diagnose CI failures and stabilize pipelines.

## Inputs to request
- CI logs and failing jobs.
- Recent merges and environment changes.
- Flake frequency and patterns.

## Workflow
1. Classify failures by stage and error type.
2. Check for environment changes and test flakiness.
3. Propose fixes and temporary mitigations.

## Output
- Triage summary with root cause candidates.

## Quality bar
- Separate flake from deterministic failure.
- Prefer fixes that reduce future noise.
