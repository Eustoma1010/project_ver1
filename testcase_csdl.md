# Nhật ký Kiểm thử & Thay đổi Cơ sở dữ liệu (testcase_csdl.md)

Tài liệu này ghi lại toàn bộ các thay đổi về cơ sở dữ liệu, tài khoản kiểm thử, các thao tác reset blockchain và các ca kiểm thử được thực hiện trong hệ thống.
## 🏢 Cấu hình trường thông tin chuẩn doanh nghiệp (Enterprise Schema Configuration)

Nhằm đảm bảo tính chính xác và tuân thủ các chuẩn mực dữ liệu doanh nghiệp trong nước và quốc tế, các trường thông tin của mô hình `CustomUser` và `Farm` được cấu hình lại với các ràng buộc nghiệp vụ chặt chẽ dưới đây:

### 1. Mô hình Người dùng (`CustomUser`)
| Tên trường | Kiểu dữ liệu | Ràng buộc nghiệp vụ (Xác thực dữ liệu) | Ý nghĩa / Quy chuẩn |
| :--- | :--- | :--- | :--- |
| `username` | `CharField` | Tối thiểu 3 ký tự, chỉ gồm chữ cái và chữ số (`isalnum`). | Tên đăng nhập định danh duy nhất. |
| `phone_number`| `CharField` | Regex: `^0\d{9,10}$` (độ dài 10 hoặc 11 số, bắt đầu bằng `0`). | Số điện thoại di động/cá nhân hợp lệ tại Việt Nam. |
| `email` | `EmailField`| Định dạng email quốc tế tiêu chuẩn. | Địa chỉ email của cá nhân đăng ký tài khoản. |

### 2. Mô hình Nhà cung cấp / Nông trại (`Farm`)
| Tên trường | Kiểu dữ liệu | Ràng buộc nghiệp vụ (Xác thực dữ liệu) | Ý nghĩa / Quy chuẩn |
| :--- | :--- | :--- | :--- |
| `name` | `CharField` | Tối thiểu 3 ký tự. Bắt buộc nhập. | Tên pháp nhân / tên thương hiệu doanh nghiệp. |
| `tax_code` | `CharField` | Regex: `^\d{10}$|^\d{13}$|^\d{10}-\d{3}$` (10 số đối với DN chính, hoặc 13 số đối với chi nhánh/đơn vị trực thuộc). | Mã số thuế doanh nghiệp hợp pháp tại Việt Nam. |
| `phone` | `CharField` | Regex: `^0\d{9,10}$` (độ dài 10-11 số, bắt đầu bằng `0`). Bắt buộc nhập. | Số điện thoại hotline liên hệ chính thức của doanh nghiệp. |
| `email` | `EmailField`| Định dạng email doanh nghiệp. Bắt buộc nhập. | Hòm thư điện tử chính thức nhận thông tin giao dịch. |
| `business_license` | `FileField` | Bắt buộc đính kèm tệp tài liệu/hình ảnh khi đăng ký. | Giấy chứng nhận đăng ký kinh doanh/Giấy chứng nhận cơ sở đủ điều kiện ATVSTP. |

### 3. Các Mô hình Sản phẩm & Giao dịch (`Product`, `Batch`, `Order`, `OrderItem`)
| Mô hình (Model) | Tên trường (Field) | Ràng buộc nghiệp vụ (Xác thực dữ liệu) | Ý nghĩa / Quy chuẩn |
| :--- | :--- | :--- | :--- |
| `Product` | `price` | `MinValueValidator(1000)` (Tối thiểu 1.000đ). | Giá trị bán lẻ thực tế hợp lý tại thị trường Việt Nam. |
| `Batch` | `initial_quantity` | `MinValueValidator(1)` (Tối thiểu 1 đơn vị giống). | Số lượng giống gieo ban đầu của một lô sản xuất phải lớn hơn 0. |
| `Batch` | `remaining_quantity` | `MinValueValidator(0)` (Không được phép âm). | Số lượng tồn kho còn lại của lô hàng. |
| `Order` | `total_price` | `MinValueValidator(0)` (Không được phép âm). | Tổng giá trị đơn hàng thực tế. |
| `OrderItem` | `quantity` | `MinValueValidator(1)` (Tối thiểu mua 1 sản phẩm). | Số lượng đặt mua cho mỗi dòng sản phẩm. |
| `OrderItem` | `price` | `MinValueValidator(0)` (Không được phép âm). | Đơn giá sản phẩm tại thời điểm mua. |

