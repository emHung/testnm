#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from curl_cffi import requests
import json
import time

class GolikeAuto:
    def __init__(self, headers):
        self.headers = headers
        self.current_account = None
        self.current_platform = None
    
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
                params=params,
                impersonate="chrome110"
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
    
    def complete_job(self, job):
        """Hoàn thành nhiệm vụ"""
        job_id = job.get('id')
        object_id = job.get('object_id')
        
        print(f"\n⏳ Đang xử lý nhiệm vụ ID: {job_id}...")
        
        try:
            # Bước 1: Skip job (mở nhiệm vụ)
            skip_url = f"https://gateway.golike.net/api/advertising/publishers/{self.current_platform.lower()}/jobs/{job_id}/skip"
            
            response = requests.post(
                skip_url,
                headers=self.headers,
                impersonate="chrome110"
            )
            
            if response.status_code != 200:
                print(f"❌ Không thể mở nhiệm vụ!")
                return False
            
            print(f"📱 Đã mở nhiệm vụ, đang thực hiện...")
            
            # Đợi một chút để giả lập thời gian thực hiện
            time.sleep(3)
            
            # Bước 2: Complete job
            complete_url = f"https://gateway.golike.net/api/advertising/publishers/{self.current_platform.lower()}/jobs/{job_id}/complete"
            
            response = requests.post(
                complete_url,
                headers=self.headers,
                impersonate="chrome110"
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
    
    def run_auto(self, max_jobs=10):
        """Chạy auto làm nhiệm vụ"""
        if not self.current_account or not self.current_platform:
            print("❌ Chưa chọn tài khoản!")
            return
        
        print(f"\n🚀 Bắt đầu auto {self.current_platform}...")
        print(f"📊 Giới hạn: {max_jobs} nhiệm vụ")
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
                print("\n⏳ Đợi 5 giây trước khi tiếp tục...")
                time.sleep(5)
        
        print("\n" + "="*60)
        print("📊 KẾT QUẢ AUTO")
        print("="*60)
        print(f"✅ Hoàn thành: {completed} nhiệm vụ")
        print(f"❌ Thất bại: {failed} nhiệm vụ")
        print(f"💰 Tổng thu nhập ước tính: {completed * 50} VNĐ")
        print("="*60)
