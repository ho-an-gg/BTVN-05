# Báo cáo kiểm tra CSV: `data/workload-edge.csv`

- **Ngưỡng tối đa:** 0.0 giờ
- **Công cụ:** `skills/csv-quality/scripts/check_csv.py`
- **Mã thoát:** 0

## Tổng giờ theo người

| Người phụ trách | Tổng giờ |
|---|---:|
| Minh | 0.0 |

## Người vượt ngưỡng

Không có. Người có tổng giờ bằng ngưỡng không được xem là quá tải.

## Dòng bị loại

| Dòng | task_id | Lý do |
|---:|---|---|
| 2 | E01 | invalid_hours |
| 3 | E01 | duplicate_id |

## Kiểm tra chất lượng dữ liệu

| Chỉ số | Giá trị |
|---|---:|
| Số dòng dữ liệu (không tính header) | 3 |
| Dòng thiếu owner | 0 |
| Dòng hours không hợp lệ | 1 |
| Số task_id bị lặp (distinct) | 1 |
| task_id bị lặp | E01 |

### Chi tiết issues

| Dòng | Cột | Loại | task_id | Mô tả |
|---:|---|---|---|---|
| 2 | hours | invalid_hours | E01 | hours 'abc' không phải số hữu hạn không âm. |
| 3 | task_id | duplicate_id | E01 | task_id E01 đã xuất hiện ở line 2. |

## Kết luận

File `data/workload-edge.csv` có 3 dòng dữ liệu. Chỉ có 1 dòng hợp lệ (line 1, owner "Minh", 0 giờ). Dòng 2 bị loại vì `hours = "abc"` không phải số. Dòng 3 bị loại vì `task_id = "E01"` trùng lặp với dòng 2. Tổng giờ hợp lệ của "Minh" là 0.0 giờ, không vượt ngưỡng 0.0 giờ.