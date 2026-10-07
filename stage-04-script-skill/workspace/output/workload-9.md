# Báo cáo kiểm tra CSV: `data/workload.csv`

- **Ngưỡng tối đa:** 9.0 giờ
- **Công cụ:** `skills/csv-quality/scripts/check_csv.py`
- **Mã thoát:** 0

## Tổng giờ theo người

| Người phụ trách | Tổng giờ |
|---|---:|
| Lan | 9.0 |
| Minh | 3.0 |

## Người vượt ngreshold

| Người phụ trách | Tổng giờ | Ngưỡng |
|---|---:|---:|
| Không có | | |

Không có. Người có tổng giờ bằng ngưỡng không được xem là quá tải.

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

- Tổng giờ hợp lệ: Lan 9.0 giờ, Minh 3.0 giờ.
- Không có người nào vượt quá 9 giờ (Lan đúng 9 giờ, không tính quá tải).
- Dòng 5 (T04) bị loại do `hours = "abc"` không phải số.
- Dòng 6 (T02) bị loại do task_id trùng với dòng 3.
- Dòng 7 (T05) bị loại do owner trống.