# Verdant – Nền tảng Nông sản sạch Hữu cơ tích hợp Blockchain

[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Django%20%7C%20Hardhat-green.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)]()

---

## 1. Tổng quan dự án

**Verdant** là nền tảng thương mại điện tử nông sản sạch cao cấp, kết nối trực tiếp các gia đình thành thị có lối sống hiện đại với các nông trại hữu cơ uy tín khắp Việt Nam. 

Nhằm giải quyết triệt để nỗi lo ngại về nguồn gốc thực phẩm, Verdant tiên phong ứng dụng **Sổ cái Blockchain (Ethereum cục bộ)** để ghi nhận thời gian thực mọi mốc canh tác và vận chuyển của từng lô sản phẩm. Từ đó, mang lại trải nghiệm mua sắm đẳng cấp và niềm tin tuyệt đối cho khách hàng.

---

## 2. Tính năng cốt lõi

### phân hệ Khách hàng (Buyer Journey)
* **Mua sắm cao cấp:** Khám phá sản phẩm theo vùng miền, danh mục nông sản; quản lý danh sách yêu thích và giỏ hàng thông minh.
* **Truy xuất nguồn gốc Blockchain:**
  - Quét mã QR hoặc truy cập trang hành trình lô hàng.
  - Xem thông số kỹ thuật (độ pH, nhiệt độ, phân bón, độ ẩm đất) và mã băm giao dịch (transaction hash) được tải trực tiếp từ Smart Contract.
  - Tích hợp **Block Explorer** nội bộ để tra cứu lịch sử khối trực quan.

### phân hệ Nông trại đối tác (Farmer Dashboard)
* **Đăng ký đối tác:** Đăng ký thông tin nông trại và chờ quản trị viên phê duyệt.
* **Quản lý sản xuất:** Đăng tải sản phẩm, thiết lập trạng thái mở bán/hết hàng.
* **Ghi nhật ký Sổ cái:**
  - Khởi tạo lô hàng (Batch) đồng thời tự động kích hoạt giao dịch đăng ký lên Blockchain.
  - Nhật ký hoạt động: Ghi nhận các mốc (Gieo hạt, Chăm sóc, Kiểm nghiệm chất lượng, Thu hoạch, Đóng gói) kèm các thông số kỹ thuật của riêng từng ngành hàng (sữa, cà phê/trà, rau quả).

### Vận chuyển & Giao nhận (Logistics Validation)
* **Xác thực giao hàng:** Khi đơn hàng hoàn thành, hệ thống tự động băm thông tin người nhận (Họ tên, Sđt, Địa chỉ) thành mã SHA-256 bảo mật và đẩy lên Blockchain để xác nhận hoàn tất quy trình cung ứng khép kín.

---

## 3. Cấu trúc Thư mục & Tệp tin Vận hành

Dự án chỉ giữ lại các tệp tin vận hành cốt lõi, loại bỏ các thư mục đệm biên dịch và kiểm thử để đảm bảo mã nguồn tinh gọn nhất:

```text
project_ver1/
├── .env                          # Cấu hình môi trường (Cổng chạy, Secret Key...)
├── .gitignore                    # Cấu hình bỏ qua tệp tin của Git (như .venv, node_modules)
├── README.md                     # Tài liệu hướng dẫn và vận hành dự án (tệp này)
│
├── contract/                     # MODULE BLOCKCHAIN (Smart Contract Hardhat)
│   ├── contracts/
│   │   └── VerdantTraceability.sol # Hợp đồng thông minh Solidity quản lý hành trình lô hàng
│   ├── scripts/
│   │   └── deploy.js             # Kịch bản triển khai (deploy) Smart Contract lên mạng Hardhat cục bộ
│   ├── .gitignore                # Cấu hình bỏ qua tệp biên dịch của Hardhat
│   ├── hardhat.config.js         # Cấu hình compiler Solidity và mạng Hardhat cục bộ
│   └── package.json              # Khai báo dependencies NPM cho môi trường Blockchain
│
├── backend/                      # MODULE BACKEND (Django Server)
│   ├── manage.py                 # Lệnh điều khiển chính của dự án Django
│   ├── requirements.txt          # Khai báo các thư viện Python (Django, Web3.py, Pillow...)
│   ├── db.sqlite3                # Cơ sở dữ liệu SQLite hoạt động của hệ thống (chứa 96 sản phẩm, 10 buyers, 18 đơn hàng...)
│   │
│   ├── core/                     # Cấu hình dự án Django chính
│   │   ├── settings.py           # Cấu hình toàn bộ dự án Django (DB, Apps, Middleware)
│   │   ├── urls.py               # Định tuyến URLs chính của dự án
│   │   └── wsgi.py / asgi.py
│   │
│   └── apps/                     # Các ứng dụng nghiệp vụ Django
│       ├── farm/                 # Quản lý trang trại, kiểm định, giao dịch blockchain
│       │   ├── blockchain.py     # Module tích hợp Web3 kết nối Hardhat blockchain
│       │   ├── models.py / views.py / urls.py / forms.py
│       ├── products/             # Quản lý Danh mục, Sản phẩm, Lô hàng và Cột mốc
│       │   └── models.py / views.py / urls.py
│       ├── users/                # Quản lý Đăng ký, Đăng nhập và Phân quyền người dùng
│       │   └── models.py / views.py / urls.py
│       └── orders/               # Quản lý Giỏ hàng, Đặt hàng và Khấu trừ kho FIFO
│           └── models.py / views.py / urls.py
│
└── frontend/                     # MODULE FRONTEND (Giao diện Web App)
    └── templates/                # Toàn bộ giao diện HTML động của dự án (kế thừa base.html)
```

