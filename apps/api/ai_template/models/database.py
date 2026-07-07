import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(description="User's full name")
    email: str = Field(index=True, unique=True, description="User's email address")
    password: str = Field(description="Hashed password")


class Stocks(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    ticker: str = Field(
        index=True,
        unique=True,
        max_length=10,
        description="Stock ticker symbol (e.g., BBCA, BMRI)",
    )
    name: str = Field(description="Full company name")
    sector: str | None = Field(default=None, description="Business sector")
    current_price: float | None = Field(default=None, description="Current stock price")
    description: str | None = Field(default=None, description="Company description")
    stock_from: str | None = Field(default="Stock from where")
