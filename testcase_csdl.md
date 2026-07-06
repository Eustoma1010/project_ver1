# Nhật ký Kiểm thử & Thay đổi Cơ sở dữ liệu (testcase_csdl.md)

Tài liệu này ghi lại toàn bộ các thay đổi về cơ sở dữ liệu, tài khoản kiểm thử, các thao tác reset blockchain và các ca kiểm thử được thực hiện trong hệ thống.

## 🔑 Danh sách Tài khoản & Dữ liệu Kiểm thử (Chuẩn Doanh nghiệp)

### 1. Tài khoản Hệ thống mặc định

| Trường | `admin` | `auditor` | `buyer` |
| :--- | :--- | :--- | :--- |
| **Mật khẩu** | `admin123` | `auditor123` | `buyer123` |
| **Vai trò** | ADMIN | AUDITOR | BUYER |
| **Họ** | Hệ Thống | Trần | Nguyễn |
| **Tên** | Quản Trị | Minh Tuấn | Thu Hà |
| **Email** | admin@verdant.com | auditor@verdant.com | buyer@verdant.com |
| **Số điện thoại** | 0901000001 | 0901000002 | 0901000003 |
| **Địa chỉ** | Trụ sở Verdant Traceability, 123 Nguyễn Huệ, Q.1, TP.HCM | Chi cục QLCL Nông Lâm sản, 135 Pasteur, Q.3, TP.HCM | 456 Lê Văn Sỹ, Q. Phú Nhuận, TP.HCM |

### 2. 10 Tài khoản Nhà cung cấp (vai trò hiện tại: `BUYER`, mật khẩu: `test123`)

| STT | Username | Họ và Tên | Email | Số điện thoại | Địa chỉ |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `go_cafe_owner` | Phạm Minh Đức | contact@gocafe.vn | 0902888123 | 142 Lê Hồng Phong, TP. Buôn Ma Thuột, Đắk Lắk |
| 2 | `highlands_coffee_owner` | Nguyễn Thái Bình | contact@highlandscoffee.com.vn | 0903777456 | 135/1 Nguyễn Chí Thanh, Quận 5, TP. HCM |
| 3 | `organica_owner` | Lê Thị Hoài An | info@organica.vn | 0914223344 | 54 Phạm Ngọc Thạch, Quận 3, TP. HCM |
| 4 | `koita_owner` | Francesco Rossi | import@koita.it | 0909123456 | 12 Thảo Điền, Quận 2, TP. HCM |
| 5 | `mua_owner` | Trần Thanh Mùa | nongsan@muaorganics.com | 0989555666 | Khe Sanh, Phường 10, TP. Đà Lạt, Lâm Đồng |
| 6 | `sonlanga_owner` | Ksor H'Yên | contact@sonlanga.com | 0905123987 | 45 Lê Duẩn, TP. Pleiku, Gia Lai |
| 7 | `health_paradise_owner` | Tan Kah Kee | support@healthparadise.com.my | 0908888999 | Lầu 5, Pearl Plaza, Bình Thạnh, TP. HCM |
| 8 | `coop_finest_owner` | Nguyễn Văn Hùng | chamsockhachhang@coopfinest.vn | 0913999888 | 199-205 Nguyễn Thái Học, Quận 1, TP. HCM |
| 9 | `vua_gao_owner` | Võ Quốc Việt | info@vuagaoviet.com | 0918111222 | Lô A1, KCN Tân Đô, Đức Hòa, Long An |
| 10 | `cat_tuong_owner` | Nguyễn Cát Tường | traicay@cattuongfruit.com | 0903112233 | Ấp Mỹ Lợi, Mỹ Phong, TP. Mỹ Tho, Tiền Giang |

> [!IMPORTANT]
> Vai trò hiện tại của 10 owner đã được nâng lên `FARMER` theo đúng luồng hệ thống (Admin duyệt → role = FARMER).

