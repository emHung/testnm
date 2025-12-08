#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from curl_cffi import requests
import json

class GolikeAuth:
    def __init__(self):
        self.authorization = None
        self.auth_file = "auth.txt"
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.6,en;q=0.5',
            'content-type': 'application/json;charset=utf-8',
            'origin': 'https://app.golike.net',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            't': 'VFZSak1rNVVSVFZOVkdjd1RuYzlQUT09',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
    
    def save_token(self, token):
        """Lưu token vào file"""
        try:
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                f.write(token)
            print(f"✅ Đã lưu token vào {self.auth_file}")
        except Exception as e:
            print(f"⚠️ Không thể lưu token: {e}")
    
    def load_token(self):
        """Đọc token từ file"""
        try:
            with open(self.auth_file, 'r', encoding='utf-8') as f:
                token = f.read().strip()
                if token:
                    return token
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"⚠️ Không thể đọc token: {e}")
        return None
    
    def login(self, authorization_token):
        """Đăng nhập bằng authorization token"""
        self.authorization = authorization_token
        self.headers['authorization'] = f'Bearer {authorization_token}'
        
        try:
            response = requests.get(
                'https://gateway.golike.net/api/users/me',
                headers=self.headers,
                impersonate="chrome110"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✅ Đăng nhập thành công!")
                    # Lưu token vào file
                    self.save_token(authorization_token)
                    return True, data.get('data')
                else:
                    print("❌ Đăng nhập thất bại!")
                    return False, None
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return False, None
                
        except Exception as e:
            print(f"❌ Lỗi khi đăng nhập: {e}")
            return False, None
    
    def get_headers(self):
        """Trả về headers đã được cấu hình"""
        return self.headers
    
    def is_logged_in(self):
        """Kiểm tra trạng thái đăng nhập"""
        return self.authorization is not None
