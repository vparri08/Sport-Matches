from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from app import crud
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser
from app.models import Order, AccountBase, OrderCreate, OrderOut, MatchesOut, User, Match, Account, AccountUpdate
from sqlmodel import and_, select
from datetime import datetime, timedelta

router = APIRouter()
@router.post('/create_account', response_model=AccountBase)
async def create_account(*, session: SessionDep, account: AccountBase):
    account_in_bd = session.get(Account, account.id)
    user = session.get(User, account.id)
    if account_in_bd:
        raise HTTPException(
            status_code=409, detail="Account with this user id already exists"
        )
    if not user:
        raise HTTPException(
            status_code=409, detail="There has to exist a user with this id"
        )
    account.available_money = 0
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get('/account', response_model=AccountBase)
async def get_user_account(*, session: SessionDep, user: CurrentUser) -> Any:
    account = crud.order.get_user_account(session=session, user_id=user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountBase(id=user.id, available_money=account.available_money)


@router.get('/orders/{username}', response_model=List[Order])
def get_orders_by_username(*, session: SessionDep, username: str):
    orders = crud.order.get_orders_by_username(session=session, username=username)
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return orders


@router.get('/ordered_matches', response_model=MatchesOut)
def get_ordered_matches(*, session: SessionDep, user: CurrentUser):
    matches = crud.order.get_ordered_matches(session=session, user_id=user.id)
    if not matches:
        raise HTTPException(status_code=404, detail="Matches not found")
    return MatchesOut(data=matches, count=len(matches))


@router.post('/order', response_model=Order)
def create_order(*, session: SessionDep, current_user: CurrentUser, order: OrderCreate):
    return crud.order.create_order(session=session, account_id=current_user.account.id, order=order)


@router.get('/orders', response_model=List[OrderOut])
def get_all_orders(*, session: SessionDep):
    return crud.order.get_all_orders(session=session)

@router.patch('/account', response_model=AccountBase)
def update_account(*, session: SessionDep, account: AccountUpdate):
    db_account = session.get(Account, account.id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return crud.order.update_account(session=session, db_account=db_account, account_in=account)
