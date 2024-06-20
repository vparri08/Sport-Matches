from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from .competition import Competition
from .team import Team


class MatchBase(SQLModel):
    date: datetime
    price: float
    total_available_tickets: int
    local_team: str
    visitor_team: str

class Match(MatchBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    competition_id: int | None = Field(default=None, foreign_key="competition.id")
    local_id: int | None = Field(default=None, foreign_key="team.id")
    visitor_id: int | None = Field(default=None, foreign_key="team.id")
    orders: list["Order"] | None = Relationship(back_populates="match")
    competition: Competition = Relationship(back_populates="matches")

class MatchCreate(MatchBase):
    competition_id: int

class MatchUpdate(SQLModel):
    date: datetime | None = None
    price: float | None = None
    total_available_tickets: int | None = None

class MatchOut(MatchBase):
    id: int
    competition_id: int

class MatchesOut(SQLModel):
    data: list[MatchOut]
    count: int

# Generic message
class Message(SQLModel):
    message: str
