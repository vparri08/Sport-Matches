from sqlalchemy import Boolean, MetaData, Column, ForeignKey, Integer, String, Date, Float, Enum, UniqueConstraint, \
    Table, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Team(Base):
    __tablename__ = 'teams' #This is table name

    id = Column(Integer, primary_key=True)
    name = Column(String(30),unique=True, nullable=False, index=True)
    country = Column(String(30),nullable=False)
    description = Column(String(100))

teams_in_competitions = Table("teams_in_competitions",Base.metadata,
                                 Column("id", Integer, primary_key=True),
                                 Column("team_id", Integer, ForeignKey("teams.id")),
                                 Column("competition_id",Integer, ForeignKey("competitions.id")))

class Competition(Base):

    __tablename__ = 'competitions'  # This is table name
    __table_args__ = (UniqueConstraint('name', 'category', 'sport'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    category = Column(Enum(*categories_list),nullable=False)
    sport = Column(Enum(*sports_list),nullable=False)
    teams = relationship("Team",secondary=teams_in_competitions,backref="competitions")

class Match(Base):
    __tablename__ = 'matches' #This is table name
    __table_args__ = (UniqueConstraint('local_id', 'visitor_id', 'competition_id', 'date'),)

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    competition = relationship("Competition",backref="matches")

    local_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    visitor_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    local = relationship("Team", foreign_keys=local_id)
    visitor = relationship("Team", foreign_keys=visitor_id)