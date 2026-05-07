---
name: bug-repro-plan
description: "Create a minimal repeatable bug reproduction plan with environment, steps, expected vs actual behavior, and evidence checklist. Use when the user asks 复现 bug, 最小复现, reproduce issue, bug repro, 问题复现步骤, or before debugging an unclear failure."
---

# Bug Repro Plan

## Purpose
Create a minimal, repeatable reproduction plan for a bug.

## Inputs to request
- Exact bug report and frequency.
- Environment details and versions.
- Logs, screenshots, or recordings.

## Workflow
1. Ask for environment details and exact versions.
2. List numbered steps to reproduce with inputs and preconditions.
3. Record expected vs actual behavior and any logs or screenshots.
4. Suggest a minimal test or script to lock the repro.

## Output
- Repro steps with inputs and environment.
- Expected vs actual summary.
- Evidence checklist and minimal repro idea.

## Quality bar
- Make steps deterministic and minimal.
- Separate reproduction from diagnosis.
