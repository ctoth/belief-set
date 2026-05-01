# Contributing

Run checks from the repository root:

```powershell
uv run pyright belief_set
uv run pytest -vv
```

The package must not import propstore. Keep formal algorithms citation-anchored
and keep propstore-specific projection, provenance, storage, worldline, and CLI
behavior outside this repository.
