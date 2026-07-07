import uuid

from pydantic import BaseModel, ConfigDict, Field


class StockBase(BaseModel):
    ticker: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Stock ticker symbol (e.g., BBCA, BMRI)",
    )
    name: str = Field(
        ..., min_length=1, max_length=255, description="Full company name"
    )
    sector: str | None = Field(None, max_length=100, description="Business sector")
    current_price: float | None = Field(None, gt=0, description="Current stock price")
    description: str | None = Field(
        None, max_length=1000, description="Company description"
    )


class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    ticker: str | None = Field(
        None, min_length=1, max_length=10, description="Stock ticker symbol"
    )
    name: str | None = Field(
        None, min_length=1, max_length=255, description="Full company name"
    )
    sector: str | None = Field(None, max_length=100, description="Business sector")
    current_price: float | None = Field(None, gt=0, description="Current stock price")
    description: str | None = Field(
        None, max_length=1000, description="Company description"
    )


class StockResponse(StockBase):
    id: uuid.UUID = Field(..., description="Unique identifier for the stock")

    model_config = ConfigDict(from_attributes=True)


class StockList(BaseModel):
    stocks: list[StockResponse]
    total: int
    page: int
    page_size: int
