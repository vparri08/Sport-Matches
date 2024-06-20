from sqlmodel import SQLModel, Field, Relationship

from .teamCompetitionRelationship import TeamCompetitionRelationship


# Shared properties
class TeamBase(SQLModel):
    name: str
    country: str
    description: str | None = None

# Database model, database table inferred from class name
class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    competitions: list["Competition"] = Relationship(back_populates="teams", link_model=TeamCompetitionRelationship)

# Properties to receive via API on creation
class TeamCreate(TeamBase):
    pass

# Properties to receive via API on update, all are optional
class TeamUpdate(SQLModel):
    name: str | None = None
    country: str | None = None
    description: str | None = None

# Properties to return via API, id is always required
class TeamOut(TeamBase):
    id: int

# Properties to return multiple teams via API
class TeamsOut(SQLModel):
    data: list[TeamOut]
    count: int

# Generic message
class Message(SQLModel):
    message: str
