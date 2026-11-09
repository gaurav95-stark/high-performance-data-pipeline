from prometheus_client import Counter, Histogram, Gauge
EVENTS_ACCEPTED = Counter("pipeline_events_accepted_total", "Accepted events")
EVENTS_PROCESSED = Counter("pipeline_events_processed_total", "Processed events")
EVENTS_FAILED = Counter("pipeline_events_failed_total", "Failed events")
PROCESSING_SECONDS = Histogram("pipeline_processing_seconds", "Event processing duration")
QUEUE_DEPTH = Gauge("pipeline_queue_depth", "Current queue depth")
ACTIVE_WORKERS = Gauge("pipeline_active_workers", "Configured worker count")
