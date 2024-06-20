import enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# Team Schemas

class TeamBase(SQLModel):
    name: str
    country: str

class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TeamCreate(TeamBase):
    pass

class TeamUpdate(SQLModel):
    name: Optional[str] = None
    country: Optional[str] = None

class TeamOut(TeamBase):
    id: int

class TeamsOut(SQLModel):
    data: List[TeamOut]
    count: int

# Competition Schemas

class CompetitionBase(SQLModel):
    name: str
    category: str  # Assuming the use of string for simplicity, use Enum if needed
    sport: str     # Assuming the use of string for simplicity, use Enum if needed

class Competition(CompetitionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class CompetitionCreate(CompetitionBase):
    pass

class CompetitionUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    sport: Optional[str] = None

class CompetitionOut(CompetitionBase):
    id: int

class CompetitionsOut(SQLModel):
    data: List[CompetitionOut]
    count: int

# Match Schemas

class MatchBase(SQLModel):
    date: datetime
    price: float
    total_available_tickets: int

class Match(MatchBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    local_id: int | None
    visitor_id: int | None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(SQLModel):
    date: datetime | None = None
    price: float | None = None
    total_available_tickets: int | None = None

class MatchOut(MatchBase):
    id: int
    local_id: int
    visitor_id: int

class MatchesOut(SQLModel):
    data: list[MatchOut]
    count: int

# Generic message
class Message(SQLModel):
    message: str


