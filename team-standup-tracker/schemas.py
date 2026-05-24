from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class StandupUpdateBase(BaseModel):
    working_on: str
    status: str
    blockers: Optional[str] = None

class StandupUpdateCreate(StandupUpdateBase):
    member_id: int

class StandupUpdate(StandupUpdateBase):
    id: int
    member_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TeamMemberBase(BaseModel):
    name: str

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMember(TeamMemberBase):
    id: int
    updates: List[StandupUpdate] = []

    class Config:
        from_attributes = True

class TeamMemberWithLastUpdate(TeamMemberBase):
    id: int
    last_update: Optional[StandupUpdate] = None

    class Config:
        from_attributes = True
