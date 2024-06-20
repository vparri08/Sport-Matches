from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, func, select

from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import Message, Team, TeamCreate, TeamOut, TeamsOut, TeamUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=TeamsOut
)
def read_teams(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve teams.
    """
    count_statement = select(func.count()).select_from(Team)
    count = session.exec(count_statement).one()

    statement = select(Team).offset(skip).limit(limit)
    teams = session.exec(statement).all()

    return TeamsOut(data=teams, count=count)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=TeamOut
)
def create_team(*, session: SessionDep, team_in: TeamCreate) -> Any:
    """
    Create new team.
    """
    team = crud.team.get_team_by_name(session=session, name=team_in.name)
    if team:
        raise HTTPException(
            status_code=400,
            detail="The team with this name already exists in the system.",
        )

    team = crud.team.create_team(session=session, team_create=team_in)
    return team


@router.patch("/{team_name}", response_model=TeamOut)
def update_team(
    *, session: SessionDep, team_name: str, team_in: TeamUpdate
) -> Any:
    """
    Update a team.
    """
    db_team = crud.team.get_team_by_name(session=session, name=team_name)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    db_team = crud.team.update_team(session=session, db_team=db_team, team_in=team_in)
    return db_team


@router.get("/{team_name}", response_model=TeamOut)
def read_team_by_name(
    *, session: SessionDep, team_name: str
) -> Any:
    """
    Retrieve team by name.
    """
    db_team = crud.team.get_team_by_name(session=session, name=team_name)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.get("/{team_id}", response_model=TeamOut)
def read_team_by_id(
    *, session: SessionDep, id: int
) -> Any:
    """
    Retrieve team by id.
    """
    db_team = crud.team.get_team_by_id(session=session, team_id=id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.delete("/{team_name}")
def delete_team(
    *, session: SessionDep, team_name: str
) -> Any:
    """
    Delete a team.
    """
    db_team = crud.team.get_team_by_name(session=session, name=team_name)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    crud.team.delete_team(session=session, db_team=db_team)
    return Message(message="Team deleted")
