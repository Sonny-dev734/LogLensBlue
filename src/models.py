# src/models.py

from typing import Optional, Dict, List
import uuid
from datetime import datetime


class Event:
    def __init__(
        self,
        id: str,
        timestamp: str,
        source: str,
        user: Optional[str],
        message: str,
        metadata: Dict[str, str]
    ):
        self.id = id
        self.timestamp = timestamp
        self.source = source
        self.user = user
        self.message = message
        self.metadata = metadata


class Alert:
    def __init__(
        self,
        id: str,
        event_id: str,
        rule_name: str,
        level: str,
        category: str,
        title: str,
        ip: Optional[str],
        user: Optional[str],
        timestamp: str,
        hint: str,
        tags: List[str] = None
    ):
        self.id = id
        self.event_id = event_id
        self.rule_name = rule_name
        self.level = level
        self.category = category
        self.title = title
        self.ip = ip
        self.user = user
        self.timestamp = timestamp
        self.hint = hint
        self.tags = tags or []


