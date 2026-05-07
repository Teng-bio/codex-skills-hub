---
name: log-summarizer
description: "Summarize noisy logs, errors, command output, or run logs into likely causes and next steps. Use when the user provides 日志, 报错, error output, traceback, CI logs, run logs, 长任务失败日志, or asks 分析日志 / 看报错 / 找失败原因."
---

# Log Summarizer

## Purpose
Summarize noisy logs into likely causes and next steps.

## Inputs to request
- Log snippet and time range.
- Service or component name.
- Recent deploys or config changes.

## Workflow
1. Group similar errors and identify the first failure.
2. Translate error messages into likely causes.
3. Suggest immediate checks or fixes.

## Output
- Top error groups with counts.
- Likely root cause and next actions.

## Quality bar
- Focus on the earliest failing signal.
- Separate symptoms from root causes.
