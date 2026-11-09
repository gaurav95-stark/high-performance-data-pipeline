#!/usr/bin/env sh
set -eu
python -m pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
