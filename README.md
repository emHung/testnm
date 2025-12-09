# Golike Auto Tool

Tool tự động làm nhiệm vụ Golike cho TikTok, Facebook, Instagram.

## Tính năng

- ✅ Đăng nhập bằng Authorization Token
- ✅ Lưu token tự động vào file `auth.txt`
- ✅ Xem thông tin tài khoản
- ✅ Làm nhiệm vụ TikTok, Facebook, Instagram
- ✅ Tùy chỉnh delay giữa các nhiệm vụ
- ✅ Hỗ trợ MEmu giả lập (Windows)
- ✅ Chạy trên Termux (Android)

## Cài đặt trên Termux

### 1. Cài đặt Python và Git

```bash
pkg update && pkg upgrade
pkg install python git
```

### 2. Clone repository

```bash
git clone https://github.com/emHung/testnm.git
cd testnm
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

## Cài đặt trên Windows

### 1. Cài đặt Python

Tải Python từ [python.org](https://www.python.org/downloads/)

### 2. Clone repository

```bash
git clone https://github.com/emHung/testnm.git
cd testnm
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy chương trình

```bash
python main.py
```

### Lần đầu sử dụng

1. Nhập Authorization Token (lấy từ Golike)
2. Token sẽ được lưu vào `auth.txt`
3. Lần sau chạy sẽ tự động dùng token đã lưu

### Lấy Authorization Token

1. Đăng nhập vào [Golike](https://app.golike.net)
2. Mở DevTools (F12)
3. Vào tab Network
4. Tìm request có header `authorization`
5. Copy token (bỏ phần "Bearer ")

## Menu chính

```
1. 📊 Xem thông tin tài khoản
2. 🎵 Làm nhiệm vụ TikTok
3. 📘 Làm nhiệm vụ Facebook
4. 📷 Làm nhiệm vụ Instagram
0. 🚪 Thoát
```

## Cấu trúc thư mục

```
testnm/
├── main.py              # File chính
├── login.py             # Xử lý đăng nhập
├── menu.py              # Menu và hiển thị
├── auto.py              # Tự động làm nhiệm vụ
├── memu_controller.py   # Điều khiển MEmu (Windows)
├── List_account.py      # Test lấy danh sách account
├── requirements.txt     # Thư viện cần thiết
├── auth.txt            # Token đã lưu (tự động tạo)
└── README.md           # Hướng dẫn
```

## Lưu ý

- Token có thời hạn, nếu hết hạn cần nhập lại
- Delay giữa các nhiệm vụ nên >= 5 giây để tránh spam
- Trên Termux không hỗ trợ MEmu (chỉ Windows)
- Cần đăng nhập sẵn app trên MEmu nếu dùng chế độ giả lập

## Troubleshooting

### Lỗi "requests not found"

```bash
pip install --upgrade pip
pip install requests
```

### Lỗi kết nối

- Kiểm tra internet
- Kiểm tra token còn hạn không
- Thử đăng nhập lại

### MEmu không kết nối (Windows)

- Kiểm tra MEmu đã chạy chưa
- Kiểm tra đường dẫn MEmu đúng chưa
- Mặc định: `D:\Program Files\Microvirt\MEmu`

## License

MIT License

## Cập nhật code

### Xóa và clone lại

```bash
cd ~ && rm -rf testnm
git clone https://github.com/emHung/testnm.git
cd testnm && pip install -r requirements.txt
```

### Pull update

```bash
cd ~/testnm
git pull origin main
pip install -r requirements.txt
```

Xem chi tiết: [UPDATE_GUIDE.md](UPDATE_GUIDE.md)

## Disclaimer

Tool chỉ để học tập và nghiên cứu. Sử dụng có trách nhiệm.

