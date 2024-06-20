from sqlmodel import Field, Relationship, SQLModel
from .match import Match


class AccountBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True, foreign_key="user.id")
    available_money: float | None = 0


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True, foreign_key="user.id")
    orders: list["Order"] = Relationship(back_populates="account")
    user: "User" = Relationship(back_populates="account")

class AccountUpdate(AccountBase):
    available_money: float

class OrderBase(SQLModel):
    tickets_bought: int
    match_id: int | None = Field(default=None, foreign_key="match.id")


class Order(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tickets_bought: int
    account_id: int | None = Field(default=None, foreign_key="account.id")
    match_id: int | None = Field(default=None, foreign_key="match.id")
    account: Account = Relationship(back_populates="orders")
    match: Match = Relationship(back_populates="orders")


class OrderCreate(OrderBase):
    match_id: int
    tickets_bought: int


class OrderOut(OrderBase):
    id: int
    account_id: int | None = None