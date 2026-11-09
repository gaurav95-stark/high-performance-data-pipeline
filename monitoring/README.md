# Monitoring

Prometheus metrics are exposed at `/metrics`: accepted/processed/failed event counters, processing duration histogram, queue depth gauge and configured worker gauge. `/health` reports service health and queue depth; `/cache/stats` reports cache hits, misses and hit ratio.

Recommended Grafana panels: events/sec, p50/p95/p99 processing latency, queue depth/age, failure rate, CPU/memory, DB latency, and cache hit ratio. Alert on sustained queue growth, worker saturation, high error rate and elevated tail latency.
