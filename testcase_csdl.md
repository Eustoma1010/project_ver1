# Nhật ký Kiểm thử & Thay đổi Cơ sở dữ liệu (testcase_csdl.md)

Tài liệu này ghi lại toàn bộ các thay đổi về cơ sở dữ liệu, tài khoản kiểm thử, các thao tác reset blockchain và các ca kiểm thử được thực hiện trong hệ thống.
## 🔑 Danh sách Tài khoản & Mật khẩu Kiểm thử

Dưới đây là danh sách các tài khoản kiểm thử đã được thiết lập sẵn trong hệ thống với cơ sở dữ liệu sạch:

### 1. Tài khoản Hệ thống mặc định
| Vai trò | Tên đăng nhập (Username) | Mật khẩu (Password) | Mô tả |
| :--- | :--- | :--- | :--- |
| **Quản trị viên** | `admin` | `admin123` | Có quyền duyệt hồ sơ Nông trại bước 1, xem báo cáo tổng thể. |
| **Kiểm định viên** | `auditor` | `auditor123` | Có quyền kiểm định Nông trại thực địa (bước 2), thẩm định sản phẩm và xác thực Milestone ghi lên Blockchain. |
| **Người mua mặc định** | `buyer` | `buyer123` | Tài khoản khách hàng thông thường để mua sắm và theo dõi hành trình. |

### 2. 10 Tài khoản Nhà cung cấp (được khôi phục từ Backup, vai trò hiện tại: `BUYER`)
*Các tài khoản này được đặt mật khẩu mặc định là `test123`. Họ có vai trò khởi đầu là `BUYER` để có thể tiến hành nộp đơn đăng ký nhà cung cấp/nông trại.*

| STT | Tên đăng nhập (Username) | Mật khẩu (Password) | Vai trò hiện tại |
| :--- | :--- | :--- | :--- |
| 1 | `go_cafe_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 2 | `highlands_coffee_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 3 | `organica_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 4 | `koita_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 5 | `mua_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 6 | `sonlanga_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 7 | `health_paradise_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 8 | `coop_finest_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 9 | `vua_gao_owner` | `test123` | BUYER (Chờ đăng ký lại) |
| 10 | `cat_tuong_owner` | `test123` | BUYER (Chờ đăng ký lại) |

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
