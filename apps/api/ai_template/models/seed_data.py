from sqlmodel import Session, select

from ai_template.models.database import Stocks
from ai_template.models.engine import engine


def seed_stocks() -> None:
    dummy_stocks = [
        {
            "ticker": "BBCA",
            "name": "PT Bank Central Asia Tbk",
            "sector": "Banking",
            "current_price": 9800.0,
            "description": "Largest private bank in Indonesia by market capitalization",
        },
        {
            "ticker": "BMRI",
            "name": "PT Bank Mandiri (Persero) Tbk",
            "sector": "Banking",
            "current_price": 6250.0,
            "description": "Indonesia's largest bank by assets",
        },
        {
            "ticker": "BBRI",
            "name": "PT Bank Rakyat Indonesia (Persero) Tbk",
            "sector": "Banking",
            "current_price": 5100.0,
            "description": "State-owned bank focusing on micro and small enterprises",
        },
        {
            "ticker": "BUMI",
            "name": "PT Bumi Resources Tbk",
            "sector": "Mining",
            "current_price": 142.0,
            "description": "Coal mining company operating in Kalimantan",
        },
    ]

    with Session(engine) as session:
        for stock_data in dummy_stocks:
            existing = session.exec(
                select(Stocks).where(Stocks.ticker == stock_data["ticker"])
            ).first()
            if not existing:
                stock = Stocks(**stock_data)
                session.add(stock)
        session.commit()
