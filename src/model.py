from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Event(BaseModel):
    event_uuid: str
    created_at: int
    event_name: str
    created_datetime: Optional[datetime]
    event_type: Optional[str]
    event_subtype: Optional[str]