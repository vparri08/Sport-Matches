from typing import Any

from sqlmodel import Session, select

from app.models import Competition, CompetitionCreate, CompetitionUpdate

def create_competition(*, session: Session, competition_create: CompetitionCreate) -> Competition:
    db_obj = Competition.model_validate(competition_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_competition(*, session: Session, db_competition: Competition, competition_in: CompetitionUpdate) -> Any:
    competition_data = competition_in.model_dump(exclude_unset=True)
    db_competition.sqlmodel_update(competition_data)
    session.add(db_competition)
    session.commit()
    session.refresh(db_competition)
    return db_competition

def get_competition_by_name(*, session: Session, name: str) -> Competition | None:
    statement = select(Competition).where(Competition.name == name)
    session_competition = session.exec(statement).first()
    return session_competition

def get_competition_by_id(*, session: Session, competition_id: int) -> Competition | None:
    statement = select(Competition).where(Competition.id == competition_id)
    session_competition = session.exec(statement).first()
    return session_competition

def delete_competition(*, session: Session, db_competition: Competition) -> None:
    session.delete(db_competition)
    session.commit()