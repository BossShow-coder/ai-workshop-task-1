from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from database import Base

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    updates = relationship("StandupUpdate", back_populates="member")

class StandupUpdate(Base):
    __tablename__ = "standup_updates"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("team_members.id"))
    working_on = Column(Text)
    status = Column(String)
    blockers = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    member = relationship("TeamMember", back_populates="updates")
