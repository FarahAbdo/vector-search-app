from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid


class VectorDocument(BaseModel):
    id: str
    text: str
    vector: List[float]
    category: str
    timestamp: str  # Changed from datetime to str
    metadata: Optional[dict] = None

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow().isoformat()  # Convert to ISO format string
        super().__init__(**data)


class SearchQuery(BaseModel):
    query: str
    top_k: int = 5
    category: Optional[str] = None

