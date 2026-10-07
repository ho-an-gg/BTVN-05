---
name: refund-policy
description: Tra cứu tài liệu chính sách hoàn tiền và đánh giá yêu cầu hoàn tiền theo ngày mua, ngày yêu cầu hoàn và trạng thái kích hoạt sản phẩm. Dùng khi người dùng hỏi về điều kiện hoặc phí hoàn tiền.
---

# Tra cứu chính sách hoàn tiền

## Các bước

1. Kiểm tra đủ ngày mua, ngày yêu cầu hoàn và trạng thái kích hoạt sản phẩm chưa. Nếu thiếu bất kỳ thông tin nào, hỏi lại trước khi kết luận; không tự giả định trạng thái kích hoạt.
2. Dùng `list_files` liệt kê `data/policies/` để tìm tài liệu chính sách. Không dựa vào tên file cố định.
3. Dùng `read_file` đọc tài liệu chính sách tìm được. Có thể đọc các file trong thư mục để xác định phạm vi ngày hiệu lực; không suy ra nội dung từ tên file.
4. Chọn chính sách dựa trên ngày mua và phạm vi hiệu lực ghi trong tài liệu. Ngày mua 2026-10-01 thuộc chính sách bắt đầu từ ngày này.
5. Tính số ngày lịch đã qua giữa ngày mua và ngày yêu cầu hoàn. Bằng đúng giới hạn ngày vẫn đủ điều kiện về thời gian.
6. Nếu sản phẩm đã kích hoạt, yêu cầu không đủ điều kiện. Nếu chưa kích hoạt, đối chiếu số ngày với giới hạn trong chính sách đã chọn. Chỉ nêu phí khi đủ điều kiện.
7. Làm theo định dạng trong `references/answer-template.md` và dẫn đường dẫn tài liệu đã đọc làm căn cứ. Nếu không tìm thấy hoặc không đọc được tài liệu, báo rõ lỗi thay vì đoán.
