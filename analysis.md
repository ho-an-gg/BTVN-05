# Block 1: Tra cứu chính sách đúng phiên bản

## Kết quả kiểm tra

### Đổi tên file rồi chạy lại A và B

Khi chạy các trường hợp này, policy được đổi tên; nội dung không đổi. Sau khi kiểm tra, tên gốc được khôi phục.

- **A:** Agent vẫn chọn policy cũ, 8 ngày, không đủ điều kiện; dẫn `data/policies/version-one.md`.
- **Trace:** [stage-02-skills/traces/20261007-180826_494a997a_turn01_15e8fd56.jsonl](stage-02-skills/traces/20261007-180826_494a997a_turn01_15e8fd56.jsonl)
  - `messages[3]`: Assistant gọi `list_files({"path": "data/policies"})`.
  - `messages[4]`: Tool trả về hai tên file mới: `policy-before-10.md` và `policy-from-10.md`.
  - `messages[5]`: Assistant gọi `read_file` trên các tên file mới vừa nhận được.
  - `messages[10]`: Kết luận không đổi (**không đủ điều kiện**, 8 ngày); căn cứ được cập nhật thành `data/policies/policy-before-10.md`.

- **B:** Mua 02/10/2026, yêu cầu 12/10/2026; agent chọn policy mới, tính 10 ngày trong giới hạn 14 ngày, đủ điều kiện và không thu phí; dẫn `data/policies/version-two.md`.
- **Trace:** [stage-02-skills/traces/20261007-180918_14f2face_turn01_ad37388b.jsonl](stage-02-skills/traces/20261007-180918_14f2face_turn01_ad37388b.jsonl)
  - `messages[3]`: Assistant gọi `list_files({"path": "data/policies"})`.
  - `messages[5]`: Assistant đọc hai file mới `policy-before-10.md` và `policy-from-10.md`.
  - `messages[10]`: Kết luận không đổi (**đủ điều kiện**, 10 ngày, không thu phí); căn cứ là `data/policies/policy-from-10.md`.

### Thiếu trạng thái kích hoạt

- **Input:** “Tôi mua ngày 02/10/2026, muốn hoàn ngày 12/10/2026.”
- **Kết quả:** Agent hỏi sản phẩm đã kích hoạt hay chưa, chưa đưa ra kết luận.
- **Trace:** [stage-02-skills/traces/20261007-181104_1de82591_turn01_0be8663f.jsonl](stage-02-skills/traces/20261007-181104_1de82591_turn01_0be8663f.jsonl)
  - `messages[1]`: Assistant đọc `skills/refund-policy/SKILL.md`.
  - `messages[3]`: Sau khi đọc bước 1 trong `SKILL.md`, Assistant nhận diện còn thiếu trạng thái kích hoạt.
  - **Hành vi quan sát:** Assistant không gọi tool tra cứu chính sách, không tự giả định sản phẩm chưa kích hoạt và hỏi lại người dùng:

    > Tôi cần thêm thông tin để tra cứu chính sách hoàn tiền cho bạn. Bạn vui lòng cho biết trạng thái kích hoạt/sử dụng sản phẩm: sản phẩm đã được kích hoạt hay chưa?

- **Câu trả lời vòng 2 của người dùng:** “rồi” (đã kích hoạt).
- **Diễn biến vòng 2:**
  - `messages[5]`: Lúc này đã đủ 3 điều kiện, Assistant mới bắt đầu gọi `list_files({"path": "data/policies"})`.
  - `messages[7]`: Đọc nội dung 2 file chính sách.
  - `messages[10]`: Đọc file `answer-template.md`.
  - `messages[12]`: Kết luận: **KHÔNG ĐỦ ĐIỀU KIỆN** hoàn tiền, vì điều khoản trong `policy-from-oct.md` ghi rõ *"Không hoàn tiền nếu sản phẩm đã kích hoạt"*.

## Kiểm tra tool trực tiếp

Gọi `list_files` trực tiếp trong cả stage 01 và stage 02:

