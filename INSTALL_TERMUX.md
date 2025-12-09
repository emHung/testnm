# Hướng dẫn cài đặt trên Termux

## Bước 1: Cài đặt Termux

Tải Termux từ [F-Droid](https://f-droid.org/packages/com.termux/) hoặc [GitHub](https://github.com/termux/termux-app/releases)

**Lưu ý:** Không dùng Termux từ Google Play Store (đã lỗi thời)

## Bước 2: Cập nhật và cài đặt packages

```bash
# Cập nhật packages
pkg update && pkg upgrade -y

# Cài đặt Python và Git
pkg install python git -y

# Cài đặt pip
pip install --upgrade pip
```

## Bước 3: Clone repository

```bash
# Di chuyển đến thư mục storage (tùy chọn)
cd ~/storage/downloads

# Clone project
git clone https://github.com/emHung/testnm.git
cd testnm


## Bước 4: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Nếu gặp lỗi cài đặt

```bash
# Cập nhật pip
pip install --upgrade pip

# Cài đặt lại
pip install -r requirements.txt
```

## Bước 5: Chạy chương trình

```bash
python main.py
```

## Lấy Authorization Token

### Cách 1: Trên điện thoại

1. Mở Chrome/Firefox trên điện thoại
2. Vào [app.golike.net](https://app.golike.net)
3. Đăng nhập
4. Mở DevTools (nếu có) hoặc dùng cách 2

### Cách 2: Từ máy tính

1. Đăng nhập Golike trên máy tính
2. Mở DevTools (F12)
3. Tab Network → tìm request có header `authorization`
4. Copy token và gửi về điện thoại

### Cách 3: Dùng Termux API

```bash
# Cài đặt Termux:API
pkg install termux-api

# Copy token từ clipboard
termux-clipboard-get
```

## Tips cho Termux

### Cho phép truy cập storage

```bash
termux-setup-storage
```

### Chạy ngầm (background)

```bash
# Cài đặt tmux
pkg install tmux

# Tạo session
tmux new -s golike

# Chạy tool
python main.py

# Thoát session (Ctrl+B rồi D)
# Quay lại session
tmux attach -t golike
```

### Tự động chạy khi mở Termux

Thêm vào file `~/.bashrc`:

```bash
echo "cd ~/testnm" >> ~/.bashrc
```

## Troubleshooting

### Lỗi "Permission denied"

```bash
chmod +x *.py
```

### Lỗi "No module named 'requests'"

```bash
pip install requests
```

### Lỗi "Connection timeout"

- Kiểm tra kết nối internet
- Thử đổi DNS: `pkg install dnsutils`
- Restart Termux

### Tool chạy chậm

- Termux có thể bị giới hạn tài nguyên
- Đóng các app khác
- Tăng delay giữa các nhiệm vụ

## Cập nhật code từ GitHub

### Xóa và clone lại (Đơn giản)

```bash
# Backup token
cp ~/testnm/auth.txt ~/auth_backup.txt

# Xóa thư mục cũ
cd ~ && rm -rf testnm

# Clone lại
git clone https://github.com/YOUR_USERNAME/testnm.git
cd testnm

# Restore token
cp ~/auth_backup.txt auth.txt

# Cài đặt
pip install -r requirements.txt
```

### Pull update (Giữ auth.txt)

```bash
cd ~/testnm
git stash
git pull origin main
git stash pop
pip install -r requirements.txt
```

Xem thêm: [UPDATE_GUIDE.md](UPDATE_GUIDE.md)

## Push lên GitHub (Cho dev)

### Lần đầu

```bash
# Cấu hình Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Tạo repository trên GitHub
# Sau đó:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/testnm.git
git push -u origin main
```

### Cập nhật sau này

```bash
git add .
git commit -m "Update features"
git push
```

## Lưu ý bảo mật

- **KHÔNG** push file `auth.txt` lên GitHub
- File `.gitignore` đã được cấu hình để bỏ qua
- Kiểm tra trước khi push: `git status`

## Commands nhanh

```bash
# Update nhanh (1 dòng)
cd ~/testnm && git stash && git pull && git stash pop && pip install -r requirements.txt

# Xóa và clone lại (1 dòng)
cd ~ && rm -rf testnm && git clone https://github.com/YOUR_USERNAME/testnm.git && cd testnm && pip install -r requirements.txt
```

