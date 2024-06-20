from sqlmodel import Field
from .base import SQLModel


class TeamCompetitionRelationship(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    competition_id: int = Field(foreign_key="competition.id", primary_key=True)