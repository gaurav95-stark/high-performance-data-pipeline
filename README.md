# Real-Time Data Processing Pipeline

A Python/FastAPI project demonstrating concurrent event ingestion, bounded async queues, worker pools, interchangeable processing strategies, SQLite persistence, indexes, TTL caching, Prometheus metrics, tests, Docker and Kubernetes examples.

## Architecture
Client -> FastAPI validation -> bounded asyncio queue -> async workers -> Strategy -> Repository (SQLite WAL + indexes) -> TTL cache / query API. Observer notifications and Prometheus metrics expose pipeline behavior.

## Setup
Python 3.11+
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```
Docs: http://127.0.0.1:8000/docs | Health: `/health` | Metrics: `/metrics`

## Submit an event
```bash
curl -X POST http://127.0.0.1:8000/events -H "Content-Type: application/json" -d '{"event_id":"evt-001","event_type":"page_view","payload":{"page":"/home","user_id":42}}'
curl http://127.0.0.1:8000/events/evt-001
```

## Tests and benchmark
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
python -m performance.benchmark
```
Benchmark values are measured on the machine where you run the script. Do not claim figures from the assignment sample as measured results.

## Deployment
```bash
docker build -f docker/Dockerfile -t realtime-pipeline .
docker run --rm -p 8000:8000 -v pipeline-data:/app/data realtime-pipeline
kubectl apply -f kubernetes/
```

## Design patterns
- Strategy: `NormalizeStrategy` and `EnrichStrategy`
- Factory: `StrategyFactory`
- Observer: `EventObserver`
- Repository: `EventRepository`

## Analysis questions
1. Largest gains usually come from profiling first, reducing database round trips, suitable indexes, batching, bounded concurrency, and caching hot reads.
2. Stateless API replicas scale horizontally; independent workers and durable brokers decouple ingestion from processing.
3. Track throughput, p50/p95/p99 latency, queue depth/age, errors, CPU, memory, DB latency, and cache hit ratio.
4. Use async for I/O, threads for blocking I/O, processes for CPU-heavy Python, and bounded queues/semaphores for backpressure.
5. Caching risks staleness; more workers can increase contention; batching trades latency for throughput; durable brokers add operational complexity.

## Important production limitation
The demo queue is in-memory, so queued events are lost on process restart. For production, replace it with Kafka/RabbitMQ, add retries/dead-letter queues, authentication, schema versioning, distributed tracing, and PostgreSQL with migrations/connection pooling. SQLite is for local/demo use; do not share its file between Kubernetes replicas.

## Six-week plan
Week 1 architecture/setup; Week 2 ingestion/workers; Week 3 tests/profiling/indexes; Week 4 cache/metrics; Week 5 error handling/containerization; Week 6 deployment/benchmark/report.
