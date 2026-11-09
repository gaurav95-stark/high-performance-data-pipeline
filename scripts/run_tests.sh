#!/usr/bin/env sh
set -eu
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
