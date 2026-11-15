"""Дополнительный DVC smoke-test — запускается при установленном DVC CLI."""

import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.dvc
def test_dvc_dag_parses_configuration() -> None:
    """Тест без изменения артефактов, проверяет корректность DAG."""
    dvc = shutil.which("dvc")
    if dvc is None:
        pytest.skip("DVC CLI отсутствует в PATH; используйте uv run pytest")
    project_root = Path(__file__).resolve().parents[1]
    completed = subprocess.run([dvc, "dag"], cwd=project_root, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    assert "prepare" in completed.stdout
    assert "train" in completed.stdout
    assert "evaluate" in completed.stdout
