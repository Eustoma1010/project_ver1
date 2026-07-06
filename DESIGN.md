---
name: Verdant
description: Nông sản sạch hữu cơ thẳng từ vườn đầy nắng đến gia đình hiện đại
colors:
  primary: "#007A36"
  neutral-bg: "#F4F9F1"
  neutral-fg: "#1A3020"
  secondary: "#E4F2DB"
  accent: "#F5A300"
  card: "#FFFFFF"
  border: "rgba(0, 100, 50, 0.13)"
typography:
  display:
    fontFamily: "Playfair Display, Georgia, serif"
    fontSize: "clamp(2rem, 5vw, 3.75rem)"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "normal"
  body:
    fontFamily: "Be Vietnam Pro, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
rounded:
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  full: "9999px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-primary-hover:
    backgroundColor: "#00632b"
  card-product:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.lg}"
    border: "1px solid {colors.border}"
---

# Design System: Verdant

## 1. Overview

**Creative North Star: "The Sunlit Orchard"**

Verdant là sự kết tinh giữa năng lượng trong lành, mát mẻ của các trang trại hữu cơ và sự ấm áp mộc mạc từ đất trồng quê hương. Hệ thống thiết kế được lấy cảm hứng từ sự tinh khiết, sạch sẽ của Vinamilk kết hợp với sắc màu hữu cơ mộc mạc cao cấp của Cocoon Vietnam. Mục tiêu của Verdant là mang thiên nhiên tươi tốt đến với không gian sống hiện đại của các gia đình thành thị lớn.

Giao diện sử dụng mật độ thông tin thoáng đãng, các đường bo góc tròn đầy đặn tạo sự thân thiện, và các hiệu ứng chuyển động mượt mà biểu thị sự phát triển tự nhiên của thực vật. Hệ thống thiết kế này loại bỏ hoàn toàn các cấu trúc thô cứng, các banner tiếp thị nhồi nhét, tạo ra một trải nghiệm mua sắm thư thái giống như đang đi dạo giữa khu vườn ngập tràn ánh nắng.

**Key Characteristics:**
- Tông màu chủ đạo là xanh lục bảo mát mắt kết hợp với vàng hổ phách hữu cơ.
- Bo góc tròn trịa và mềm mại (8px đến 24px) tạo cảm xúc tự nhiên, an lành.
- Khoảng trắng phóng khoáng, giữ cho mắt người xem được thư giãn.

## 2. Colors

Bảng màu Verdant mang hơi thở của một khu vườn tươi tốt dưới nắng sớm.

