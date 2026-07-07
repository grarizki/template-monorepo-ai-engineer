# Contributing

## Testing

All code changes to `apps/api/ai_template/` or `apps/web/src/` must include
corresponding test updates. Non-code changes (docs, config, CI) are exempt.

CI will block merge if source code changed but no test files were modified.

## Development

```bash
make install    # Install all dependencies
make dev        # Run API + Web in parallel
make test       # Run all tests
make lint       # Lint all (Ruff + Biome)
```

## Git Hooks

Pre-commit hooks run automatically:
- **Pre-commit**: Biome (JS/TS) + Ruff (Python) lint/format
- **Pre-push**: pytest (API) + Vitest (Web)
