---
name: csv-quality
description: Kiểm tra chất lượng CSV công việc và tính tổng giờ theo owner với ngưỡng do người dùng cung cấp, sau đó ghi báo cáo Markdown dưới output/. Dùng khi người dùng yêu cầu rà soát CSV, tổng giờ hoặc xác định người quá tải.
---

# Kiểm tra chất lượng CSV và quá tải theo người

Dùng script để phân tích CSV; không tự tính số liệu bằng mắt và không sửa file đầu vào.

## Xác định ngưỡng

- Nếu người dùng yêu cầu xác định người quá tải nhưng chưa cung cấp ngưỡng giờ, hỏi ngưỡng trước khi chạy script hoặc kết luận.
- Chỉ dùng ngưỡng được cung cấp trong yêu cầu hiện tại. Không lấy ngưỡng từ cuộc trò chuyện cũ.
- Truyền đúng giá trị vào tham số bắt buộc `--max-hours`. Script chỉ nhận số hữu hạn không âm.

## Chạy script

Dùng tool `bash` (working directory là workspace):

```bash
python skills/csv-quality/scripts/check_csv.py --input <đường dẫn CSV> --max-hours <ngưỡng>
```

Ví dụ:

```bash
python skills/csv-quality/scripts/check_csv.py --input data/workload.csv --max-hours 8
```

## Đọc kết quả

- Exit code `0`: phân tích thành công. Đọc JSON từ stdout. Các trường chất lượng hiện có là `row_count`, `missing_owner_count`, `invalid_hours_count`, `duplicate_id_count`, `duplicate_ids`, `issues`.
- `max_hours`: ngưỡng đã dùng.
- `hours_by_owner`: tổng giờ của mỗi owner, chỉ tính các dòng hợp lệ.
- `overloaded_owners`: owner có tổng giờ **lớn hơn** ngưỡng; tổng bằng ngưỡng không phải quá tải.
- `excluded_rows`: các dòng không được cộng, gồm số dòng CSV, `task_id` (hoặc `null`) và mọi mã lý do áp dụng. Dòng trống được bỏ qua.
- Mỗi `task_id` không rỗng chỉ được tính lần xuất hiện đầu tiên. Nếu lần đầu không hợp lệ, lần sau vẫn bị loại là ID trùng.
- Exit code khác `0`: lỗi tham số hoặc lỗi thực thi (ví dụ file không tồn tại, thiếu cột bắt buộc, CSV lỗi). Đọc stderr, báo lỗi và không đưa ra tổng giờ hay báo cáo như thể đã phân tích thành công.
- Nếu tool trả `timed_out: true` hoặc `ok: false`, báo lỗi và không suy đoán kết quả.

## Viết báo cáo

1. Đọc `references/report-template.md` trong thư mục skill này: `skills/csv-quality/references/report-template.md`.
2. Dùng JSON của lần chạy hiện tại làm nguồn cho ngưỡng, tổng giờ, người quá tải, thống kê chất lượng và các dòng bị loại.
3. Nêu rõ từng dòng bị loại và tất cả lý do của dòng đó. Phân biệt lỗi dữ liệu được báo trong JSON với lỗi thực thi khiến script không phân tích được.
4. Ghi báo cáo bằng `write_file` vào đường dẫn người dùng yêu cầu (mặc định `output/workload.md`), rồi trả đường dẫn và tóm tắt ngắn.
