from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, func, select

from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import Message, Competition, CompetitionCreate, CompetitionsOut, CompetitionUpdate, CompetitionOut

router = APIRouter()

@router.get(
    "/",
    response_model=CompetitionsOut
)
def read_competitions(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve competitions.
    """
    count_statement = select(func.count()).select_from(Competition)
    count = session.exec(count_statement).one()

    statement = select(Competition).offset(skip).limit(limit)
    competitions = session.exec(statement).all()

    return CompetitionsOut(data=competitions, count=count)

@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=CompetitionOut
)
def create_competition(*, session: SessionDep, competition_in: CompetitionCreate) -> Any:
    """
    Create new competition.
    """
    competition = crud.competition.get_competition_by_name(session=session, name=competition_in.name)
    if competition:
        raise HTTPException(
            status_code=400,
            detail="The competition with this name already exists in the system.",
        )

    competition = crud.competition.create_competition(session=session, competition_create=competition_in)
    return competition

@router.patch("/{competition_id}", response_model=CompetitionOut)
def update_competition(
    *, session: SessionDep, competition_id: int, competition_in: CompetitionUpdate
) -> Any:
    """
    Update a competition.
    """
    db_competition = crud.competition.get_competition_by_id(session=session, competition_id=competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    db_competition = crud.competition.update_competition(session=session, db_competition=db_competition, competition_in=competition_in)
    return db_competition

@router.get("/{competition_id}", response_model=CompetitionOut)
def read_competition_by_id(
    *, session: SessionDep, competition_id: int
) -> Any:
    """
    Retrieve competition by name.
    """
    db_competition = crud.competition.get_competition_by_id(session=session, competition_id=competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return db_competition

@router.delete("/{competition_id}")
def delete_competition(
    *, session: SessionDep, competition_id: int
) -> Any:
    """
    Delete a competition.
    """
    db_competition = crud.competition.get_competition_by_id(session=session, competition_id=competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    crud.competition.delete_competition(session=session, db_competition=db_competition)
    return Message(message="Competition deleted")