from pydantic import BaseModel
from typing import List, Optional

class Resource(BaseModel):
    id: int
    type: str
    quantity: int

class Volunteer(BaseModel):
    id: int
    name: str
    skills: List[str]
    availability: int  # hours available

class DisasterZone(BaseModel):
    id: int
    name: str
    severity: int  # severity level of the disaster
    required_resources: List[Resource]
    required_volunteers: int

class Allocation(BaseModel):
    zone: DisasterZone
    allocated_resources: List[Resource]
    allocated_volunteers: List[Volunteer]
    unmet_severity: Optional[int] = None  # severity that could not be met