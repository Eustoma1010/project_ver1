# Kế hoạch thiết kế: Hệ thống Kiểm định chéo (Cross-Verification System)

## 📌 Tổng quan luồng và Vai trò người dùng
Hệ thống sẽ tích hợp vai trò **Kiểm định viên (Auditor/Inspector)** để xác thực chéo các thông tin nhật ký sản xuất (Milestones) của Nông dân trước khi thông tin được hoàn tất và hiển thị cho Khách hàng.

### 1. Vai trò người dùng mới
- **Auditor/Inspector:** Có quyền truy cập dashboard dành riêng cho kiểm định viên, phê duyệt hoặc từ chối các cột mốc nhật ký của từng lô hàng.

---

## 🌾 Luồng đăng ký & Xác minh đối tác Nông trại (Farmer Onboarding)
Quy trình đăng ký Nông dân được thiết kế theo mô hình mô phỏng kiểm định chéo 2 lớp (Admin hệ thống và Bên kiểm định thứ ba):

1. **Thông tin đăng ký nông trại:**
   - **Thông tin cơ bản:** Tên nông trại, Chủ sở hữu, Tỉnh/Thành phố, Địa chỉ chi tiết.
   - **Tài liệu kiểm chứng:** Tải lên hình ảnh Giấy phép kinh doanh / Đăng ký hộ kinh doanh (lưu trữ cục bộ trên server Django).
2. **Quy trình phê duyệt 2 giai đoạn:**
   - **Bước 1: Nông dân đăng ký:** Khi nông dân gửi biểu mẫu đăng ký, hồ sơ được lưu với trạng thái khởi tạo `PENDING_ADMIN` (Chờ Admin duyệt sơ bộ).
   - **Bước 2: Admin duyệt sơ bộ:** Quản trị viên (Admin) kiểm tra thông tin hành chính trong Django Admin. Nếu hợp lệ, duyệt chuyển trạng thái sang `PENDING_AUDITOR` (Chờ Kiểm định viên duyệt chuyên môn).
    - **Bước 3: Kiểm định viên phê duyệt:** Kiểm định viên bên thứ ba đăng nhập vào Dashboard kiểm định, xem hồ sơ, tiến hành đánh giá thực địa hoặc kiểm tra nghiệp vụ và quyết định:
      - **Phê duyệt (Approve):** Cấp giấy chứng nhận uy tín của bên thứ ba, chuyển trạng thái nông trại thành `APPROVED` (Đã duyệt). Lúc này Nông dân mới chính thức được mở khóa Dashboard để đăng sản phẩm và tạo lô hàng.
      - **Từ chối (Reject):** Chuyển trạng thái sang `REJECTED` (Từ chối cấp phép).
    - **Ràng buộc bảo mật & hiển thị đặc thù:**
      - **Giao diện Nông dân trong thời gian duyệt:** Nông dân chưa được duyệt (`PENDING_ADMIN`, `PENDING_AUDITOR`, `REJECTED`) hoặc bị đình chỉ (`SUSPENDED`) khi đăng nhập/truy cập cổng đối tác sẽ chỉ thấy giao diện hiển thị trạng thái hồ sơ chi tiết, tuyệt đối **không hiển thị** các thanh menu quản lý doanh nghiệp, sản phẩm hay lô hàng.
      - **Danh sách công cộng:** Tất cả các nông trại có trạng thái chưa duyệt hoặc bị đình chỉ (`PENDING_ADMIN`, `PENDING_AUDITOR`, `REJECTED`, `SUSPENDED`) sẽ **hoàn toàn bị ẩn** khỏi danh sách nhà cung cấp công khai hiển thị trên trang chủ và các trang sản phẩm của Khách hàng. Chỉ hiển thị các nông trại đã `APPROVED`.
      - **Blockchain Update:** Chỉ khi trạng thái nông trại là `APPROVED`, Nông dân mới có quyền đăng ký sản phẩm mới, tạo lô hàng mới (Batch) và đẩy các khối (Block) nhật ký sản xuất mới lên Blockchain.
3. **Quy trình Đánh giá định kỳ & Đột xuất (Periodic & Surprise Audits):**
   - **Đánh giá định kỳ (6 tháng):** Hệ thống theo dõi ngày đánh giá gần nhất (`last_audit_date`). Khi đến hạn 6 tháng, Kiểm định viên sẽ thực hiện một đợt đánh giá lại hồ sơ và nông trại thực tế.
   - **Đánh giá đột xuất (Surprise Audit):** Kiểm định viên có quyền bắt đầu một đợt đánh giá đột xuất đối với một **Lô sản phẩm (Batch)** cụ thể hoặc toàn bộ Nông trại tại bất kỳ thời điểm nào.
   - **Kết quả đánh giá:**
     - **Đạt yêu cầu (Satisfied):** Chứng chỉ được giữ nguyên ở trạng thái `APPROVED`, ngày đánh giá gần nhất được cập nhật.
     - **Không đạt yêu cầu (Unsatisfied):** Chứng chỉ bị thu hồi lập tức, trạng thái nông trại chuyển thành `SUSPENDED` (Đình chỉ).
