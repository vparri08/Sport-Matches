from typing import Any

from sqlmodel import Session, select

from app.models import Team, TeamCreate, TeamUpdate


def create_team(*, session: Session, team_create: TeamCreate) -> Team:
    db_obj = Team.model_validate(team_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_team(*, session: Session, db_team: Team, team_in: TeamUpdate) -> Any:
    team_data = team_in.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


def get_team_by_name(*, session: Session, name: str) -> Team | None:
    statement = select(Team).where(Team.name == name)
    session_team = session.exec(statement).first()
    return session_team


def get_team_by_id(*, session: Session, team_id: int) -> Team | None:
    statement = select(Team).where(Team.id == team_id)
    session_team = session.exec(statement).first()
    return session_team


def delete_team(*, session: Session, db_team: Team) -> None:
    session.delete(db_team)
    session.commit()
