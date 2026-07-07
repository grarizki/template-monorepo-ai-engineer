from fastapi import HTTPException, status
from sqlmodel import Session, select

from ai_template.models.database import Stocks


def normalize_ticker(ticker: str) -> str:
    return ticker.upper().strip()


def get_stock_or_404(session: Session, ticker: str) -> Stocks:
    normalized = normalize_ticker(ticker)
    stock = session.exec(select(Stocks).where(Stocks.ticker == normalized)).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with ticker {normalized} not found",
        )
    return stock


def check_ticker_exists(session: Session, ticker: str) -> bool:
    normalized = normalize_ticker(ticker)
    return (
        session.exec(select(Stocks).where(Stocks.ticker == normalized)).first()
        is not None
    )