---

## 4. Hướng dẫn cài đặt & Vận hành

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
   *Địa chỉ deploy mặc định của Smart Contract trên mạng Hardhat cục bộ là: `0x5FbDB2315678afecb367f032d93F642f64180aa3`.*

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

## 5. Danh sách Tài khoản & Dữ liệu Kiểm thử

Hệ thống đã được thiết lập sẵn bộ dữ liệu kiểm thử chuẩn doanh nghiệp bao gồm các phân quyền tương ứng:

### 1. Tài khoản Hệ thống
*   **Quản trị viên (ADMIN)**: `admin` | Mật khẩu: `admin123`
*   **Thẩm định viên (AUDITOR)**: `auditor` | Mật khẩu: `auditor123`
*   **Khách mua mặc định (BUYER)**: `buyer` | Mật khẩu: `buyer123`

### 2. 10 Tài khoản Nhà cung cấp (Nông trại)
*   Mật khẩu chung cho tất cả tài khoản nông dân: `test123` (Vai trò: `FARMER`).
*   Danh sách:
    1.  `go_cafe_owner` - **Gờ Cafe** (Đắk Lắk)
    2.  `highlands_coffee_owner` - **Highlands Coffee** (Lâm Đồng)
    3.  `organica_owner` - **Organica** (Lâm Đồng)
    4.  `koita_owner` - **Koita** (TP. HCM)
    5.  `mua_owner` - **Mùa** (Lâm Đồng)
    6.  `sonlanga_owner` - **SonlanGa** (Gia Lai)
    7.  `health_paradise_owner` - **Health Paradise** (TP. HCM)
    8.  `coop_finest_owner` - **Co.op Finest** (TP. HCM)
    9.  `vua_gao_owner` - **Vua Gạo** (Long An)
    10. `cat_tuong_owner` - **Cát Tường** (Tiền Giang)

### 3. 10 Tài khoản Khách hàng (`BUYER`)
*   Mật khẩu chung cho tất cả người mua: `buyer123`.
*   Danh sách: `buyer`, `buyer_tuan`, `buyer_lan`, `buyer_dung`, `buyer_vy`, `buyer_hoang`, `buyer_mai`, `buyer_phong`, `buyer_chi`, `buyer_quan`.
*   *Mô phỏng*: Đã tạo sẵn **18 đơn hàng** thực tế từ 10 buyers, gán 26 sự kiện giao vận lên Blockchain cho các đơn hàng đã nhận.

---

## 6. Kịch bản Kiểm thử Hệ thống (Test Cases)

### CASE 1: Quy trình hoạt động chuẩn (Happy Path)
1.  **Nộp hồ sơ**: Farmer đăng nhập $\rightarrow$ Gửi thông tin đăng ký nông trại.
2.  **Duyệt hồ sơ**: Admin duyệt hồ sơ bước 1 $\rightarrow$ Nông trại chờ kiểm định.
3.  **Cấp chứng chỉ**: Auditor phê duyệt thực địa $\rightarrow$ Nông trại hoạt động, Farmer được cấp quyền đăng sản phẩm.
4.  **Đăng sản phẩm**: Farmer đăng sản phẩm mới $\rightarrow$ Auditor phê duyệt $\rightarrow$ Sản phẩm hiển thị trên trang chủ nhưng hết hàng.
5.  **Tạo lô hàng**: Farmer tạo lô sản phẩm mới $\rightarrow$ Thêm cột mốc lịch trình canh tác.
6.  **Xác thực mốc**: Auditor duyệt cột mốc $\rightarrow$ Sinh giao dịch Blockchain.
7.  **Thu hoạch**: Farmer tạo mốc đặc biệt `Thu hoạch & Đóng gói` $\rightarrow$ Auditor duyệt $\rightarrow$ Lô hàng chuyển sang `HARVESTED`, sản phẩm hiển thị "Còn hàng".
8.  **Đặt hàng**: Buyer đặt mua hàng $\rightarrow$ Đơn hàng `PENDING` $\rightarrow$ Hệ thống tự trừ kho FIFO của lô.
9.  **Giao hàng**: Farmer chuyển trạng thái đơn hàng thành `SHIPPED` $\rightarrow$ `DELIVERED` $\rightarrow$ Ký gửi biên lai giao nhận bảo mật lên Blockchain.

