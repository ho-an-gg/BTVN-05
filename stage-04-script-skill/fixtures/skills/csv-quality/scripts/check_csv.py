#!/usr/bin/env python3
"""Kiểm tra chất lượng CSV công việc và tính tổng giờ theo owner.

Chạy từ workspace:
    python skills/csv-quality/scripts/check_csv.py --input data/tasks.csv --max-hours 8

Exit 0: CSV đã được phân tích, kể cả khi có dòng bị loại hoặc owner quá tải.
Exit khác 0: lỗi đầu vào hoặc tham số; thông báo lỗi được ghi ra stderr.
Script chỉ đọc CSV, không sửa file đầu vào.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys

REQUIRED_COLUMNS = ("task_id", "owner", "hours")
REASON_ORDER = (
    "wrong_field_count",
    "missing_task_id",
    "duplicate_id",
    "missing_owner",
    "invalid_hours",
)


class InputError(Exception):
    pass


def parse_hours(raw: str | None) -> float | None:
    """Số giờ hợp lệ là số hữu hạn không âm; trả None nếu không hợp lệ."""
    if raw is None or not raw.strip():
        return None
    try:
        value = float(raw.strip())
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return value


def parse_max_hours(raw: str) -> float:
    """Đọc ngưỡng hữu hạn, không âm; báo lỗi nếu giá trị không hợp lệ."""
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("phải là một số hữu hạn không âm") from exc
    if not math.isfinite(value) or value < 0:
        raise argparse.ArgumentTypeError("phải là một số hữu hạn không âm")
    return value


def analyze(path: str, max_hours: float) -> dict:
    try:
        handle = open(path, encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise InputError(f"Không đọc được file {path}: {exc.strerror or exc}") from exc

    with handle:
        reader = csv.reader(handle, strict=True)
        try:
            header = next(reader, None)
            if header is None:
                raise InputError(f"File {path} rỗng, không có header.")
            columns = [column.strip() for column in header]
            missing = [column for column in REQUIRED_COLUMNS if column not in columns]
            if missing:
                raise InputError(
                    f"Thiếu cột bắt buộc: {', '.join(missing)}. "
                    f"Header hiện có: {', '.join(columns)}"
                )
            index = {name: columns.index(name) for name in REQUIRED_COLUMNS}

            row_count = 0
            wrong_field_count = 0
            missing_owner_count = 0
            invalid_hours_count = 0
            first_seen: dict[str, int] = {}
            duplicate_ids: list[str] = []
            issues: list[dict] = []
            excluded_rows: list[dict] = []
            hours_by_owner: dict[str, float] = {}

            for row in reader:
                line = reader.line_num
                if not any(cell.strip() for cell in row):
                    continue
                row_count += 1

                def cell(name: str) -> str:
                    position = index[name]
                    return row[position].strip() if position < len(row) else ""

                task_id = cell("task_id")
                owner = cell("owner")
                raw_hours = cell("hours")
                reasons: list[str] = []

                if len(row) != len(columns):
                    wrong_field_count += 1
                    reasons.append("wrong_field_count")
                    issues.append({
                        "line": line,
                        "column": None,
                        "type": "wrong_field_count",
                        "task_id": task_id or None,
                        "message": f"Có {len(row)} trường, header có {len(columns)} cột.",
                    })

                if not task_id:
                    reasons.append("missing_task_id")
                    issues.append({
                        "line": line,
                        "column": "task_id",
                        "type": "missing_task_id",
                        "task_id": None,
                        "message": "task_id trống.",
                    })
                elif task_id in first_seen:
                    reasons.append("duplicate_id")
                    if task_id not in duplicate_ids:
                        duplicate_ids.append(task_id)
                    issues.append({
                        "line": line,
                        "column": "task_id",
                        "type": "duplicate_id",
                        "task_id": task_id,
                        "message": f"task_id {task_id} đã xuất hiện ở line {first_seen[task_id]}.",
                    })
                else:
                    # Đánh dấu lần đầu ngay cả khi dòng này còn lỗi dữ liệu.
                    first_seen[task_id] = line

                if not owner:
                    missing_owner_count += 1
                    reasons.append("missing_owner")
                    issues.append({
                        "line": line,
                        "column": "owner",
                        "type": "missing_owner",
                        "task_id": task_id or None,
                        "message": "owner trống.",
                    })

                hours = parse_hours(raw_hours)
                if hours is None:
                    invalid_hours_count += 1
                    reasons.append("invalid_hours")
                    issues.append({
                        "line": line,
                        "column": "hours",
                        "type": "invalid_hours",
                        "task_id": task_id or None,
                        "value": raw_hours,
                        "message": f"hours '{raw_hours}' không phải số hữu hạn không âm.",
                    })

                if reasons:
                    reason_set = set(reasons)
                    excluded_rows.append({
                        "line": line,
                        "task_id": task_id or None,
                        "reasons": [reason for reason in REASON_ORDER if reason in reason_set],
                    })
                    continue

                hours_by_owner[owner] = hours_by_owner.get(owner, 0.0) + hours

        except csv.Error as exc:
            raise InputError(f"Lỗi parse CSV ở line {reader.line_num}: {exc}") from exc
        except UnicodeDecodeError as exc:
            raise InputError(f"File {path} không phải UTF-8: {exc}") from exc

    overloaded_owners = [
        {"owner": owner, "total_hours": total}
        for owner, total in sorted(hours_by_owner.items())
        if total > max_hours
    ]
    return {
        "input": path,
        "row_count": row_count,
        "wrong_field_count": wrong_field_count,
        "missing_owner_count": missing_owner_count,
        "invalid_hours_count": invalid_hours_count,
        "duplicate_id_count": len(duplicate_ids),
        "duplicate_ids": duplicate_ids,
        "issues": sorted(issues, key=lambda item: item["line"]),
        "max_hours": max_hours,
        "hours_by_owner": hours_by_owner,
        "overloaded_owners": overloaded_owners,
        "excluded_rows": sorted(excluded_rows, key=lambda item: item["line"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Kiểm tra chất lượng CSV và tổng giờ theo owner."
    )
    parser.add_argument("--input", required=True, help="Đường dẫn CSV, ví dụ data/tasks.csv")
    parser.add_argument(
        "--max-hours",
        required=True,
        type=parse_max_hours,
        help="Ngưỡng giờ tối đa; phải là số hữu hạn không âm",
    )
    args = parser.parse_args(argv)
    try:
        result = analyze(args.input, args.max_hours)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
