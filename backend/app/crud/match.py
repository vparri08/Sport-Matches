from typing import Any, Optional

from sqlmodel import Session, select

from app.models import Match, MatchCreate, MatchUpdate


def create_match(*, session: Session, match_create: MatchCreate) -> Match:
    db_obj = Match.model_validate(match_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_match(*, session: Session, db_match: Match, match_in: MatchUpdate) -> Any:
    match_data = match_in.model_dump(exclude_unset=True)
    db_match.sqlmodel_update(match_data)
    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match


def get_match_by_id(*, session: Session, match_id: int) -> Match | None:
    statement = select(Match).where(Match.id == match_id)
    session_match = session.exec(statement).first()
    return session_match


def delete_match(*, session: Session, db_match: Match) -> None:
    session.delete(db_match)
    session.commit()