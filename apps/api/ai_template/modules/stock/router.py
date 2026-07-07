from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ai_template.models.database import Stocks
from ai_template.models.engine import db_session
from ai_template.models.seed_data import seed_stocks
from ai_template.modules.stock.schema import (
    StockCreate,
    StockList,
    StockResponse,
    StockUpdate,
)
from ai_template.utils.pagination import paginate_query
from ai_template.utils.stock_helpers import (
    check_ticker_exists,
    get_stock_or_404,
    normalize_ticker,
)

stocks_router = APIRouter(prefix="/stocks", tags=["Stocks"])


@stocks_router.post(
    "/", response_model=StockResponse, status_code=status.HTTP_201_CREATED
)
def create_stock(stock: StockCreate, session: Session = Depends(db_session)):
    normalized_ticker = normalize_ticker(stock.ticker)
    if check_ticker_exists(session, normalized_ticker):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock with ticker {normalized_ticker} already exists",
        )
    stock_data = stock.model_dump()
    stock_data["ticker"] = normalized_ticker
    db_stock = Stocks(**stock_data)
    session.add(db_stock)
    session.commit()
    session.refresh(db_stock)
    return db_stock


@stocks_router.get("/", response_model=StockList)
def get_stocks(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    sector: str | None = Query(None, description="Filter by sector"),
    session: Session = Depends(db_session),
):
    query = select(Stocks)
    if sector:
        query = query.where(Stocks.sector == sector)
    result = paginate_query(session, query, page, page_size)
    stocks = [StockResponse.model_validate(s) for s in result.items]
    return StockList(
        stocks=stocks, total=result.total, page=result.page, page_size=result.page_size
    )


@stocks_router.get("/{ticker}", response_model=StockResponse)
def get_stock(ticker: str, session: Session = Depends(db_session)):
    return get_stock_or_404(session, ticker)


@stocks_router.patch("/{ticker}", response_model=StockResponse)
def update_stock(
    ticker: str, stock_update: StockUpdate, session: Session = Depends(db_session)
):
    stock = get_stock_or_404(session, ticker)
    update_data = stock_update.model_dump(exclude_unset=True)
    if "ticker" in update_data:
        new_ticker = normalize_ticker(update_data["ticker"])
        if new_ticker != stock.ticker and check_ticker_exists(session, new_ticker):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock with ticker {new_ticker} already exists",
            )
        update_data["ticker"] = new_ticker
    for key, value in update_data.items():
        setattr(stock, key, value)
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock


@stocks_router.delete("/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock(ticker: str, session: Session = Depends(db_session)):
    stock = get_stock_or_404(session, ticker)
    session.delete(stock)
    session.commit()


@stocks_router.post("/seed", status_code=status.HTTP_200_OK)
def seed_stocks_endpoint():
    try:
        seed_stocks()
        return {"message": "Dummy stocks seeded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error seeding stocks: {str(e)}",
        )