---


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

---

## 🚀 Hướng dẫn Quy trình Kiểm thử Hệ thống (Testing Workflow)

Để kiểm tra toàn diện tất cả tính năng của hệ thống (Đăng ký Nông trại, Duyệt 2 bước, Đăng sản phẩm, Quản lý lô hàng, Ghi nhận Blockchain, Mua hàng FIFO, và Giao nhận hàng), chúng ta phân chia 10 tài khoản người dùng thành **4 Nhóm Kiểm thử (Test Cases)** cụ thể dưới đây.

---

### 🧪 CASE 1: Quy trình hoạt động chuẩn (Happy Path End-to-End)
* **Tài khoản sử dụng**: `go_cafe_owner` và `highlands_coffee_owner`
* **Mục tiêu**: Kiểm tra luồng chạy hoàn chỉnh không lỗi từ đăng ký đến giao hàng và ghi chuỗi khối thành công.

#### Các bước thực hiện:
1. **Bước 1: Nộp hồ sơ Nông trại**
   * Đăng nhập bằng `go_cafe_owner` (pass: `test123`).
   * Truy cập mục **Đăng ký nhà cung cấp** trên thanh Menu.
   * Nhập thông tin Nông trại (tên, mã số thuế, vùng miền, mô tả, tải file giấy phép KD...). Gửi hồ sơ.
   * *Kết quả mong đợi*: Màn hình hiển thị trạng thái "Chờ duyệt hồ sơ".
2. **Bước 2: Quản trị viên duyệt hồ sơ (Bước 1)**
   * Đăng nhập bằng `admin` (pass: `admin123`).
   * Truy cập trang **Quản trị (Duyệt sản phẩm & nhà cung cấp)** (`/admin/reports/`).
   * Click **Duyệt hồ sơ** cho nông trại của `go_cafe_owner`.
   * *Kết quả mong đợi*: Trạng thái nông trại chuyển sang "Chờ kiểm định thực địa".
3. **Bước 3: Kiểm định viên thẩm định thực địa (Bước 2)**
   * Đăng nhập bằng `auditor` (pass: `auditor123`).
   * Truy cập trang **Thẩm định viên (Auditor)**.
   * Ở mục "Thẩm định Nông trại Mới", click **Phê duyệt & cấp chứng chỉ**.
   * *Kết quả mong đợi*: Nông trại được chuyển sang trạng thái "HOẠT ĐỘNG". Vai trò của `go_cafe_owner` tự động nâng lên thành `FARMER`.
4. **Bước 4: Nông dân đăng bán sản phẩm mới**
   * Đăng nhập lại bằng `go_cafe_owner`.
   * Truy cập **Quản lý sản phẩm** -> Click **Thêm sản phẩm mới**.
   * Nhập thông tin sản phẩm (chọn danh mục, tên, giá, đơn vị, mô tả, ảnh). Gửi yêu cầu.
   * *Kết quả mong đợi*: Sản phẩm được tạo với trạng thái "Chờ thẩm định".
5. **Bước 5: Thẩm định viên duyệt sản phẩm**
   * Đăng nhập bằng `auditor`.
   * Tại mục "Thẩm định sản phẩm mới", tìm sản phẩm của `go_cafe_owner` và click **Duyệt**.
   * *Kết quả mong đợi*: Trạng thái sản phẩm thành "Đã duyệt". Sản phẩm xuất hiện trên trang chủ cửa hàng nhưng có nhãn "Hết hàng" (vì chưa có lô thu hoạch nào).
6. **Bước 6: Khởi tạo Lô canh tác & Ghi mốc lịch trình**
   * Đăng nhập bằng `go_cafe_owner`.
   * Truy cập **Quản lý lô hàng** -> Click **Tạo lô sản phẩm mới**.
   * Nhập mã lô, số lượng dự kiến, chọn sản phẩm.
   * Tiến hành thêm một cột mốc lịch trình mới (ví dụ: "Gieo hạt" hoặc "Bón phân") kèm các thông số kỹ thuật (pH đất, độ ẩm...).
   * *Kết quả mong đợi*: Lô hàng được tạo thành công, cột mốc hiển thị trạng thái "Chờ xác thực".
