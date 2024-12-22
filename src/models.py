from pydantic import BaseModel
from typing import List, Optional

class Relationship(BaseModel):
    target_id: str
    type: str
    properties: Optional[dict] = {}

class Entity(BaseModel):
    id: str
    type: str
    properties: dict
    relationships: List[Relationship]
#hello pandu
# Endpoint function
class QueryRequest(BaseModel):
    question: str  # Ensure that 'question' is a required string field