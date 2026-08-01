import logging

import requests
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings
from src.schemas import CommentSchema, PostSchema, UserSchema

logger = logging.getLogger(__name__)

class ExtractError(Exception):
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    reraise=True,
)
def _get(endpoint: str) -> list[dict]:
    url=f"{settings.jsonplaceholder_base_url}/{endpoint}"
    logger.info("Requesting %s",url)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_users() -> list[UserSchema]:
    raw = _get("users")
    try:
        users = [UserSchema.model_validate(u) for u in raw]
    except ValidationError as exc:
        raise ExtractError(f"User payload failed validation: {exc}") from exc
    logger.info("Extracted %d users ", len(users))
    return users

def extract_posts() -> list[PostSchema]:
    raw = _get("posts")
    try:
        posts = [PostSchema.model_validate(u) for u in raw]
    except ValidationError as exc:
        raise ExtractError(f"Post payload failed validation: {exc}") from exc
    logger.info("Extracted %d posts ", len(posts))
    return posts

def extract_comments() -> list[CommentSchema]:
    raw = _get("comments")
    try:
        comments = [CommentSchema.model_validate(u) for u in raw]
    except ValidationError as exc:
        raise ExtractError(f"Comments payload failed validation: {exc}") from exc
    logger.info("Extracted %d comments ", len(comments))
    return comments    