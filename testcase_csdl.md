# Nhật ký Kiểm thử & Thay đổi Cơ sở dữ liệu (testcase_csdl.md)

Tài liệu này ghi lại toàn bộ các thay đổi về cơ sở dữ liệu, tài khoản kiểm thử, các thao tác reset blockchain và các ca kiểm thử được thực hiện trong hệ thống.

---

## 📅 Nhật ký cập nhật

### [2026-07-06 20:58] Khởi tạo tệp nhật ký kiểm thử
* **Tác vụ**: Tạo tệp `testcase_csdl.md` để ghi nhận lịch sử thay đổi.
* **Trạng thái**: Đã hoàn thành.

### [2026-07-06 20:56] Chuyển đổi vai trò 10 tài khoản sang BUYER
* **Tác vụ**: Cập nhật vai trò của 10 tài khoản nông dân cũ vừa được khôi phục về trạng thái `BUYER` (Người mua).
* **Mục đích**: Để các tài khoản này phải thực hiện luồng đăng ký Nông trại mới từ đầu nhằm kiểm thử quy trình duyệt 2 bước.
* **SQL/Django Command**:
  ```python
  User.objects.filter(role='FARMER').update(role='BUYER')
  ```
* **Kết quả**: 10 tài khoản đã chuyển sang `BUYER` thành công.

### [2026-07-06 20:54] Khôi phục 10 tài khoản kiểm thử từ Backup
* **Tác vụ**: Trích xuất 10 tài khoản chủ trang trại cũ từ file `db.sqlite3.bak` và khôi phục vào cơ sở dữ liệu mới (không khôi phục sản phẩm và nông trại cũ).
* **Danh sách tài khoản**:
  1. `go_cafe_owner`
  2. `highlands_coffee_owner`
  3. `organica_owner`
  4. `koita_owner`
  5. `mua_owner`
  6. `sonlanga_owner`
  7. `health_paradise_owner`
  8. `coop_finest_owner`
  9. `vua_gao_owner`
  10. `cat_tuong_owner`
* **Kết quả**: Khôi phục thành công.

### [2026-07-06 20:49] Làm sạch toàn bộ dữ liệu & Tái tạo Smart Contract
* **Tác vụ**: Xóa sạch 100% dữ liệu cũ trên website và deploy lại Blockchain.
* **Thao tác**:
  1. Dọn sạch DB: `python3 manage.py flush --no-input`
  2. Triển khai lại Smart Contract: `npx hardhat run scripts/deploy.js --network localhost`
  3. Cập nhật địa chỉ Contract mới trong `blockchain.py`: `0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512`
  4. Khởi tạo lại các tài khoản kiểm thử mặc định: `admin`, `auditor`, `buyer`.
