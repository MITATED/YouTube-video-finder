from dataclasses import dataclass, is_dataclass, asdict
import json


@dataclass
class ResultItem:
    title: str
    video_url: str
    custom_score: float
    views: int
    channel_id: str
    channel_name: str
    num_subscribers: int
    view_subscriber_ratio: float
    channel_url: str


class ResultItemJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)
