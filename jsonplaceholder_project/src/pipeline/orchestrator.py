import logging
import time

from src.pipeline.extract import ExtractError, extract_comments, extract_posts, extract_users
from src.pipeline.transform import transform_address, transform_comment, transform_post, transform_user
from src.pipeline.load import load_addresses, load_comments, load_posts, load_users
from src.database import engine
from src.models import Base

logger = logging.getLogger(__name__)

class PipelineError(Exception):
    """Raised when the pipeline fails and cannot continue"""

def run_pipeline() -> dict[str, int]:
    start = time.monotonic()
    logger.info("Pipeline run started")

    try:
        # Base.metadata.create_all(bind=engine)
        raw_users = extract_users()
        raw_posts = extract_posts()
        raw_comments = extract_comments()
    except ExtractError:
        logger.exception("Pipeline aborted: extract stage failed")
        raise PipelineError("Extract stage failed")

    users = [transform_user(u) for u in raw_users]
    addresses = [transform_address(u) for u in raw_users]
    posts = [transform_post(u) for u in raw_posts]
    comments = [transform_comment(u) for u in raw_comments]

    counts = {
        "users": load_users(users),
        "addresses": load_addresses(addresses),
        "posts": load_posts(posts),
        "comments": load_comments(comments)
    }

    elapsed = time.monotonic() - start
    logger.info("Pipeline run completed in %.2fs: %s", elapsed, counts)
    return counts