### CASE 2: Luồng Từ chối & Cập nhật lại (Rejection)
*   Admin từ chối hồ sơ nông trại hoặc Auditor từ chối cấp chứng chỉ $\rightarrow$ Trạng thái chuyển sang `REJECTED`, cho phép Farmer chỉnh sửa gửi duyệt lại.
*   Auditor từ chối duyệt cột mốc lịch trình $\rightarrow$ Cột mốc hiển thị nhãn đỏ từ chối, **không** được ghi nhận lên Blockchain.

### CASE 3: Thao tác hàng loạt & Bộ lọc liên kết
*   **Cascading Dropdowns**: Thay đổi dropdown Nông trại ở cột trái $\rightarrow$ Dropdown sản phẩm bên phải tự động cập nhật tương ứng không bị trùng lặp dữ liệu.
*   **Duyệt hàng loạt**: Auditor tích chọn nhiều sản phẩm/cột mốc hành trình và duyệt hàng loạt trong một lần click chuột.

### CASE 4: Đình chỉ hoạt động (Suspension)
*   Auditor đánh giá thực địa định kỳ nông trại "Không Đạt" $\rightarrow$ Nông trại tự động chuyển sang `SUSPENDED`.
*   Toàn bộ sản phẩm của nông trại bị ẩn khỏi cửa hàng; Farmer bị khóa quyền tạo lô hàng và cập nhật mốc lịch trình mới.

---

## 7. Hệ thống thiết kế (Design System)

Trang web sử dụng ngôn ngữ thiết kế **Verdant** tối giản, hiện đại mang hơi thở thiên nhiên:

*   **Typography:**
    -   *Tiêu đề (Display/Headline):* Sử dụng phông chữ **Manrope** (sans-serif) sắc nét, hiện đại, tạo cảm giác chuyên nghiệp.
    -   *Nội dung (Body/Labels):* Sử dụng phông chữ **Be Vietnam Pro** chân thực, tối ưu hiển thị tiếng Việt.
*   **Palette màu tự nhiên:**
    -   `Verdant Green` (#007A36): Màu xanh lá của nông sản sạch hữu cơ (Primary).
    -   `Amber Gold` (#F5A300): Màu vàng hổ phách của nắng ấm đồng quê (Accent).
    -   `Meadow Background` (#F4F9F1): Tông nền tổng thể mát mẻ, dễ chịu.
    -   `Forest Ink` (#1A3020): Màu chữ chủ đạo (thay thế màu đen tuyền giúp dịu mắt hơn).

---

## 8. Nhật ký cập nhật gần đây
*   **[2026-07-06 22:41]**: Tạo mới 3 danh mục và 6 bài viết tin tức hữu cơ, sức khỏe dạng HTML chuẩn để render mượt mà trên giao diện Modal.
*   **[2026-07-06 22:34]**: Tạo mới 9 tài khoản Buyer và tạo sinh 18 đơn hàng mô phỏng, trừ kho FIFO và đồng bộ 26 sự kiện giao vận lên Blockchain.
*   **[2026-07-06 22:28]**: Tạo sinh mới 96 lô hàng và 299 cột mốc lịch trình chất lượng cao, ký gửi thành công 395 giao dịch lên Hardhat Blockchain.
*   **[2026-07-06 22:06]**: Khôi phục và chuẩn hóa hoàn thiện 96 sản phẩm sạch của 10 nhà cung cấp.
*   **[2026-07-06 22:01]**: Làm sạch toàn bộ dữ liệu 10 Nhà cung cấp (xóa giấy phép kinh doanh thừa, sửa email/SĐT trùng lặp, phân bổ ngày kiểm định không trùng nhau).
*   **[2026-07-06 20:49]**: Deploy lại Blockchain Hardhat cục bộ, cập nhật địa chỉ Contract mới `0x5FbDB2315678afecb367f032d93F642f64180aa3`.
