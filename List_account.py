#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.6,en;q=0.5',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3NjUxMjY5MTgsImV4cCI6MTc5NjY2MjkxOCwibmJmIjoxNzY1MTI2OTE4LCJqdGkiOiJXSEpBa21heFF2cDl3QkhMIiwic3ViIjozMDk3MTEwLCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.b_tUoAX8-L_16DyjaAdIV6wec-ApgFarRY1Sa5e87eo',
    'content-type': 'application/json;charset=utf-8',
    'origin': 'https://app.golike.net',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    't': 'VFZSak1rNVVSVFZOVkdjd1RuYzlQUT09',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

def get_accounts(platform_name, api_endpoint):
    """Lấy danh sách tài khoản từ API"""
    print(f"\n🚀 Đang lấy tài khoản {platform_name}...")
    print("============================================================\n")
    
    try:
        response = requests.get(
            api_endpoint,
            headers=headers
        )

        print(f"HTTP Status: {response.status_code}")

        data = response.json()
        print(f"API success: {data.get('success')}")
        
        # Xử lý cấu trúc data khác nhau cho từng platform
        raw_data = data.get('data', [])
        
        # Facebook có cấu trúc data.data
        if platform_name == "Facebook" and isinstance(raw_data, dict):
            accounts = raw_data.get('data', [])
        else:
            accounts = raw_data
        
        # Kiểm tra nếu data không phải là list
        if not isinstance(accounts, list):
            print(f"⚠️ Dữ liệu trả về không đúng định dạng: {type(accounts)}")
            return

        print(f"Số lượng tài khoản {platform_name}: {len(accounts)}\n")

        if len(accounts) > 0:
            print(f"Danh sách tài khoản {platform_name}:")
            
            if platform_name == "Facebook":
                # Hiển thị dạng bảng cho Facebook
                print("=" * 80)
                print(f"{'ID':<12} | {'FB_ID':<18} | {'FB_NAME':<40}")
                print("=" * 80)
                for acc in accounts:
                    if not isinstance(acc, dict):
                        continue
                    acc_id = str(acc.get('id', 'N/A'))
                    fb_id = str(acc.get('fb_id', 'N/A'))
                    fb_name = str(acc.get('fb_name', 'N/A'))
                    
                    # Cắt ngắn nếu quá dài
                    if len(fb_name) > 40:
                        fb_name = fb_name[:37] + "..."
                    
                    print(f"{acc_id:<12} | {fb_id:<18} | {fb_name:<40}")
                print("=" * 80)
            else:
                # Hiển thị bình thường cho TikTok và Instagram
                print("-" * 60)
                for acc in accounts:
                    if not isinstance(acc, dict):
                        continue
                    if platform_name == "TikTok":
                        print(f"ID: {acc.get('id')} | "
                              f"@{acc.get('unique_username')} | "
                              f"{acc.get('nickname')}")
                    elif platform_name == "Instagram":
                        print(f"ID: {acc.get('id')} | "
                              f"@{acc.get('username')} | "
                              f"{acc.get('full_name')}")
                print("-" * 60)
        else:
            print(f"⚠️ Không tìm thấy tài khoản {platform_name} nào!")

    except Exception as e:
        print(f"❌ Lỗi khi lấy tài khoản {platform_name}: {e}")
        import traceback
        traceback.print_exc()

# Lấy tài khoản TikTok
get_accounts("TikTok", "https://gateway.golike.net/api/tiktok-account")

# Lấy tài khoản Facebook
get_accounts("Facebook", "https://gateway.golike.net/api/fb-account")

# Lấy tài khoản Instagram
get_accounts("Instagram", "https://gateway.golike.net/api/instagram-account")