4. **Quy chế khóa quyền khi bị thu hồi chứng chỉ (Suspension & Legacy Orders):**
   - Khi nông trại bị `SUSPENDED` hoặc `REJECTED`:
     - **Khóa hoàn toàn các quyền:** Không thể đăng ký sản phẩm mới, không thể tạo lô hàng (Batch) mới, không thể ghi nhận các cột mốc nhật ký mới lên Blockchain.
     - **Ngoại lệ xử lý đơn hàng cũ (Legacy Orders):** Nông dân vẫn được giữ lại quyền truy cập mục Đơn hàng (Orders) để xử lý, cập nhật trạng thái vận chuyển và hoàn tất các đơn hàng đã được Khách hàng đặt mua **trước thời điểm bị đình chỉ**. Điều này giúp bảo vệ quyền lợi kinh tế của khách hàng và tránh tranh chấp hợp đồng cũ.
5. **Đảm bảo tương thích ngược (Backward Compatibility):**
   - **Bảo toàn CSDL cũ:** Không xóa bỏ trường `approved` (Boolean) cũ trong model `Farm`. Thay vào đó, ta sẽ đồng bộ hóa:
     - Khi `status = APPROVED` -> `approved = True`.
     - Khi `status` ở các trạng thái khác -> `approved = False`.
     - Điều này đảm bảo tất cả các code cũ lọc theo `approved=True` hoặc `approved=False` vẫn chạy chính xác 100% mà không bị lỗi.
     - Giữ nguyên toàn bộ cấu trúc các hàm cũ và Smart Contract Solidity hiện tại.

---

## 🛠️ Luồng công việc (Workflow Plan)

### Bước 1: Đăng nhập & Điều hướng tự động (Login Flow)
- Màn hình đăng nhập chung (chuẩn Django username/password).
- Tài khoản Kiểm định viên (Auditor) được tạo thủ công bởi Quản trị viên (Admin).
- Sau khi đăng nhập thành công, hệ thống tự động kiểm tra vai trò (`role`):
  - `FARMER` -> Chuyển hướng tới `/farm/dashboard/`
  - `AUDITOR` -> Chuyển hướng tới `/auditor/dashboard/` (Trang quản lý dành riêng cho bên kiểm định thứ ba)
  - `BUYER` -> Chuyển hướng tới trang chủ `/` (hoặc trang hồ sơ cá nhân `/users/profile/`)
  - `ADMIN` -> Chuyển hướng tới trang quản trị `/admin/reports/`

### Bước 2: Thiết lập cơ chế Kiểm định chéo (Cross-Verification Logic)
Quy trình kiểm định và ghi nhận Cột mốc nhật ký (Milestones) được xây dựng theo mô hình kết hợp thực tế của doanh nghiệp (IBM Food Trust / TE-FOOD):

1. **Phân loại Cột mốc (Milestone Types):**
   - **Cột mốc thủ công (Farmer-declared):** Do nông dân tự nhập (ví dụ: bón phân, xử lý đất). 
     - Trạng thái mặc định: `PENDING_AUDIT` (Chờ kiểm định).
     - Chưa được ghi nhận lên Blockchain và chưa hiển thị công khai cho Khách hàng.
   - **Cột mốc tự động (IoT Automated):** Giả lập dữ liệu từ các cảm biến IoT (ví dụ: Nhiệt độ kho lạnh, Độ ẩm đất). Dữ liệu này được gửi tự động và đi thẳng lên Blockchain với trạng thái `VERIFIED` (Đã xác thực) vì đây là dữ liệu khách quan từ máy móc, không cần qua bước kiểm duyệt của con người.
2. **Nghiệp vụ Phê duyệt của Kiểm định viên:**
   - Kiểm định viên vào Dashboard xem danh sách cột mốc `PENDING_AUDIT`.
   - Khi bấm **Phê duyệt (Approve)**:
     - Mở hộp thoại yêu cầu nhập **Ý kiến kiểm định (Audit Opinion)** và **Mã số biên bản kiểm thực (Inspection ID)**.
     - Khi lưu, thông tin này cùng với danh tính Kiểm định viên sẽ được ký và ghi nhận vĩnh viễn lên Blockchain. Trạng thái cột mốc đổi thành `VERIFIED`, bắt đầu hiển thị công khai cho Khách hàng.
   - Khi bấm **Từ chối (Reject)**:
     - Yêu cầu nhập **Lý do từ chối (Rejection Reason)**.
     - Trạng thái đổi thành `REJECTED` (Không hiển thị cho khách hàng, gửi phản hồi để nông dân điều chỉnh).

---

## 📅 Các đầu việc cần làm (Todo List)