| Đầu vào | Kết quả |
| --- | --- |
| `data/policies/` | Trả danh sách các policy trong thư mục. |
| Đường dẫn file | Báo lỗi vì đường dẫn không phải thư mục. |
| Đường dẫn không tồn tại | Báo lỗi rõ ràng. |
| Đường dẫn vượt workspace | Báo lỗi, không liệt kê nội dung bên ngoài workspace. |

## Câu hỏi cuối bài

Tool `list_files` giúp agent tìm tài liệu trong workspace kể cả khi tên file thay đổi. Skill `refund-policy` hướng dẫn agent chọn chính sách theo ngày mua, kiểm tra thông tin cần thiết và trình bày căn cứ. Chỉ sửa prompt không giải quyết được yêu cầu đổi tên file vì agent vẫn thiếu khả năng tìm file trong workspace.

---

# Block 2: Kiểm tra quá tải theo người

## Stage 03: Tính tổng giờ qua Bash

Đã chạy yêu cầu tính tổng `hours` theo `owner` trong `data/workload.csv`, không sửa file đầu vào.

- `T04`: loại khỏi phép tính vì `hours` có giá trị `abc`, không chuyển được thành số.
- `T05`: loại khỏi phép tính vì thiếu `owner`.
- `T02`: được phát hiện trùng, nhưng đoạn lệnh chạy đã cộng cả hai dòng thay vì loại dòng trùng.
- Tổng thu được: Lan **14 giờ**, Minh **3 giờ**. Lan có 14 giờ do `T02` (5 giờ) bị cộng hai lần.

**Trace hoàn tất:** [stage-03-bash/traces/20261007-225640_fe419e77_turn01_0f3309a6.jsonl](stage-03-bash/traces/20261007-225640_fe419e77_turn01_0f3309a6.jsonl)

- `messages[4–5]`: đọc `data/workload.csv` thành công.
- `messages[8–9]`: Bash chạy thành công (`exit_code: 0`), ghi nhận lỗi của `T04`, thiếu owner của `T05`, phát hiện `T02` trùng và in tổng Lan 14, Minh 3.
- `messages[12]`: lượt chạy hoàn tất.

## Stage 04: Script skill

### Trace hiện có trước khi mở rộng script

Trace duy nhất đang có là lần kiểm tra chất lượng `data/tasks.csv` ngày 06/10, trước khi thêm `--max-hours`. Script cũ chạy thành công với exit code 0 và trả về 6 dòng dữ liệu, 1 dòng thiếu owner, 1 dòng hours không hợp lệ, 1 ID trùng (`T02`). Các issues nằm ở line 4 (`T03` thiếu owner), line 5 (`T04`, hours=`abc`) và line 6 (`T02` trùng với line 3). Agent đã ghi báo cáo vào `output/csv-quality.md`.

**Trace:** [stage-04-script-skill/traces/20261007-000957_5251f93e_turn01_f86764bb.jsonl](stage-04-script-skill/traces/20261007-000957_5251f93e_turn01_f86764bb.jsonl)

### Kết quả phiên bản có `--max-hours`

#### Chạy trực tiếp với ngưỡng 8

Lệnh `check_csv.py --input workspace/data/workload.csv --max-hours 8` chạy thành công. JSON cho biết 6 dòng dữ liệu, `wrong_field_count: 0`, 1 dòng thiếu owner, 1 dòng hours không hợp lệ và 1 ID trùng (`T02`). Tổng hợp: Lan **9 giờ**, Minh **3 giờ**; Lan vượt ngưỡng. Các dòng bị loại: line 5 (`T04`, `invalid_hours`), line 6 (`T02`, `duplicate_id`) và line 7 (`T05`, `missing_owner`).

#### Chạy trực tiếp với ngưỡng 9

Lệnh `check_csv.py --input workspace/data/workload.csv --max-hours 9` cũng chạy thành công. Thống kê chất lượng, tổng giờ và các dòng bị loại giống ngưỡng 8; `overloaded_owners` rỗng vì Lan có đúng 9 giờ, bằng ngưỡng nên không được tính là quá tải.

#### Agent chạy với ngưỡng 8 và tạo báo cáo

Agent đọc `skills/csv-quality/SKILL.md`, chạy script với `--max-hours 8`, đọc reference và ghi báo cáo `stage-04-script-skill/workspace/output/workload-8.md`. Báo cáo nêu Lan 9 giờ quá tải, Minh 3 giờ không quá tải và liệt kê đúng ba dòng bị loại cùng lý do.

