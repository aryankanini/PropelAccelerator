<!-- Schema: ./findings-registry-schema.md -->
# Findings Registry

## Index

| File | Finding IDs |
|------|-------------|
| app/config.py | F001 |

## Entries

```yaml
- id: F001
  file: app/config.py
  cat: implementation-decision
  type: decision
  severity: HIGH
  issue: Runtime environment configuration key selected
  cause: Requirements require startup validation but do not name a required setting
  date: 2026-09-10
  workflow: implement-tasks
```