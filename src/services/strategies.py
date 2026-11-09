from abc import ABC, abstractmethod

class ProcessingStrategy(ABC):
    @abstractmethod
    async def process(self, event):
        raise NotImplementedError

class NormalizeStrategy(ProcessingStrategy):
    async def process(self, event):
        return {"event_type": event["event_type"],
                "normalized_payload": {str(k).strip().lower(): v for k, v in event["payload"].items()}}

class EnrichStrategy(ProcessingStrategy):
    async def process(self, event):
        payload = event["payload"]
        return {"event_type": event["event_type"], "field_count": len(payload),
                "has_user_id": "user_id" in payload,
                "normalized_payload": {str(k).strip().lower(): v for k, v in payload.items()}}

class StrategyFactory:
    @staticmethod
    def create(name):
        choices = {"normalize": NormalizeStrategy, "enrich": EnrichStrategy}
        if name not in choices:
            raise ValueError(f"Unknown processing strategy: {name}")
        return choices[name]()
