import logging
import sys

from src.config import settings
from src.pipeline.orchestrator import PipelineError, run_pipeline

def configure_logging() -> None:
    logging.basicConfig(
        level=settings.log_level, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

def main() -> int:
    configure_logging()
    logger = logging.getLogger("run_pipeline")

    try:
        counts =  run_pipeline()
    except PipelineError as exc:
        logger.error("Pipeline failed: %s", exc)
        return 1
    except Exception:
        logger.exception("Unexpected error during pipline run")
        return 1

    logger.info("Row counts loaded: %s", counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())