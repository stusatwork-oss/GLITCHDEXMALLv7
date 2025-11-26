# V4 Renderist Mall OS - Known Issues

## Phase 1 (V4.0.1-alpha)

### Non-Interactive Exit

**Issue**: Demo fails with `EOFError` when run in non-interactive shells.

**Cause**: The `input()` call at the end of `main()` expects user input to return to launcher.

**Workaround**: Use `mall_demo()` directly instead of `main()`:

```python
from src.main import mall_demo
mall_demo()
```

Or run with timeout:
```bash
timeout 15 python3 src/main.py
```

**Status**: By design - launcher integration requires interactive terminal.

---

### Cloud State Persistence

**Issue**: Old cloud state may load with incompatible mood values.

**Cause**: Previous sessions saved with old mood names (e.g., "neutral", "warped").

**Workaround**: Delete `data/cloud_state.json` to start fresh:

```bash
rm v4-renderist/data/cloud_state.json
```

**Status**: Will be fixed in Phase 2 with migration logic.

---

### Slow Pressure Buildup

**Issue**: Demo may complete without reaching contradiction thresholds (75+).

**Cause**: Default demo duration (10s) with simulated movement doesn't generate enough pressure.

**Workaround**: Run longer demo or simulate artifact discoveries:

```python
demo = MallDemo()
demo.run(duration=60.0)  # 1 minute
```

Or manually force pressure for testing:
```python
demo.cloud.force_pressure(80.0)  # Jump to critical
```

**Status**: Expected behavior - real gameplay generates more pressure.

---

### Missing Systems

The following systems are stubbed but not implemented in Phase 1:

- `bleed_events.py` - Sora clip integration
- `ao3_logs.py` - Log generation system
- `adjacency.py` - Probabilistic zone relationships

**Status**: Planned for Phase 2.

---

## Reporting Issues

For bugs or feature requests, please check that the issue is not already documented here before reporting.

When reporting, include:
- V4 version (currently V4.0.1-alpha)
- Python version
- Console output with error
- Steps to reproduce