### Primary
- **Verdant Green** (#007A36): Đại diện cho lá cây quang hợp, sự sinh sôi nảy nở. Được dùng cho các nút CTA chính, tiêu đề thương hiệu, và các thành phần nhấn quan trọng.

### Secondary
- **Sage Green** (#E4F2DB): Sắc xanh nhạt dịu mát của những đọt lá non, dùng làm nền phụ hoặc các nút danh mục phụ.

### Accent
- **Amber Gold** (#F5A300): Sắc vàng hổ phách của mật ong và quả chín dưới nắng, đem lại sự ấm áp hữu cơ (inspired by Cocoon). Dùng để nhấn các thẻ ưu đãi, các chứng nhận chất lượng hoặc các trạng thái nổi bật.

### Neutral
- **Meadow Background** (#F4F9F1): Màu nền tổng thể của toàn trang web, tạo cảm giác dịu mắt thay vì màu trắng tinh thông thường.
- **Forest Ink** (#1A3020): Màu chữ chủ đạo, sắc xanh đen đậm của thân gỗ lâu năm, tránh dùng màu đen tuyền thô cứng để đảm bảo tính tự nhiên tối đa.
- **Meadow Border** (rgba(0, 100, 50, 0.13)): Đường viền xanh mờ nhẹ nhàng kết nối các thẻ sản phẩm.

**The Ten Percent Rule.** Tông màu nhấn Amber Gold và Verdant Green chỉ được chiếm tối đa 10% diện tích bất kỳ màn hình nào. Sự hiếm hoi mới tạo nên giá trị và thu hút sự chú ý.

## 3. Typography

**Display Font:** Playfair Display (with Georgia, serif)
**Body Font:** Be Vietnam Pro (with sans-serif)

**Character:** Sự kết hợp tương phản tuyệt đẹp giữa nét thanh lịch cổ điển của phông chữ có chân Playfair Display ở các tiêu đề chính và nét hiện đại, rõ ràng dễ đọc của Be Vietnam Pro ở phần nội dung.

### Hierarchy
- **Display** (Bold, 32px đến 60px, Line-height: 1.2): Dùng cho tiêu đề biểu ngữ trang chủ (Hero section).
- **Headline** (Bold, 24px đến 30px, Line-height: 1.3): Dùng cho các tiêu đề phần chính (Sản phẩm nổi bật, Câu chuyện nông trại).
- **Title** (Semi-Bold, 16px đến 20px, Line-height: 1.4): Dùng cho tiêu đề sản phẩm, tên nông trại.
- **Body** (Regular, 14px đến 16px, Line-height: 1.6): Dùng cho mô tả sản phẩm, bài viết blog. Giới hạn độ rộng dòng ở 65-75ch để mắt người đọc không bị mỏi.
- **Label** (Semi-Bold, 11px đến 13px, Letter-spacing: 0.05em): Dùng cho xuất xứ sản phẩm, nhãn badge chất lượng.

## 4. Elevation

Hệ thống thiết kế Verdant hạn chế tối đa việc sử dụng bóng đổ đậm hoặc thô cứng để tránh cảm giác nhân tạo. Độ sâu được tạo ra chủ yếu bằng việc phân tầng màu sắc (Tonal Layering) giữa nền Meadow Background và các thẻ màu trắng thuần khiết.

### Shadow Vocabulary
- **Ambient Glow** (`box-shadow: 0 10px 25px -5px rgba(0, 100, 50, 0.05)`): Bóng đổ khuếch tán siêu nhẹ màu xanh lá cây mờ, chỉ hiển thị khi người dùng di chuột (hover) vào thẻ sản phẩm hoặc các nút bấm nổi để tạo phản hồi sinh động.

## 5. Components

Các thành phần được thiết kế bo góc tròn đầy đặn gợi lên các đường cong mềm mại của rau quả tự nhiên.

### Buttons
- **Shape:** Bo góc tròn hoàn toàn (rounded-full) cho nút CTA chính, hoặc góc bo lớn (rounded-xl) cho nút phụ.
- **Primary:** Nền màu Verdant Green (#007A36), chữ màu trắng, padding (12px 24px).
- **Hover / Focus:** Chuyển sang màu xanh đậm hơn (#00632b) và dịch chuyển nhẹ lên trên (translate-y[-2px]).

### Cards / Containers
- **Corner Style:** Bo góc lớn mềm mại (16px radius).
- **Background:** Trắng thuần khiết (#FFFFFF) để làm nổi bật hình ảnh nông sản trên nền Meadow Background.
- **Shadow Strategy:** Không đổ bóng ở trạng thái tĩnh. Chỉ kích hoạt Ambient Glow khi hover.
- **Border:** Viền Meadow Border siêu mỏng (1px).

### Inputs / Fields
- **Style:** Bo góc mềm mại (12px), nền màu nhạt (#EBF5E4) để dễ nhận biết.
- **Focus:** Viền đổi sang màu Verdant Green (#007A36) và có vòng hào quang mỏng mờ.

### Navigation
- **Style:** Header cố định (sticky) với hiệu ứng làm mờ nền kính mờ (backdrop-blur) trên tông màu trắng đục nhẹ nhàng, giữ kết nối thị giác khi cuộn trang.

## 6. Do's and Don'ts

### Do:
- **Do** Duy trì độ tương phản văn bản Forest Ink trên nền Meadow Background luôn ở mức cao (≥ 4.5:1).
- **Do** Sử dụng đường bo góc lớn mềm mại (rounded-2xl) cho mọi container chứa ảnh nông sản.
- **Do** Sử dụng font Playfair Display cho các tiêu đề chính để truyền tải cảm xúc thương hiệu cao cấp.

### Don't:
- **Don't** Sử dụng màu đen tuyền (#000000) cho chữ hoặc viền; luôn dùng màu Forest Ink (#1A3020) và Meadow Border.
- **Don't** Sử dụng bóng đổ tối màu, sắc nét hoặc góc cạnh khiến giao diện mang hơi hướng công nghệ/SaaS khô khan.
- **Don't** Sử dụng các đường kẻ sọc màu sắc bên trái thẻ (Side-stripe borders) làm điểm nhấn.
