from sqlalchemy.orm import Session
from app.models import Quotes 


def search_clients(db: Session, name: str):
    return db.query(Quotes.client_name)\
        .filter(Quotes.client_name.ilike(f"%{name}%"))\
        .distinct()\
        .limit(5)\
        .all()