### 3. 10 Nhà cung cấp (Farm) — Dữ liệu khôi phục từ Backup

| STT | Tên NCC | Owner | Khu vực | Tỉnh/TP | Mã số thuế | SĐT liên hệ | Email | Trạng thái |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | Gờ Cafe | `go_cafe_owner` | Miền Trung | Đắk Lắk | 6001234567 | 02623852147 | contact@gocafe.vn | APPROVED |
| 2 | Highlands Coffee | `highlands_coffee_owner` | Miền Trung | Lâm Đồng | 0311234568 | 19001755 | contact@highlandscoffee.com.vn | APPROVED |
| 3 | Organica | `organica_owner` | Miền Trung | Lâm Đồng | 0312345678 | 02838234567 | info@organica.vn | APPROVED |
| 4 | Koita | `koita_owner` | Miền Nam | TP. HCM | 0313456789 | 02862812345 | import@koita.it | APPROVED |
| 5 | Mùa | `mua_owner` | Miền Trung | Lâm Đồng | 5801234987 | 02633811223 | nongsan@muaorganics.com | APPROVED |
| 6 | SonlanGa | `sonlanga_owner` | Miền Trung | Gia Lai | 5900987654 | 02693822456 | contact@sonlanga.com | APPROVED |
| 7 | Health Paradise | `health_paradise_owner` | Miền Nam | TP. HCM | 0314567890 | 02835123456 | support@healthparadise.com.my | APPROVED |
| 8 | Co.op Finest | `coop_finest_owner` | Miền Nam | TP. HCM | 0300234567 | 1900555568 | chamsockhachhang@coopfinest.vn | APPROVED |
| 9 | Vua Gạo | `vua_gao_owner` | Miền Nam | Long An | 1101823456 | 18008012 | info@vuagaoviet.com | APPROVED |
| 10 | Cát Tường | `cat_tuong_owner` | Miền Nam | Tiền Giang | 1201234567 | 02733855667 | traicay@cattuongfruit.com | APPROVED |

#### Giới thiệu doanh nghiệp (Description)

| STT | Tên NCC | Mô tả doanh nghiệp |
| :---: | :--- | :--- |
| 1 | **Gờ Cafe** | Thương hiệu cà phê đặc sản Buôn Ma Thuột. Cung cấp Robusta & Arabica nguyên chất từ vườn hữu cơ canh tác bền vững. Chứng nhận 4C, UTZ. Năng lực: 50 tấn cà phê nhân/năm. |
| 2 | **Highlands Coffee** | Chuỗi cà phê hàng đầu VN (700+ cửa hàng). Cà phê rang xay cao cấp & trà đặc trưng. Nguyên liệu từ Lâm Đồng. ISO 22000, HACCP. Năng lực: 200 tấn/năm. |
| 3 | **Organica** | Hệ thống phân phối thực phẩm hữu cơ uy tín (từ 2012). Hợp tác 30+ nông trại hữu cơ. Chứng nhận USDA, EU Organic, PGS VN. Năng lực: 500 đơn/ngày. |
| 4 | **Koita** | Sữa hữu cơ cao cấp nhập khẩu từ Ý, phân phối Đông Nam Á. EU Organic, không chất bảo quản. Kho lạnh 10.000 lít tại Q.2 TP.HCM. Đối tác khách sạn 5 sao. |
| 5 | **Mùa** | Nông sản hữu cơ Đà Lạt. Trang trại 5ha nhà kính hiện đại, tưới nhỏ giọt Israel. Rau củ quả không hóa chất. VietGAP, PGS. Năng lực: 2 tấn rau/ngày. |
| 6 | **SonlanGa** | HTX nông nghiệp cộng đồng Gia Lai, 45 hộ đồng bào Jrai, 120ha canh tác. Trà thảo mộc, cà phê mật ong, hạt điều. OCOP 4 sao, VietGAP. 30 tấn/năm. |
| 7 | **Health Paradise** | Thương hiệu superfood hữu cơ Malaysia. Hạt quinoa, chia, lanh, granola. USDA Organic, Non-GMO. VP & kho tại Pearl Plaza TP.HCM. 15.000 SP/tháng. |
| 8 | **Co.op Finest** | Dòng cao cấp Saigon Co.op (800+ điểm bán). Rau hữu cơ, trái cây NK, thịt bò Úc, hải sản tươi. QR truy xuất nguồn gốc. GlobalGAP, ISO 22000. 50.000 SP/tháng. |
| 9 | **Vua Gạo** | Gạo sạch chuẩn xuất khẩu, KCN Tân Đô, Long An. Vùng nguyên liệu 500ha liên kết. ST25, Jasmine, gạo lứt hữu cơ. HACCP, GlobalGAP. Xay xát: 100 tấn/ngày. |
| 10 | **Cát Tường** | Trái cây nhiệt đới xuất khẩu Mỹ Tho, Tiền Giang. Bưởi da xanh, xoài Hòa Lộc, sầu riêng Ri6. 200ha liên kết. VietGAP, GlobalGAP. XK sang EU, Nhật, Hàn. 20 tấn/ngày. |


