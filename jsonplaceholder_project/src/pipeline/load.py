import logging

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Address, Comment, User, Post

logger = logging.getLogger(__name__)

def _upsert(session: Session, model, rows: list[dict], conflict_col:str) -> int:
    if not rows:
        return 0
    stmt = pg_insert(model).values(rows)
    update_cols = {
        c.name: getattr(stmt.excluded, c.name) 
        for c in model.__table__.columns 
        if c.name not in (conflict_col, "loaded_at")
    }
    stmt = stmt.on_conflict_do_update(index_elements=[conflict_col], set_=update_cols)
    session.execute(stmt)
    return len(rows)

def load_users(users: list[dict]) -> int:
    with get_session() as session:
        count = _upsert(session, User, users, conflict_col="id")
    logger.info("Upserted %d users", count)
    return count

def load_addresses(addresses: list[dict]) -> int:
    with get_session() as session:
        count = _upsert(session, Address, addresses, conflict_col="user_id")
    logger.info("Upserted %d in addresses", count)
    return count

def load_posts(posts: list[dict]) -> int:
    with get_session() as session:
        count = _upsert(session, Post, posts, conflict_col="id")
    logger.info("Upserted %d posts", count)
    return count

def load_comments(comments: list[dict]) -> int:
    with get_session() as session:
        count = _upsert(session, Comment, comments, conflict_col="id")
    logger.info("Upserted %d comments", count)
    return count