**Trace lệnh terminal và JSON ngưỡng 8/9 được gửi trong chat:** [stage-04-script-skill/traces/20261007-231513_acb3566c_turn01_e7da933d.jsonl](stage-04-script-skill/traces/20261007-231513_acb3566c_turn01_e7da933d.jsonl)

**Trace agent ngưỡng 8:** [stage-04-script-skill/traces/20261007-231549_e70de388_turn01_9ebce22e.jsonl](stage-04-script-skill/traces/20261007-231549_e70de388_turn01_9ebce22e.jsonl). Các sự kiện chính: `sequence 4–5` đọc skill; `sequence 8, 11` chạy script thành công với exit code 0; `sequence 9–10` đọc reference; `sequence 14–15` ghi báo cáo; `sequence 18` lượt hoàn tất.

#### Agent chạy với ngưỡng 9 và tạo báo cáo

Agent đọc skill, chạy script với `--max-hours 9`, đọc reference và ghi `stage-04-script-skill/workspace/output/workload-9.md`. Kết quả: Lan 9 giờ, Minh 3 giờ, không ai vượt ngưỡng vì Lan bằng đúng ngưỡng. Ba dòng bị loại và thống kê chất lượng trùng với lượt ngưỡng 8. Báo cáo phản ánh kết quả đúng; trong tiêu đề bảng có lỗi gõ “vượt ngưỡng” thành “vượt ngthreshold”.

**Trace agent ngưỡng 9:** [stage-04-script-skill/traces/20261007-232032_8a2a182b_turn01_c8e827da.jsonl](stage-04-script-skill/traces/20261007-232032_8a2a182b_turn01_c8e827da.jsonl). Các sự kiện chính: `sequence 4–5` đọc skill; `sequence 8, 11` chạy script thành công với exit code 0; `sequence 9–10` đọc reference; `sequence 14–15` ghi báo cáo; `sequence 18` lượt hoàn tất.

Hai kết quả JSON ngưỡng 8/9 được gửi trực tiếp vào chat là kết quả terminal. Trace agent ngưỡng 8 và 9 riêng biệt ghi nhận agent cũng chạy đúng từng ngưỡng và tạo hai báo cáo.

#### Yêu cầu thiếu ngưỡng

Trong cuộc trò chuyện mới, người dùng yêu cầu tính tổng giờ và xác định người quá tải nhưng không cung cấp ngưỡng. Agent đọc `skills/csv-quality/SKILL.md`, sau đó hỏi lại ngưỡng và kết thúc lượt; không chạy Bash, không kết luận quá tải và không tạo báo cáo. Hành vi này đúng yêu cầu skill.

**Trace:** [stage-04-script-skill/traces/20261007-232240_8f58269d_turn01_738dbf82.jsonl](stage-04-script-skill/traces/20261007-232240_8f58269d_turn01_738dbf82.jsonl). `sequence 4–5` đọc skill; lượt hoàn tất ở `sequence 8` mà không có tool call Bash.

#### File không tồn tại

Người dùng yêu cầu kiểm tra `data/khong-co.csv` với ngưỡng 8. Agent đọc skill rồi chạy script; lệnh kết thúc với exit code 1, stdout rỗng và stderr báo `Không đọc được file data/khong-co.csv: No such file or directory`. Agent dùng Bash liệt kê/tìm CSV để xác nhận file không tồn tại, sau đó hoàn tất lượt mà không tạo báo cáo giả hoặc đưa ra thống kê cho file này.

**Trace:** [stage-04-script-skill/traces/20261007-232516_9525681a_turn01_6f631f75.jsonl](stage-04-script-skill/traces/20261007-232516_9525681a_turn01_6f631f75.jsonl). `sequence 4–5` đọc skill; `sequence 8–9` chạy script và nhận lỗi; `sequence 12–17` kiểm tra các file CSV hiện có; lượt hoàn tất ở `sequence 20`.

#### Edge case: ID đầu tiên có `hours` không hợp lệ

