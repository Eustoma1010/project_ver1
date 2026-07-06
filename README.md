# Verdant – Nền tảng Nông sản sạch Hữu cơ tích hợp Blockchain

Verdant là nền tảng thương mại điện tử nông sản sạch cao cấp, kết nối trực tiếp các gia đình thành thị với các nông trại hữu cơ uy tín khắp Việt Nam. Điểm đặc biệt của Verdant là tích hợp công nghệ Blockchain để đảm bảo tính minh bạch và truy xuất nguồn gốc tuyệt đối cho từng lô hàng sản xuất.

---

## 🌟 Tính năng cốt lõi

1. **Khách hàng (Buyers):**
   - Tìm kiếm, đặt mua nông sản hữu cơ theo danh mục và vùng miền.
   - Thêm sản phẩm yêu thích và đặt hàng nhanh chóng.
   - **Truy xuất nguồn gốc thời gian thực:** Quét mã QR hoặc xem dòng thời gian (timeline) hành trình của sản phẩm được lấy trực tiếp từ Sổ cái Blockchain (mã giao dịch, nhiệt độ bảo quản, chỉ số pH, ngày thu hoạch, đơn vị vận chuyển).

2. **Đối tác Nông trại (Farmers):**
   - Đăng ký hồ sơ doanh nghiệp/nông trại chờ Ban quản trị duyệt.
   - Đăng sản phẩm và quản lý thông tin sản phẩm.
   - **Ghi nhật ký sản xuất lên Blockchain:** Tạo các lô hàng mới (Batch) và cập nhật các cột mốc thực tế (Gieo hạt, bón phân, kiểm nghiệm chất lượng, thu hoạch, đóng gói).
   - Quản lý và duyệt đơn đặt hàng từ khách hàng.

3. **Vận chuyển & Giao nhận (Logistics):**
   - Ghi nhận trạng thái giao nhận và băm mã bảo mật giao nhận (SHA-256) trực tiếp lên Blockchain khi đơn hàng được giao thành công.

4. **Trình khám phá khối (Blockchain Explorer):**
   - Giao diện trực quan giúp xem danh sách các giao dịch (transactions), mã băm (tx hash), địa chỉ người gửi/người nhận ngay trên mạng lưới cục bộ.

---

## 📂 Cấu trúc thư mục dự án

```text
project_ver1/
├── backend/            # Mã nguồn Python/Django (API & Logic xử lý chính)
│   ├── apps/
│   │   ├── farm/       # Quản lý nông trại, sản phẩm đối tác, nhật ký sản xuất
│   │   ├── orders/     # Đơn hàng, thanh toán, vận chuyển
│   │   ├── products/   # Trang chủ, hiển thị sản phẩm, Blockchain Explorer
│   │   └── users/      # Đăng ký, đăng nhập, hồ sơ cá nhân
│   └── core/           # Cấu hình dự án Django (Settings, URLs)
├── frontend/           # Giao diện tĩnh (HTML templates, JS & logo)
│   ├── templates/      # Django HTML Templates (Base, Home, Farm, Explorer, v.v.)
│   └── static/         # File tĩnh (Logo, Javascript xử lý modal & icon)
├── contract/           # Smart Contract Solidity & cấu hình Hardhat (Ethereum local)
│   ├── contracts/      # Mã nguồn Solidity (VerdantTraceability.sol)
│   ├── scripts/        # Script triển khai Smart Contract (deploy.js)
│   └── test/           # Unit tests cho Smart Contract
├── DESIGN.md           # Hệ thống thiết kế của Verdant (Màu sắc, Font chữ Manrope)
└── PRODUCT.md          # Đặc tả sản phẩm, chân dung khách hàng & nguyên tắc thiết kế
```

---

## 🛠️ Hướng dẫn cài đặt và vận hành

### 1. Khởi chạy Blockchain cục bộ (Hardhat)
Yêu cầu cài đặt [Node.js](https://nodejs.org/).

1. Di chuyển vào thư mục contract:
   ```bash
   cd contract
   ```
2. Cài đặt các gói phụ thuộc:
   ```bash
   npm install
   ```
3. Chạy Node Hardhat cục bộ (mạng thử nghiệm Ethereum):
   ```bash
   npx hardhat node
   ```
4. Triển khai Smart Contract lên mạng Hardhat vừa chạy:
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```
   *Lưu ý địa chỉ Contract sau khi deploy thành công để cập nhật vào cấu hình hệ thống nếu cần.*

### 2. Thiết lập Backend Django
Yêu cầu Python 3.10 – 3.12.

1. Di chuyển vào thư mục backend:
   ```bash
   cd backend
   ```
2. Khởi tạo và kích hoạt môi trường ảo:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Trên Linux/macOS
   # hoặc .venv\Scripts\activate trên Windows
   ```
3. Cài đặt các thư viện:
   ```bash
   pip install -r requirements.txt
   ```
4. Chạy migration tạo cơ sở dữ liệu:
   ```bash
   python manage.py migrate
   ```
5. Khởi chạy máy chủ phát triển (Dev server):
   ```bash
   python manage.py runserver
   ```

---

## 🎨 Hệ thống thiết kế (Design System)

Dự án áp dụng hệ thống thiết kế **Verdant** mang phong cách tự nhiên, cao cấp:
- **Font chủ đạo:** Tiêu đề dùng phông chữ không chân **Manrope** hiện đại, thân thiện; Nội dung dùng **Be Vietnam Pro** rõ ràng, dễ đọc.
- **Tông màu:**
  - `Primary` - Xanh lục bảo (#007A36): Thể hiện sự tươi mát của nông trại sạch.
  - `Accent` - Vàng hổ phách (#F5A300): Thể hiện sự ấm áp hữu cơ và chất lượng.
  - `Background` - Meadow Background (#F4F9F1): Dịu mắt thay cho màu trắng tinh thông thường.