#### Ảnh giới thiệu nhà cung cấp (image_url) — Nguồn: Unsplash (miễn phí)

| STT | Tên NCC | Chủ đề ảnh | Link ảnh |
| :---: | :--- | :--- | :--- |
| 1 | Gờ Cafe | Hạt cà phê rang xay | `https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&q=80` |
| 2 | Highlands Coffee | Cà phê thưởng thức | `https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=800&q=80` |
| 3 | Organica | Rau xanh hữu cơ tươi | `https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&q=80` |
| 4 | Koita | Sữa tươi hữu cơ | `https://images.unsplash.com/photo-1563636619-e9143da7973b?w=800&q=80` |
| 5 | Mùa | Vườn rau nhà kính | `https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80` |
| 6 | SonlanGa | Trà thảo mộc khô | `https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=800&q=80` |
| 7 | Health Paradise | Ngũ cốc & hạt dinh dưỡng | `https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80` |
| 8 | Co.op Finest | Quầy thực phẩm cao cấp | `https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&q=80` |
| 9 | Vua Gạo | Cánh đồng lúa vàng | `https://images.unsplash.com/photo-1536054953991-6c3cbeab783c?w=800&q=80` |
| 10 | Cát Tường | Trái cây nhiệt đới | `https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=800&q=80` |

---

## 📅 Nhật ký cập nhật

### [2026-07-06 21:40] Cập nhật ảnh giới thiệu cho 10 Nhà cung cấp
* **Tác vụ**: Tìm và gán ảnh giới thiệu chất lượng cao từ Unsplash cho 10 NCC, phù hợp với chủ đề kinh doanh (cà phê, rau hữu cơ, sữa, trà thảo mộc, ngũ cốc, siêu thị, lúa gạo, trái cây).
* **Trạng thái**: ✅ Đã hoàn thành.

### [2026-07-06 21:32] Tạo sinh thông tin chi tiết cho 10 Nhà cung cấp
* **Tác vụ**: Bổ sung mô tả doanh nghiệp chi tiết chuẩn enterprise cho 10 NCC: lĩnh vực hoạt động, chứng nhận chất lượng (VietGAP, GlobalGAP, USDA, ISO, HACCP...), quy mô sản xuất và năng lực cung ứng.
* **Trạng thái**: ✅ Đã hoàn thành.

### [2026-07-06 21:27] Khôi phục 10 Nhà cung cấp từ Backup
* **Tác vụ**: Trích xuất dữ liệu 10 Farm từ `db.sqlite3.bak`, tạo lại trong CSDL hiện tại và gán đúng owner. Chuyển role 10 owner sang `FARMER` theo luồng hệ thống.
* **Trạng thái**: ✅ Đã hoàn thành. 10/10 farm khôi phục thành công với status `APPROVED`.
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

