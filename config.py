
from dataclasses import dataclass


@dataclass
class DefaultCFG:

    sleep_time_between_requests: int = 15
    api_key: str = "your-api"
    model_name: str = "gemini-2.0-flash"
    

    