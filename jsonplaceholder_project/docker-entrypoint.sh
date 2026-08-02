#!/bin/sh

set -e

echo "[entrypoint] Applying database migrations....."

RUN_MODE="${RUN_MODE:-once}"

if ["$RUN_MODE" = "schedule"]; then
    INTERVAL="${PIPELINE_INTERVAL_SECONDS:-60}"
    echo "[entrypoint] RUN_MODE = schedule - running every ${INTERVAL}S. Ctrl+C or docker compose stop' to end."
    while true; do
        echo "[entrypoint] $(date -u +%Y-%m-%dT%H:%M:%SZ) - starting pipeline run"
        python run_pipeline.py || echo "[entrypoint] pipeline run failed, will retry next interval"
        echo "[entrypoint] sleeping ${INTERVAL}s until next run"
        sleep "$INTERVAL"
    done
else
    echo "[entrypoint] RUN_MODE = once - running pipline a single time"
    exec python run_pipeline.py
fi