7. **Bước 7: Thẩm định viên xác thực cột mốc lên Blockchain**
   * Đăng nhập bằng `auditor`.
   * Tại mục "Xác thực cột mốc hành trình", nhập mã thanh tra (Inspection ID), ý kiến kiểm định và click **Phê duyệt**.
   * *Kết quả mong đợi*: Cột mốc chuyển sang trạng thái "Đã xác thực", tạo ra mã giao dịch Blockchain (`blockchain_tx_hash`).
8. **Bước 8: Thu hoạch & Mở bán sản phẩm**
   * Đăng nhập bằng `go_cafe_owner`.
   * Tạo một cột mốc đặc biệt với tiêu đề chính xác: `Thu hoạch & Đóng gói`. Nhập ngày thu hoạch, số lượng thực tế.
   * Đăng nhập bằng `auditor` -> tiến hành duyệt cột mốc `Thu hoạch & Đóng gói` này lên Blockchain.
   * *Kết quả mong đợi*: Lô hàng tự động chuyển sang trạng thái `HARVESTED` (Đã thu hoạch). Sản phẩm trên trang chủ tự động chuyển sang trạng thái "Còn hàng" và cập nhật số dư kho.
9. **Bước 9: Khách hàng đặt mua sản phẩm**
   * Đăng nhập bằng `buyer` (pass: `buyer123`).
   * Chọn sản phẩm của `go_cafe_owner` trên trang chủ, thêm vào giỏ hàng và tiến hành đặt hàng.
   * *Kết quả mong đợi*: Đơn hàng được tạo thành công ở trạng thái "Chờ xử lý".
10. **Bước 10: Nông dân duyệt đơn hàng & Giao hàng**
    * Đăng nhập bằng `go_cafe_owner`.
    * Tại Dashboard, click **Duyệt đơn hàng** cho sản phẩm vừa đặt.
    * *Kết quả mong đợi*: Trạng thái đơn hàng tự động chuyển sang "Đang giao" (Shipped) và gán đơn vị vận chuyển.
    * Click tiếp **Xác nhận giao hàng thành công** -> Hệ thống tự động ghi nhận biên lai giao nhận lên Blockchain.

---

### 🧪 CASE 2: Luồng Từ chối & Cập nhật lại (Rejection & Resubmission)
* **Tài khoản sử dụng**: `organica_owner` và `koita_owner`
* **Mục tiêu**: Kiểm tra hoạt động của các nút từ chối hồ sơ/sản phẩm và khả năng chỉnh sửa gửi lại của nhà cung cấp.

#### Các bước thực hiện:
1. **Từ chối đăng ký Nông trại ở Bước 1**:
   * Đăng nhập bằng `organica_owner`, gửi đơn đăng ký nông trại.
   * Đăng nhập bằng `admin`, click **Từ chối** hồ sơ.
   * *Kết quả mong đợi*: Nông trại chuyển sang trạng thái `REJECTED`. Khi `organica_owner` đăng nhập lại, họ sẽ thấy nút đăng ký mở lại để nộp đơn mới.
2. **Từ chối đăng ký Nông trại ở Bước 2**:
   * Đăng nhập bằng `koita_owner`, gửi đơn đăng ký nông trại. Admin duyệt hồ sơ bước 1.
   * Đăng nhập bằng `auditor`, click **Từ chối cấp chứng chỉ**.
   * *Kết quả mong đợi*: Trạng thái nông trại chuyển sang `REJECTED`. Nhà cung cấp có thể cập nhật lại thông tin để gửi duyệt lại.
3. **Từ chối duyệt sản phẩm**:
   * Nhà cung cấp (đã được duyệt) thêm sản phẩm mới.
   * Auditor click **Từ chối** duyệt sản phẩm đó.
   * *Kết quả mong đợi*: Sản phẩm có trạng thái `REJECTED`. Nhà cung cấp có thể chỉnh sửa lại sản phẩm này thông qua trang quản lý để gửi duyệt lại.
