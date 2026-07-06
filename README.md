# 🌿 Verdant – Nền tảng Nông sản sạch Hữu cơ tích hợp Blockchain

> **Creative North Star: "The Sunlit Orchard"**  
> *Sự trong lành, tươi mát của thiên nhiên tươi tốt kết hợp với sự minh bạch, an tâm tuyệt đối của công nghệ Blockchain.*

[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Django%20%7C%20Hardhat-green.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)]()

---

## 📖 Tổng quan dự án

**Verdant** là nền tảng thương mại điện tử nông sản sạch cao cấp, kết nối trực tiếp các gia đình thành thị có lối sống hiện đại với các nông trại hữu cơ uy tín khắp Việt Nam. 

Nhằm giải quyết triệt để nỗi lo ngại về nguồn gốc thực phẩm, Verdant tiên phong ứng dụng **Sổ cái Blockchain (Ethereum cục bộ)** để ghi nhận thời gian thực mọi mốc canh tác và vận chuyển của từng lô sản phẩm. Từ đó, mang lại trải nghiệm mua sắm đẳng cấp và niềm tin tuyệt đối cho khách hàng.

---

## 🌟 Tính năng cốt lõi

### 1. Phân hệ Khách hàng (Buyer Journey)
* **Mua sắm cao cấp:** Khám phá sản phẩm theo vùng miền, danh mục nông sản; quản lý danh sách yêu thích và giỏ hàng thông minh.
* **Truy xuất nguồn gốc Blockchain:**
  - Quét mã QR hoặc truy cập trang hành trình lô hàng.
  - Xem thông số kỹ thuật (độ pH, nhiệt độ, phân bón, độ ẩm đất) và mã băm giao dịch (transaction hash) được tải trực tiếp từ Smart Contract.
  - Tích hợp **Block Explorer** nội bộ để tra cứu lịch sử khối trực quan.

### 2. Phân hệ Nông trại đối tác (Farmer Dashboard)
* **Đăng ký đối tác:** Đăng ký thông tin nông trại và chờ quản trị viên phê duyệt.
* **Quản lý sản xuất:** Đăng tải sản phẩm, thiết lập trạng thái mở bán/hết hàng.
* **Ghi nhật ký Sổ cái:**
  - Khởi tạo lô hàng (Batch) đồng thời tự động kích hoạt giao dịch đăng ký lên Blockchain.
  - Nhật ký hoạt động: Ghi nhận các mốc (Gieo hạt, Chăm sóc, Kiểm nghiệm chất lượng, Thu hoạch, Đóng gói) kèm các thông số kỹ thuật của riêng từng ngành hàng (sữa, cà phê/trà, rau quả).

### 3. Vận chuyển & Giao nhận (Logistics Validation)
* **Xác thực giao hàng:** Khi đơn hàng hoàn thành, hệ thống tự động băm thông tin người nhận (Họ tên, Sđt, Địa chỉ) thành mã SHA-256 bảo mật và đẩy lên Blockchain để xác nhận hoàn tất quy trình cung ứng khép kín.

---

## 📂 Cấu trúc thư mục

```text
project_ver1/
├── backend/            # Mã nguồn chính Backend (Django 5.2)
│   ├── apps/
│   │   ├── farm/       # Logic quản lý nông trại, sản phẩm, lô hàng & Blockchain helper
│   │   ├── orders/     # Giỏ hàng, thanh toán và xử lý giao vận
│   │   ├── products/   # Trang chủ, Blockchain Explorer, API truy xuất nguồn gốc
│   │   └── users/      # Authentication (đăng ký, đăng nhập, hồ sơ)
│   └── core/           # Cấu hình dự án Django (Settings, URLs, WSGI)
├── frontend/           # Tài nguyên tĩnh & Giao diện người dùng
│   ├── templates/      # Django HTML Templates (bố cục kế thừa base.html)
│   └── static/         # File CSS, JS và logo
├── contract/           # Smart Contract Solidity & môi trường thử nghiệm Hardhat
│   ├── contracts/      # Hợp đồng thông minh VerdantTraceability.sol
│   ├── scripts/        # Script triển khai hợp đồng (deploy.js)
│   └── test/           # Unit tests kiểm thử Smart Contract
└── README.md           # Tài liệu hướng dẫn dự án
```

---

## 🛠️ Hướng dẫn cài đặt & Vận hành

### Bước 1: Khởi chạy Mạng lưới Blockchain (Hardhat)
Yêu cầu hệ thống đã cài đặt **Node.js** (Khuyên dùng v18+).

1. Truy cập thư mục hợp đồng:
   ```bash
   cd contract
   ```
2. Cài đặt các gói phụ thuộc:
   ```bash
   npm install
   ```
3. Chạy Node Blockchain cục bộ (mạng Ethereum giả lập):
   ```bash
   npx hardhat node
   ```
4. Mở một terminal mới và chạy script deploy để triển khai Smart Contract lên mạng localhost:
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```
   *Ghi lại địa chỉ Smart Contract xuất ra màn hình để đối chiếu.*

### Bước 2: Thiết lập Máy chủ Backend (Django)
Yêu cầu hệ thống đã cài đặt **Python 3.10 – 3.12**.

1. Truy cập thư mục backend:
   ```bash
   cd backend
   ```
2. Tạo và kích hoạt môi trường ảo:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Trên Linux/macOS
   # Hoặc: .venv\Scripts\activate trên Windows
   ```
3. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
4. Thực hiện ánh xạ Cơ sở dữ liệu (SQLite mặc định):
   ```bash
   python manage.py migrate
   ```
5. Khởi động server phát triển:
   ```bash
   python manage.py runserver
   ```
6. Truy cập website tại địa chỉ: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📐 Hệ thống thiết kế (Design System)

Trang web sử dụng ngôn ngữ thiết kế **Verdant** mang phong cách tối giản cao cấp, thân thiện với thiên nhiên:

* **Typography:**
  - **Tiêu đề lớn/vừa (Display/Headline):** Sử dụng phông chữ **Manrope** (sans-serif) sắc nét, hiện đại, tạo cảm giác chuyên nghiệp, gọn gàng.
  - **Nội dung (Body/Labels):** Sử dụng phông chữ **Be Vietnam Pro** chân thực, tối ưu hóa hiển thị tiếng Việt trên mọi thiết bị.
* **Palette màu tự nhiên:**
  - `Verdant Green` (#007A36): Màu xanh lá mướt mát đại diện cho nông trại organic (Primary).
  - `Amber Gold` (#F5A300): Màu vàng hổ phách mang lại sự ấm áp của nông sản chín dưới nắng (Accent).
  - `Meadow Background` (#F4F9F1): Tông nền tổng thể dịu nhẹ, tạo trải nghiệm đọc và mua sắm thư thái nhất.
  - `Forest Ink` (#1A3020): Màu chữ chủ đạo (thay thế màu đen tuyền để giao diện dịu mắt hơn).