Chạy trực tiếp `check_csv.py --input workspace/data/workload-edge.csv --max-hours 0`. Script phân tích thành công với 3 dòng dữ liệu và `wrong_field_count: 0`. Dòng 2 (`E01`, `hours=abc`) bị loại vì `invalid_hours`; lần xuất hiện tiếp theo của `E01` ở dòng 3 bị loại vì `duplicate_id`, tham chiếu lần đầu tại dòng 2. Chỉ `Minh` được tính với tổng 0 giờ; `overloaded_owners` rỗng ở ngưỡng 0. Kết quả xác nhận script giữ lần xuất hiện đầu tiên của ID kể cả khi dòng đó không hợp lệ.

Agent cũng chạy edge case với ngưỡng 0, đọc reference và tạo báo cáo `stage-04-script-skill/workspace/output/workload-edge.md`. Báo cáo nêu Minh 0 giờ, không có người quá tải, line 2 bị loại vì `invalid_hours`, line 3 vì `duplicate_id`.

- **Kết quả JSON trực tiếp:** do người dùng cung cấp từ lần chạy terminal.
- **Trace agent:** [stage-04-script-skill/traces/20261007-233111_9d4d5f92_turn01_975a9301.jsonl](stage-04-script-skill/traces/20261007-233111_9d4d5f92_turn01_975a9301.jsonl). `sequence 4–5` đọc skill; `sequence 8, 11` chạy script thành công với exit code 0; `sequence 9–10` đọc reference; `sequence 14–15` ghi báo cáo; `sequence 18` lượt hoàn tất.

## Tổng kết thay đổi và đối chiếu yêu cầu nộp bài

- Đã mở rộng `workspace/skills/csv-quality/scripts/check_csv.py` với `--max-hours`, tổng giờ theo owner, danh sách quá tải và `excluded_rows`, đồng thời giữ thống kê chất lượng hiện có.
- Đã cập nhật `workspace/skills/csv-quality/SKILL.md` để hỏi ngưỡng khi thiếu, chỉ dùng ngưỡng ở yêu cầu hiện tại và truyền giá trị qua CLI.
- Đã cập nhật `workspace/skills/csv-quality/references/report-template.md` để trình bày ngưỡng, tổng giờ, người quá tải, các dòng bị loại và thông tin chất lượng.
- Đã có `data/workload.csv`, `data/workload-edge.csv`, JSON trực tiếp với ngưỡng 8/9 và 0, báo cáo agent cho ngưỡng 8/9 và edge case, cùng trace cho ngưỡng 8/9, thiếu ngưỡng, file không tồn tại và edge case.
- Đã thêm kiểm thử tự động riêng `stage-04-script-skill/tests/test_workload_edge_case.py::test_first_invalid_task_id_occurrence_still_marks_id_as_seen`. Kiểm thử tạo CSV tạm và kiểm tra ID lần đầu có giờ sai vẫn làm lần xuất hiện sau bị loại là `duplicate_id`. Đã chạy `uv run pytest tests/test_workload_edge_case.py`: pytest thu thập 1 test và test đạt (`1 passed`).
- Đã đồng bộ `SKILL.md`, `references/report-template.md` và `scripts/check_csv.py` từ `workspace/skills/csv-quality/` sang `fixtures/skills/csv-quality/`; đã đối chiếu và ba cặp file giống nhau.
- Đã chạy kiểm thử tự động mới và xác nhận test đạt. Không có mục kiểm thử edge case nào còn chờ kết quả trong phần này.


## Câu hỏi cuối bài

Script chịu trách nhiệm đọc và kiểm tra CSV, áp dụng quy tắc ID trùng/lọc dòng, tính tổng giờ và so sánh với ngưỡng; nó xuất JSON xác định để các kết quả có thể kiểm tra lại. Model đọc skill, truyền đúng ngưỡng và đường dẫn, xử lý lỗi tool, rồi diễn giải JSON thành báo cáo theo reference. Nếu script được sửa nhưng skill không cập nhật, agent có thể không truyền `--max-hours`, dùng ngưỡng cũ hoặc hiểu sai các trường JSON. Nếu reference không cập nhật, báo cáo có thể bỏ sót ngưỡng, tổng giờ, người quá tải hoặc các dòng bị loại cùng lý do.
