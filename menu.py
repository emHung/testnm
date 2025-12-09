#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os

class GolikeMenu:
    def __init__(self, headers):
        self.headers = headers
    
    def get_user_info(self):
        """Lấy thông tin người dùng"""
        print("\n📊 Đang lấy thông tin người dùng...")
        print("============================================================\n")
        
        try:
            response = requests.get(
                'https://gateway.golike.net/api/users/me',
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    user = data.get('data', {})
                    print(f"👤 Tên: {user.get('name')}")
                    print(f"📧 Email: {user.get('email')}")
                    print(f"💰 Số dư: {user.get('coin')} VNĐ")
                    print(f"🆔 User ID: {user.get('id')}")
                    return user
                else:
                    print("❌ Không thể lấy thông tin người dùng!")
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        return None
    
    def get_accounts(self, platform_name, api_endpoint):
        """Lấy danh sách tài khoản từ API"""
        try:
            response = requests.get(
                api_endpoint,
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                raw_data = data.get('data', [])
                
                # Facebook có cấu trúc data.data
                if platform_name == "Facebook" and isinstance(raw_data, dict):
                    accounts = raw_data.get('data', [])
                else:
                    accounts = raw_data
                
                # Kiểm tra nếu data không phải là list
                if not isinstance(accounts, list):
                    print(f"⚠️ Dữ liệu trả về không đúng định dạng")
                    return []
                
                return accounts
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Lỗi khi lấy tài khoản {platform_name}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def display_accounts(self, platform_name):
        """Hiển thị và cho phép chọn tài khoản"""
        print(f"\n📱 Danh sách tài khoản {platform_name}:")
        print("============================================================\n")
        
        if platform_name == "TikTok":
            api_endpoint = "https://gateway.golike.net/api/tiktok-account"
        elif platform_name == "Facebook":
            api_endpoint = "https://gateway.golike.net/api/fb-account"
        elif platform_name == "Instagram":
            api_endpoint = "https://gateway.golike.net/api/instagram-account"
        else:
            print("❌ Platform không hợp lệ!")
            return None
        
        accounts = self.get_accounts(platform_name, api_endpoint)
        
        if len(accounts) == 0:
            print(f"⚠️ Không tìm thấy tài khoản {platform_name} nào!")
            return None
        
        for idx, acc in enumerate(accounts, 1):
            if not isinstance(acc, dict):
                print(f"{idx}. ⚠️ Dữ liệu không hợp lệ: {acc}")
                continue
                
            if platform_name == "TikTok":
                print(f"{idx}. ID: {acc.get('id')} | @{acc.get('unique_username')} | {acc.get('nickname')}")
            elif platform_name == "Facebook":
                print(f"{idx}. ID: {acc.get('id')} | {acc.get('fb_name')} | UID: {acc.get('fb_id')}")
            elif platform_name == "Instagram":
                print(f"{idx}. ID: {acc.get('id')} | @{acc.get('username')} | {acc.get('full_name')}")
        
        print("\n0. Quay lại")
        
        try:
            choice = int(input("\n👉 Chọn tài khoản (nhập số): "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(accounts):
                selected_account = accounts[choice - 1]
                print(f"\n✅ Đã chọn tài khoản: {selected_account.get('id')}")
                return selected_account
            else:
                print("❌ Lựa chọn không hợp lệ!")
                return None
        except ValueError:
            print("❌ Vui lòng nhập số!")
            return None
    
    def show_main_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "="*60)
        print("🎯 GOLIKE AUTO - MENU CHÍNH")
        print("="*60)
        print("1. 📊 Xem thông tin tài khoản")
        print("2. 🎵 Làm nhiệm vụ TikTok")
        print("3. 📘 Làm nhiệm vụ Facebook")
        print("4. 📷 Làm nhiệm vụ Instagram")
        print("5. 📝 Xem log hoạt động")
        print("0. 🚪 Thoát")
        print("="*60)
    
    def view_log(self, log_file="auto_log.txt", lines=50):
        """Xem log hoạt động"""
        print("\n📝 LOG HOẠT ĐỘNG")
        print("="*60)
        
        try:
            if not os.path.exists(log_file):
                print("⚠️ Chưa có file log!")
                return
            
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            if len(all_lines) == 0:
                print("⚠️ File log trống!")
                return
            
            # Lấy N dòng cuối
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            print(f"Hiển thị {len(recent_lines)} dòng gần nhất:\n")
            for line in recent_lines:
                print(line.rstrip())
            
            print("\n" + "="*60)
            print(f"📊 Tổng số dòng log: {len(all_lines)}")
            
        except Exception as e:
            print(f"❌ Lỗi khi đọc log: {e}")
