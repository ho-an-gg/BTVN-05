# Báo cáo kiểm tra CSV: `data/workload.csv`

- **Ngưỡng tối đa:** 8.0 giờ
- **Công cụ:** `skills/csv-quality/scripts/check_csv.py`
- **Mã thoát:** 0

## Tổng giờ theo người

| Người phụ trách | Tổng giờ |
|---|---:|
| Lan | 9.0 |
| Minh | 3.0 |

## Người vượt ngưỡng

| Người phụ trách | Tổng giờ | Ngưỡng |
|---|---:|---:|
| Lan | 9.0 | 8.0 |

## Dòng bị loại

| Dòng | task_id | Lý do |
|---:|---|---|
| 5 | T04 | invalid_hours |
| 6 | T02 | duplicate_id |
| 7 | T05 | missing_owner |

## Kiểm tra chất lượng dữ liệu

| Chỉ số | Giá trị |
|---|---:|
| Số dòng dữ liệu (không tính header) | 6 |
| Dòng thiếu owner | 1 |
| Dòng hours không hợp lệ | 1 |
| Số task_id bị lặp (distinct) | 1 |
| task_id bị lặp | T02 |

### Chi tiết issues

| Dòng | Cột | Loại | task_id | Mô tả |
|---:|---|---|---|---|
| 5 | hours | invalid_hours | T04 | hours 'abc' không phải số hữu hạn không âm. |
| 6 | task_id | duplicate_id | T02 | task_id T02 đã xuất hiện ở line 3. |
| 7 | owner | missing_owner | T05 | owner trống. |

## Kết luận

- Tổng số dòng hợp lệ được tính: 3/6 (3 dòng bị loại).
- **Lan** vượt ngưỡng 8 giờ với tổng **9.0 giờ** → quá tải.
- **Minh** ở mức 3.0 giờ, không quá tải.
- Dòng 5 (T04) bị loại do `hours = "abc"` không phải số.
- Dòng 6 (T02) bị loại do task_id trùng lặp với dòng 3.
- Dòng 7 (T05) bị loại do thiếu `owner`.