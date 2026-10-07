# Báo cáo kiểm tra CSV: `{đường dẫn CSV}`

- **Ngưỡng tối đa:** {max_hours} giờ
- **Công cụ:** `skills/csv-quality/scripts/check_csv.py`
- **Mã thoát:** {exit_code}

## Tổng giờ theo người

| Người phụ trách | Tổng giờ |
|---|---:|
| {owner} | {total_hours} |

## Người vượt ngưỡng

| Người phụ trách | Tổng giờ | Ngưỡng |
|---|---:|---:|
| {owner} | {total_hours} | {max_hours} |

{Nếu không có người vượt ngưỡng, ghi: Không có. Người có tổng giờ bằng ngưỡng không được xem là quá tải.}

## Dòng bị loại

| Dòng | task_id | Lý do |
|---:|---|---|
| {line} | {task_id hoặc null} | {liệt kê tất cả mã lý do và mô tả} |

{Nếu không có dòng bị loại, ghi: Không có.}

## Kiểm tra chất lượng dữ liệu

| Chỉ số | Giá trị |
|---|---:|
| Số dòng dữ liệu (không tính header) | {row_count} |
| Dòng thiếu owner | {missing_owner_count} |
| Dòng hours không hợp lệ | {invalid_hours_count} |
| Số task_id bị lặp (distinct) | {duplicate_id_count} |
| task_id bị lặp | {duplicate_ids} |

### Chi tiết issues

| Dòng | Cột | Loại | task_id | Mô tả |
|---:|---|---|---|---|
| {line} | {column} | {type} | {task_id} | {message} |

{Nếu không có issue, ghi: Không có.}

## Kết luận

{Tóm tắt tổng giờ và người quá tải theo JSON. Nêu rõ các dòng bị loại không được tính.}