- [x] **Database & Models:**
  - Cập nhật model `Farm`: 
    - Thêm trường Giấy phép kinh doanh (image file).
    - Thêm trường trạng thái duyệt `status` (`PENDING_ADMIN`, `PENDING_AUDITOR`, `APPROVED`, `REJECTED`, `SUSPENDED`).
    - Thêm trường `last_audit_date` (Date, null=True) và `next_audit_deadline` (Date, null=True).
    - Cài đặt phương thức save() hoặc signal tự động cập nhật trường boolean `approved` cũ (nếu `status == APPROVED` -> `approved = True`, ngược lại -> `approved = False`) để đảm bảo tương thích ngược.
  - Thêm vai trò `AUDITOR` vào `ROLE_CHOICES` trong `CustomUser` model.
  - Thêm model `FarmAudit` (để ghi nhận lịch sử các đợt đánh giá định kỳ/đột xuất: nông trại, kiểm định viên, ngày kiểm định, kết quả đạt/không đạt, nhận xét).
  - Cập nhật model `BatchMilestone`: Thêm trường `status` (PENDING_AUDIT, VERIFIED, REJECTED), `milestone_type` (MANUAL, IOT), `audit_opinion` (text), `inspection_id` (char), `auditor` (FK to CustomUser).
  - Chạy migration (`makemigrations`, `migrate`).

- [x] **Luồng đăng ký & Duyệt đối tác (Farmer Onboarding):**
  - Cập nhật Form đăng ký nông trại `FarmRegistrationForm` thu thập các trường thông tin cơ bản và ảnh Giấy phép kinh doanh.
  - Thiết kế lại trang đăng ký nông trại [register.html](file:///data/worktime/project_ver1/frontend/templates/farm/register.html) đẹp mắt.
  - Viết chức năng duyệt 2 lớp: Admin duyệt chuyển lên trạng thái `PENDING_AUDITOR`, sau đó Kiểm định viên duyệt chuyển lên `APPROVED` hoặc `REJECTED`.
  - Chỉ hiển thị nông trại `APPROVED` trên danh sách đối tác công khai (Trang chủ và Trang sản phẩm).

- [x] **Luồng Đăng nhập, Chuyển hướng & Chặn quyền (Login & Access Control):**
  - Cập nhật View xử lý đăng nhập để tự động chuyển hướng dựa trên vai trò của user.
  - Xây dựng decorator hoặc hàm check quyền: Nông dân chỉ được phép thêm sản phẩm mới, thêm Batch mới, cập nhật Milestone mới khi nông trại có trạng thái `APPROVED`.
  - Đối với các nông trại bị `SUSPENDED` hoặc `REJECTED`: Chặn toàn bộ các quyền trên, NHƯNG vẫn cho phép truy cập danh sách đơn hàng `/farm/orders/` để xử lý các đơn hàng cũ đã đặt trước đó.

- [x] **Giao diện & Chức năng cho Kiểm định viên (Auditor Dashboard):**
  - Tạo view và template dashboard kiểm định viên `/auditor/dashboard/`.
  - Hiển thị danh sách nông trại chờ duyệt (`PENDING_AUDITOR`), danh sách nông trại đang hoạt động để thực hiện Đánh giá định kỳ/đột xuất, và danh sách cột mốc chờ xác thực.
  - Thêm chức năng Approve/Reject nông trại & cột mốc nhật ký (kèm popup nhập ý kiến đánh giá và cập nhật Blockchain).
  - Thêm chức năng tạo Biên bản đánh giá (`FarmAudit`) và đình chỉ nông trại (`SUSPENDED`) nếu trượt đánh giá đột xuất.

- [x] **Giao diện Khách hàng & Truy xuất:**
  - Chỉ hiển thị các cột mốc đã được xác thực (`VERIFIED`) trên trang hành trình sản phẩm của Khách hàng. Hiển thị nhãn phân biệt "Tự động (IoT Sensors)" và "Đã xác thực bởi Kiểm định viên".

- [x] **Luồng Phê duyệt Sản phẩm 2 lớp (Product Approval Flow):**
  - Cập nhật model `Product`: Mặc định `available = False` khi tạo mới và thêm trường trạng thái `status` (`PENDING_ADMIN`, `PENDING_AUDITOR`, `APPROVED`, `REJECTED`).
  - Giao diện Admin: Thêm phần duyệt sơ bộ sản phẩm mới tại `/admin/reports/` (chuyển sang `PENDING_AUDITOR`).
  - Giao diện Auditor: Thêm phần thẩm định sản phẩm mới tại Auditor Dashboard `/farm/auditor/dashboard/` (chuyển sang `APPROVED`).
  - Giao diện Khách hàng: Hiển thị sản phẩm chưa sẵn có (chưa có lô hàng thu hoạch và kiểm định) với nhãn "Chưa có hàng / Hàng không có sẵn" và chặn thêm vào giỏ hàng.
