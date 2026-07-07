from pydantic import BaseModel
from sqlmodel import Session, func, select


class PaginationResult(BaseModel):
    items: list
    total: int
    page: int
    page_size: int


def paginate_query(
    session: Session, query, page: int, page_size: int
) -> PaginationResult:
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()
    offset = (page - 1) * page_size
    items = session.exec(query.offset(offset).limit(page_size)).all()
    return PaginationResult(items=items, total=total, page=page, page_size=page_size)
