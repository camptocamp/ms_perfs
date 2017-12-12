#!/bin/bash
set -e

COMPOSE="/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose-perfs.yml"

export USERS
export BASE_URLS
export WARMUP
export TIME_PER_TEST

echo "Running perf script at $(date)" 
${COMPOSE} stop
${COMPOSE} rm -f
${COMPOSE} build
${COMPOSE} up --abort-on-container-exit || true

mkdir -p archives

./summary.py --csv --html --prefix archives/summary_
echo "Finished perf script at $(date)"
