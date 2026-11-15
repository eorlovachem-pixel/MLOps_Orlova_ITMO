#!/usr/bin/env bash
set -euo pipefail
# Run in HW3 project root after installing uv and Git.
uv sync
python scripts/bootstrap_remote.py
uv run dvc pull
uv run dvc status
uv run dvc repro
uv run dvc dag
uv run dvc metrics show
uv run dvc push
uv run dvc status -c
printf '
Add the generated uv.lock and updated DVC metadata to Git before submission.
'
