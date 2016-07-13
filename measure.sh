#!/bin/bash
set -e

COMPOSE="docker-compose -f docker-compose.yml -f docker-compose-perfs.yml"

${COMPOSE} stop
${COMPOSE} rm -f --all
${COMPOSE} build
${COMPOSE} up
