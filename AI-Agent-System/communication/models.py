from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class Task(BaseModel):
    name: str
    priority: int
    parameters: Dict[str, Any]

class Message(BaseModel):
    message_id: str
    sender: str
    recipient: str
    type: str
    task: Optional[Task] = None
    related_message_id: Optional[str] = None
    status: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    timestamp: str

    @staticmethod
    def new(sender: str, recipient: str, msg_type: str, **kwargs):
        return Message(
            message_id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            type=msg_type,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs
        )
