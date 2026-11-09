# Local validation record

Environment: execution container, Python 3.13.5. Hardware specifications were not exposed, so CPU/RAM are intentionally not reported.

## Automated tests
- Test cases passed: 9
- Test cases failed: 0
- Total statement/branch coverage report: **92.05%**
- Required threshold: 80%
- Command: `pytest --cov=src --cov-report=term-missing --cov-fail-under=80`

## Throughput smoke benchmark
- Events: 500
- Workers: 4
- Elapsed: 0.8694 seconds
- Throughput: **575.08 events/second**

This is one smoke-test run in a shared execution environment, not a production capacity guarantee. Repeat on the target machine, capture p95/p99 latency and resource use, and compare multiple worker counts before making performance claims.
