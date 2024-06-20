from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import Match, MatchCreate, MatchOut, MatchesOut, MatchUpdate, Message

router = APIRouter()


@router.get(
    "/",
    response_model=MatchesOut
)
def read_matches(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve matches.
    """
    count_statement = select(func.count()).select_from(Match)
    count = session.exec(count_statement).one()

    statement = select(Match).offset(skip).limit(limit)
    matches = session.exec(statement).all()

    return MatchesOut(data=matches, count=count)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MatchOut
)
def create_match(*, session: SessionDep, match_in: MatchCreate) -> Any:
    """
    Create new match.
    """
    match = crud.match.create_match(session=session, match_create=match_in)
    return match


@router.patch("/{match_id}", response_model=MatchOut)
def update_match(
    *, session: SessionDep, match_id: int, match_in: MatchUpdate
) -> Any:
    """
    Update a match.
    """
    db_match = crud.match.get_match_by_id(session=session, match_id=match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    db_match = crud.match.update_match(session=session, db_match=db_match, match_in=match_in)
    return db_match


@router.get("/{match_id}", response_model=MatchOut)
def read_match_by_id(
    *, session: SessionDep, match_id: int
) -> Any:
    """
    Retrieve match by ID.
    """
    db_match = crud.match.get_match_by_id(session=session, match_id=match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@router.delete("/{match_id}")
def delete_match(
    *, session: SessionDep, match_id: int
) -> Any:
    """
    Delete a match.
    """
    db_match = crud.match.get_match_by_id(session=session, match_id=match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    crud.match.delete_match(session=session, db_match=db_match)
    return Message(message="Match deleted")