4. **Từ chối xác thực cột mốc**:
   * Nhà cung cấp thêm mốc lịch trình.
   * Auditor click **Từ chối** xác thực cột mốc đó.
   * *Kết quả mong đợi*: Cột mốc hiển thị nhãn màu đỏ "Từ chối" kèm ý kiến của Auditor. Mốc này **không** được ghi nhận lên Blockchain để bảo vệ tính trung thực của chuỗi cung ứng.

---

### 🧪 CASE 3: Thao tác hàng loạt & Bộ lọc liên kết (Bulk Actions & Dynamic Filters)
* **Tài khoản sử dụng**: `mua_owner`, `sonlanga_owner`, `health_paradise_owner`
* **Mục tiêu**: Kiểm tra các giao diện nâng cao, bộ lọc liên kết không lặp dữ liệu và các nút xử lý hàng loạt.

#### Các bước thực hiện:
1. **Kiểm tra bộ lọc liên kết (Cascading Dropdowns)**:
   * Cho cả 3 tài khoản đăng ký nông trại và sản phẩm thành công.
   * Truy cập trang `/admin/reports/` hoặc `/farm/auditor_dashboard/`.
   * *Thao tác*: Thay đổi lựa chọn tại dropdown Nông trại ở cột trái.
   * *Kết quả mong đợi*: Dropdown Danh mục/Sản phẩm ở cột bên phải tự động cập nhật và thu hẹp danh sách chỉ hiển thị các sản phẩm thuộc về nông trại đã chọn ở bên trái, sắp xếp gọn gàng trên cùng một hàng.
2. **Duyệt hàng loạt sản phẩm**:
   * Đăng nhập bằng `mua_owner` và `sonlanga_owner` gửi phê duyệt nhiều sản phẩm cùng lúc.
   * Đăng nhập bằng `auditor`, click nút **Duyệt tất cả sản phẩm** đang hiển thị theo bộ lọc hiện tại.
   * *Kết quả mong đợi*: Tất cả các sản phẩm được tích chọn tự động chuyển sang trạng thái "Đã duyệt" chỉ sau 1 click chuột.
3. **Duyệt hàng loạt cột mốc hành trình**:
   * Tạo nhiều mốc lịch trình chờ duyệt cho các lô hàng khác nhau.
   * Đăng nhập bằng `auditor`, click nút **Xác thực tất cả cột mốc** hiển thị theo bộ lọc.
   * *Kết quả mong đợi*: Hệ thống tự động xử lý hàng loạt các giao dịch ký gửi lên Blockchain, gán mã giao dịch tương ứng và hoàn tất quy trình nhanh chóng.

---

### 🧪 CASE 4: Đình chỉ hoạt động & Thu hồi quyền (Suspension Flow)
* **Tài khoản sử dụng**: `coop_finest_owner`, `vua_gao_owner`, `cat_tuong_owner`
* **Mục tiêu**: Đảm bảo hệ thống ngăn chặn hiệu quả các nhà cung cấp vi phạm chất lượng hoặc không đạt kiểm định định kỳ.

#### Các bước thực hiện:
1. **Bước 1: Đăng ký và hoạt động bình thường**
   * Cho các tài khoản trên tạo nông trại và đăng bán sản phẩm đã duyệt.
2. **Bước 2: Tiến hành kiểm tra định kỳ không đạt**
   * Đăng nhập bằng `auditor`.
   * Tại mục "Danh sách nhà cung cấp đang hoạt động", tìm nông trại của `coop_finest_owner`.
   * Click **Kiểm tra thực địa** -> Chọn kết quả **Không Đạt (Fail)** kèm ghi chú vi phạm.
   * *Kết quả mong đợi*: 
     * Nông trại tự động chuyển sang trạng thái "ĐÌNH CHỈ" (`SUSPENDED`).
     * Tất cả các sản phẩm của nông trại này trên trang chủ lập tức bị ẩn hoặc vô hiệu hóa nút mua hàng.
3. **Bước 3: Kiểm tra quyền hạn khi bị đình chỉ**
   * Đăng nhập bằng `coop_finest_owner`.
   * *Kết quả mong đợi*: Hệ thống hiển thị thông báo tài khoản đang bị đình chỉ hoạt động. Nông dân bị chặn quyền cập nhật cài đặt, không thể tạo lô hàng mới hay thêm cột mốc mới.

