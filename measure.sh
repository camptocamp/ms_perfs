#!/bin/bash
set -e

COMPOSE="docker-compose -f docker-compose.yml -f docker-compose-perfs.yml"

export USERS
export BASE_URLS
export WARMUP
export TIME_PER_TEST

${COMPOSE} stop
${COMPOSE} rm -f
${COMPOSE} build
${COMPOSE} up --abort-on-container-exit || true

./summary.py

echo "Summary file you can open with Excel or LibreOffice Calc: summary.py"
