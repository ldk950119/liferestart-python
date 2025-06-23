
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Talent(BaseModel):
    id: int
    name: str
    desc: str
    effect: Dict[str, int] = Field(default_factory=dict)

class Event(BaseModel):
    id: int
    age: int
    desc: str
    effect: Dict[str, int] = Field(default_factory=dict)

class Ending(BaseModel):
    id: int
    desc: str
    cond: Dict[str, Optional[int]]

class LifeLog(BaseModel):
    age: int
    event_id: int
    desc: str

class LifeResult(BaseModel):
    log: List[LifeLog]
    final_age: int
    ending: Ending
