#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
import os

class MemuController:
    def __init__(self, memu_path="D:\\Program Files\\Microvirt\\MEmu"):
        """Khởi tạo controller cho MEmu (chỉ Windows)"""
        self.memu_path = memu_path
        self.adb_path = os.path.join(memu_path, "adb.exe")
        self.memu_console = os.path.join(memu_path, "memuc.exe")
        
        # Kiểm tra hệ điều hành
        if os.name != 'nt':
            print("⚠️ MEmu chỉ hỗ trợ trên Windows!")
            print("💡 Trên Termux/Linux, vui lòng dùng chế độ trình duyệt.")
        
        # Package names cho các app
        self.packages = {
            "TikTok": "com.zhiliaoapp.musically",
            "Facebook": "com.facebook.katana",
            "Instagram": "com.instagram.android"
        }
    
    def check_memu_running(self):
        """Kiểm tra MEmu có đang chạy không"""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "127.0.0.1:21503" in result.stdout or "emulator" in result.stdout
        except Exception as e:
            print(f"❌ Lỗi khi kiểm tra MEmu: {e}")
            return False
    
    def start_memu(self, index=0):
        """Khởi động MEmu"""
        try:
            print(f"🚀 Đang khởi động MEmu {index}...")
            subprocess.Popen([self.memu_console, "start", "-i", str(index)])
            
            # Đợi MEmu khởi động
            for i in range(30):
                time.sleep(2)
                if self.check_memu_running():
                    print("✅ MEmu đã khởi động!")
                    return True
                print(f"⏳ Đang đợi MEmu khởi động... ({i+1}/30)")
            
            print("❌ Timeout khi khởi động MEmu!")
            return False
        except Exception as e:
            print(f"❌ Lỗi khi khởi động MEmu: {e}")
            return False
    
    def connect_adb(self):
        """Kết nối ADB với MEmu"""
        try:
            # Kết nối với port mặc định của MEmu
            subprocess.run([self.adb_path, "connect", "127.0.0.1:21503"], 
                         capture_output=True, timeout=5)
            time.sleep(1)
            return self.check_memu_running()
        except Exception as e:
            print(f"❌ Lỗi khi kết nối ADB: {e}")
            return False
    
    def open_app(self, platform):
        """Mở app trên MEmu"""
        package = self.packages.get(platform)
        if not package:
            print(f"❌ Không tìm thấy package cho {platform}")
            return False
        
        try:
            print(f"📱 Đang mở app {platform}...")
            
            # Mở app
            result = subprocess.run(
                [self.adb_path, "shell", "monkey", "-p", package, "-c", 
                 "android.intent.category.LAUNCHER", "1"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ Đã mở app {platform}!")
                time.sleep(3)
                return True
            else:
                print(f"❌ Không thể mở app: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi mở app: {e}")
            return False
    
    def tap_screen(self, x, y):
        """Tap vào vị trí trên màn hình"""
        try:
            subprocess.run(
                [self.adb_path, "shell", "input", "tap", str(x), str(y)],
                capture_output=True,
                timeout=5
            )
            return True
        except Exception as e:
            print(f"❌ Lỗi khi tap: {e}")
            return False
    
    def swipe_screen(self, x1, y1, x2, y2, duration=300):
        """Vuốt màn hình"""
        try:
            subprocess.run(
                [self.adb_path, "shell", "input", "swipe", 
                 str(x1), str(y1), str(x2), str(y2), str(duration)],
                capture_output=True,
                timeout=5
            )
            return True
        except Exception as e:
            print(f"❌ Lỗi khi swipe: {e}")
            return False
    
    def open_url(self, url):
        """Mở URL trên trình duyệt MEmu"""
        try:
            print(f"🌐 Đang mở URL: {url}")
            subprocess.run(
                [self.adb_path, "shell", "am", "start", "-a", 
                 "android.intent.action.VIEW", "-d", url],
                capture_output=True,
                timeout=10
            )
            time.sleep(2)
            return True
        except Exception as e:
            print(f"❌ Lỗi khi mở URL: {e}")
            return False
    
    def press_back(self):
        """Nhấn nút Back"""
        try:
            subprocess.run(
                [self.adb_path, "shell", "input", "keyevent", "KEYCODE_BACK"],
                capture_output=True,
                timeout=5
            )
            return True
        except Exception as e:
            print(f"❌ Lỗi khi nhấn Back: {e}")
            return False
    
    def press_home(self):
        """Nhấn nút Home"""
        try:
            subprocess.run(
                [self.adb_path, "shell", "input", "keyevent", "KEYCODE_HOME"],
                capture_output=True,
                timeout=5
            )
            return True
        except Exception as e:
            print(f"❌ Lỗi khi nhấn Home: {e}")
            return False
