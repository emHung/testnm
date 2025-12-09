#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import os
from memu_controller import MemuController
from tiktok_automation import TikTokAutomation, FacebookAutomation, InstagramAutomation

class GolikeAuto:
    def __init__(self, headers):
        self.headers = headers
        self.current_account = None
        self.current_platform = None
        self.delay = 5  # Delay mặc định 5 giây
        self.memu = None
        self.use_memu = False
        
        # Automation helpers
        self.tiktok_auto = TikTokAutomation()
        self.facebook_auto = FacebookAutomation()
        self.instagram_auto = InstagramAutomation()
    
    def set_account(self, account, platform):
        """Thiết lập tài khoản và platform hiện tại"""
        self.current_account = account
        self.current_platform = platform
        print(f"\n✅ Đã thiết lập tài khoản {platform}: {account.get('id')}")
    
    def get_jobs(self):
        """Lấy danh sách nhiệm vụ"""
        if not self.current_account or not self.current_platform:
            print("❌ Chưa chọn tài khoản!")
            return []
        
        platform_map = {
            "TikTok": "tiktok",
            "Facebook": "facebook",
            "Instagram": "instagram"
        }
        
        platform_key = platform_map.get(self.current_platform)
        if not platform_key:
            print("❌ Platform không hợp lệ!")
            return []
        
        print(f"\n🔍 Đang tìm nhiệm vụ {self.current_platform}...")
        
        try:
            url = f"https://gateway.golike.net/api/advertising/publishers/{platform_key}/jobs"
            params = {
                'account_id': self.current_account.get('id'),
                'data': 'null'
            }
            
            response = requests.get(
                url,
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    jobs = data.get('data', [])
                    print(f"✅ Tìm thấy {len(jobs)} nhiệm vụ!")
                    return jobs
                else:
                    print(f"⚠️ {data.get('message', 'Không có nhiệm vụ')}")
                    return []
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Lỗi khi lấy nhiệm vụ: {e}")
            return []
    
    def open_job_on_memu(self, job):
        """Mở nhiệm vụ trên MEmu"""
        if not self.use_memu or not self.memu:
            return False
        
        link = job.get('link')
        if not link:
            return False
        
        try:
            # Mở app tương ứng
            if not self.memu.open_app(self.current_platform):
                return False
            
            # Đợi app mở
            time.sleep(3)
            
            # Mở link trong app
            self.memu.open_url(link)
            
            return True
        except Exception as e:
            print(f"❌ Lỗi khi mở job trên MEmu: {e}")
            return False
    
    def complete_job(self, job):
        """Hoàn thành nhiệm vụ"""
        job_id = job.get('id')
        object_id = job.get('object_id')
        link = job.get('link')
        
        print(f"\n⏳ Đang xử lý nhiệm vụ ID: {job_id}...")
        print(f"📝 Loại: {job.get('type')} | Giá: {job.get('price')} VNĐ")
        
        try:
            # Bước 1: Skip job (nhận nhiệm vụ)
            skip_url = f"https://gateway.golike.net/api/advertising/publishers/{self.current_platform.lower()}/jobs/{job_id}/skip"
            
            response = requests.post(
                skip_url,
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"❌ Không thể nhận nhiệm vụ!")
                return False
            
            skip_data = response.json()
            if not skip_data.get('success'):
                print(f"❌ Lỗi: {skip_data.get('message')}")
                return False
            
            print(f"✅ Đã nhận nhiệm vụ!")
            
            # Thực hiện nhiệm vụ tự động
            job_type = job.get('type', '').lower()
            
            if link:
                success = False
                
                if self.current_platform == "TikTok":
                    if 'follow' in job_type:
                        success = self.tiktok_auto.auto_follow_tiktok(link, wait_time=5)
                    elif 'like' in job_type:
                        success = self.tiktok_auto.auto_like_tiktok(link, wait_time=5)
                    elif 'comment' in job_type:
                        comment = job.get('comment_content', 'Nice video!')
                        success = self.tiktok_auto.auto_comment_tiktok(link, comment, wait_time=5)
                    else:
                        # Mở link mặc định
                        import webbrowser
                        webbrowser.open(link)
                        success = True
                
                elif self.current_platform == "Facebook":
                    success = self.facebook_auto.auto_like_facebook(link, wait_time=5)
                
                elif self.current_platform == "Instagram":
                    success = self.instagram_auto.auto_follow_instagram(link, wait_time=5)
                
                if not success:
                    print("⚠️ Không thể thực hiện tự động, vui lòng làm thủ công!")
                    time.sleep(10)
            else:
                print("⚠️ Không có link nhiệm vụ!")
                time.sleep(3)
            
            # Bước 2: Complete job
            print(f"📤 Đang gửi yêu cầu hoàn thành...")
            complete_url = f"https://gateway.golike.net/api/advertising/publishers/{self.current_platform.lower()}/jobs/{job_id}/complete"
            
            response = requests.post(
                complete_url,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Hoàn thành nhiệm vụ! Nhận: {job.get('price')} VNĐ")
                    return True
                else:
                    print(f"❌ Lỗi: {data.get('message')}")
                    return False
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi hoàn thành nhiệm vụ: {e}")
            return False
    
    def set_delay(self, delay):
        """Thiết lập thời gian delay giữa các nhiệm vụ"""
        self.delay = delay
        print(f"⏱️ Đã thiết lập delay: {delay} giây")
    
    def setup_memu(self, memu_path=None):
        """Thiết lập MEmu controller (chỉ Windows)"""
        # Kiểm tra hệ điều hành
        if os.name != 'nt':
            print("⚠️ MEmu chỉ hỗ trợ trên Windows!")
            print("💡 Sử dụng chế độ trình duyệt thay thế.")
            return False
        
        try:
            if memu_path:
                self.memu = MemuController(memu_path)
            else:
                self.memu = MemuController()
            
            # Kiểm tra MEmu
            if not self.memu.check_memu_running():
                print("⚠️ MEmu chưa chạy!")
                choice = input("👉 Khởi động MEmu? (Y/n): ").strip().lower()
                if choice != 'n':
                    if not self.memu.start_memu():
                        print("❌ Không thể khởi động MEmu!")
                        return False
            
            # Kết nối ADB
            if self.memu.connect_adb():
                print("✅ Đã kết nối với MEmu!")
                self.use_memu = True
                return True
            else:
                print("❌ Không thể kết nối ADB!")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi thiết lập MEmu: {e}")
            return False
    
    def run_auto(self, max_jobs=10):
        """Chạy auto làm nhiệm vụ"""
        if not self.current_account or not self.current_platform:
            print("❌ Chưa chọn tài khoản!")
            return
        
        # Hỏi có dùng MEmu không (chỉ trên Windows)
        if not self.use_memu and os.name == 'nt':
            use_memu_choice = input("\n👉 Sử dụng MEmu giả lập? (Y/n): ").strip().lower()
            if use_memu_choice != 'n':
                memu_path = input("👉 Đường dẫn MEmu (Enter = mặc định): ").strip()
                if memu_path:
                    self.setup_memu(memu_path)
                else:
                    self.setup_memu()
        
        print(f"\n🚀 Bắt đầu auto {self.current_platform}...")
        print(f"📊 Giới hạn: {max_jobs} nhiệm vụ")
        print(f"⏱️ Delay giữa các nhiệm vụ: {self.delay} giây")
        print(f"📱 Chế độ: {'MEmu' if self.use_memu else 'Trình duyệt'}")
        print("="*60)
        
        completed = 0
        failed = 0
        
        for i in range(max_jobs):
            print(f"\n--- Lần thử {i+1}/{max_jobs} ---")
            
            jobs = self.get_jobs()
            
            if len(jobs) == 0:
                print("⚠️ Không còn nhiệm vụ!")
                break
            
            job = jobs[0]  # Lấy nhiệm vụ đầu tiên
            
            if self.complete_job(job):
                completed += 1
            else:
                failed += 1
            
            # Đợi trước khi lấy nhiệm vụ tiếp theo
            if i < max_jobs - 1:
                print(f"\n⏳ Đợi {self.delay} giây trước khi tiếp tục...")
                time.sleep(self.delay)
        
        print("\n" + "="*60)
        print("📊 KẾT QUẢ AUTO")
        print("="*60)
        print(f"✅ Hoàn thành: {completed} nhiệm vụ")
        print(f"❌ Thất bại: {failed} nhiệm vụ")
        print(f"💰 Tổng thu nhập ước tính: {completed * 50} VNĐ")
        print("="*60)
