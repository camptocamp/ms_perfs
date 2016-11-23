#!/bin/bash
set -e

COMPOSE="docker-compose -f docker-compose.yml -f docker-compose-perfs.yml"

${COMPOSE} stop
${COMPOSE} rm -f
${COMPOSE} build
${COMPOSE} up --abort-on-container-exit || true

./summary.py

echo "Summary file you can open with Excel or LibreOffice Calc: summary.py"
