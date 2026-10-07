"""Edge case cho ID có lần xuất hiện đầu tiên với hours không hợp lệ."""

import json
import subprocess
import sys

import paths

SCRIPT = paths.WORKSPACE_DIR / "skills" / "csv-quality" / "scripts" / "check_csv.py"


def test_first_invalid_task_id_occurrence_still_marks_id_as_seen(tmp_path):
    source = tmp_path / "workload-edge.csv"
    source.write_text(
        "task_id,owner,hours\nE01,Lan,abc\nE01,Lan,5\nE02,Minh,0\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(source),
            "--max-hours",
            "0",
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["row_count"] == 3
    assert data["max_hours"] == 0
    assert data["hours_by_owner"] == {"Minh": 0}
    assert data["overloaded_owners"] == []
    assert data["excluded_rows"] == [
        {"line": 2, "task_id": "E01", "reasons": ["invalid_hours"]},
        {"line": 3, "task_id": "E01", "reasons": ["duplicate_id"]},
    ]
    assert [(issue["line"], issue["type"]) for issue in data["issues"]] == [
        (2, "invalid_hours"),
        (3, "duplicate_id"),
    ]
