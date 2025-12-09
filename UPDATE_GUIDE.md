# Hướng dẫn cập nhật code từ GitHub

## Cách 1: Xóa và clone lại (Đơn giản nhất)

### Trên Termux

```bash
# Di chuyển ra ngoài thư mục project
cd ~

# Xóa thư mục cũ
rm -rf golike-auto

# Clone lại từ GitHub
git clone https://github.com/YOUR_USERNAME/golike-auto.git

# Vào thư mục
cd golike-auto

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy tool
python main.py
```

**Lưu ý:** File `auth.txt` sẽ bị mất, cần đăng nhập lại!

### Backup token trước khi xóa

```bash
# Backup token
cp golike-auto/auth.txt ~/auth_backup.txt

# Sau khi clone lại, restore token
cp ~/auth_backup.txt golike-auto/auth.txt
```

## Cách 2: Pull update (Giữ lại auth.txt)

```bash
# Vào thư mục project
cd ~/golike-auto

# Stash các thay đổi local (bao gồm auth.txt)
git stash

# Pull code mới
git pull origin main

# Restore lại auth.txt
git stash pop

# Cài đặt thư viện mới (nếu có)
pip install -r requirements.txt
```

## Cách 3: Reset về code gốc

```bash
cd ~/golike-auto

# Backup auth.txt
cp auth.txt ~/auth_backup.txt

# Reset về code gốc
git fetch origin
git reset --hard origin/main

# Restore auth.txt
cp ~/auth_backup.txt auth.txt

# Cài đặt lại
pip install -r requirements.txt
```

## Kiểm tra version hiện tại

```bash
cd ~/golike-auto
git log --oneline -5
```

## Xem thay đổi trước khi pull

```bash
git fetch origin
git diff HEAD origin/main
```

## Nếu gặp lỗi "modified files"

```bash
# Xem file nào bị thay đổi
git status

# Nếu chỉ có auth.txt
git checkout -- .
git pull origin main
```

## Push code lên GitHub (Cho dev)

### Lần đầu

```bash
cd ~/golike-auto

# Cấu hình Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Add tất cả file (trừ auth.txt - đã có .gitignore)
git add .

# Commit
git commit -m "Update from Termux"

# Push
git push origin main
```

### Lần sau

```bash
cd ~/golike-auto

# Kiểm tra file thay đổi
git status

# Add file
git add .

# Commit với message
git commit -m "Fix bugs and improvements"

# Push
git push origin main
```

## Xử lý conflict

```bash
# Nếu có conflict khi pull
git pull origin main

# Xem file conflict
git status

# Sửa file conflict thủ công hoặc:
# Giữ code từ GitHub
git checkout --theirs <file>

# Hoặc giữ code local
git checkout --ours <file>

# Sau khi sửa xong
git add .
git commit -m "Resolve conflicts"
```

## Quick Commands

### Update nhanh (giữ auth.txt)

```bash
cd ~/golike-auto && git stash && git pull && git stash pop && pip install -r requirements.txt
```

### Xóa và clone lại nhanh

```bash
cd ~ && rm -rf golike-auto && git clone https://github.com/YOUR_USERNAME/golike-auto.git && cd golike-auto && pip install -r requirements.txt
```

### Backup và restore auth.txt

```bash
# Backup
cp ~/golike-auto/auth.txt ~/auth_backup.txt

# Restore
cp ~/auth_backup.txt ~/golike-auto/auth.txt
```

## Troubleshooting

### Lỗi "Permission denied"

```bash
chmod -R 755 ~/golike-auto
```

### Lỗi "Not a git repository"

```bash
cd ~/golike-auto
git init
git remote add origin https://github.com/YOUR_USERNAME/golike-auto.git
git fetch origin
git reset --hard origin/main
```

### Lỗi "Authentication failed"

Sử dụng Personal Access Token thay vì password:

1. Vào GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Copy token
4. Khi push, dùng token làm password

### Lỗi "pip install failed"

```bash
# Xóa cache
pip cache purge

# Cài lại
pip install --upgrade pip
pip install -r requirements.txt
```
