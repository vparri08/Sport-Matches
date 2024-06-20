from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

from .teamCompetitionRelationship import TeamCompetitionRelationship


class Category(Enum):
    JUNIOR = "junior"
    SENIOR = "senior"
    VETERAN = "veteran"

class Sport(Enum):
    FOOTBALL = "football"
    BASKETBALL = "basketball"
    VOLLEYBALL = "volleyball"
    FUTSAL = "futsal"

# Shared properties
class CompetitionBase(SQLModel):
    name: str
    category: Category
    sport: Sport

# Database model, database table inferred from class name
class Competition(CompetitionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    teams: list["Team"] = Relationship(back_populates="competitions", link_model=TeamCompetitionRelationship)
    matches: list["Match"] = Relationship(back_populates="competition")

# Properties to receive via API on creation
class CompetitionCreate(CompetitionBase):
    pass

# Properties to receive via API on update, all are optional
class CompetitionUpdate(SQLModel):
    name: str | None = None
    category: Category | None = None
    sport: Sport | None = None

# Properties to return via API, id is always required
class CompetitionOut(CompetitionBase):
    id: int

# Properties to return multiple teams via API
class CompetitionsOut(SQLModel):
    data: list[CompetitionOut]
    count: int

# Generic message
class Message(SQLModel):
    message: str
