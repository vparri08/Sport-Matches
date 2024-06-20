from http.client import HTTPException

from sqlmodel import Session, select
from typing import List, Any
from app.models import User, Match, Account, Order, OrderCreate, OrderOut, AccountBase, AccountUpdate

def create_account(*, session: Session, account: AccountBase) -> Account:
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def get_user_account(*, session: Session, user_id: int) -> Account:
    return session.get(Account, user_id)


def get_orders_by_username(*, session: Session, username: str) -> List[Order]:
    statement = select(User).where(User.email == username)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    account = user.account
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.orders


def get_ordered_matches(*, session: Session, user_id: int) -> List[Match]:
    user = session.get(User, user_id)
    account = user.account
    orders = account.orders
    matches = [order.match for order in orders]
    return matches


def create_order(*, session: Session, account_id: int, order: OrderCreate) -> Order:
    order = Order(**order.dict(), account_id=account_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_all_orders(*, session: Session) -> List[Order]:
    statement = select(Order)
    return session.exec(statement).all()


def delete_order(*, session: Session, order: Order):
    session.delete(order)
    session.commit()


def update_available_tickets(*, session: Session, order: Order):
    match = order.match
    match.total_available_tickets -= order.tickets_bought
    session.add(match)
    session.commit()


def update_account(*, session: Session, db_account: Account, account_in: AccountUpdate) -> Any:
    account_data = account_in.model_dump(exclude_unset=True)
    db_account.sqlmodel_update(account_data)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


def add_order_to_account(*, session: Session, account: Account, order: Order):
    account.orders.append(order)
    session.add(account)
    session.commit()