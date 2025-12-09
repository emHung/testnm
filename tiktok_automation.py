#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import os

class TikTokAutomation:
    """Tự động hóa các hành động trên TikTok"""
    
    def __init__(self, use_adb=False):
        self.use_adb = use_adb
        self.adb_path = "adb"  # Hoặc đường dẫn đầy đủ
    
    def parse_tiktok_link(self, link):
        """Phân tích link TikTok để lấy username"""
        # Link dạng: https://www.tiktok.com/@username
        if '@' in link:
            username = link.split('@')[1].split('?')[0].split('/')[0]
            return username
        return None
    
    def open_tiktok_profile(self, link):
        """Mở profile TikTok"""
        if self.use_adb:
            # Mở trên Android qua ADB
            try:
                subprocess.run([
                    self.adb_path, "shell", "am", "start", "-a",
                    "android.intent.action.VIEW", "-d", link
                ], timeout=10)
                return True
            except Exception as e:
                print(f"❌ Lỗi ADB: {e}")
                return False
        else:
            # Mở trên trình duyệt
            import webbrowser
            webbrowser.open(link)
            return True
    
    def auto_follow_tiktok(self, link, wait_time=5):
        """
        Tự động follow TikTok
        
        Lưu ý: Hàm này chỉ mở link, bạn cần:
        1. Đăng nhập TikTok trước
        2. Thực hiện follow thủ công hoặc dùng automation tool
        """
        print(f"📱 Đang mở TikTok profile...")
        print(f"🔗 Link: {link}")
        
        username = self.parse_tiktok_link(link)
        if username:
            print(f"👤 Username: @{username}")
        
        # Mở link
        if not self.open_tiktok_profile(link):
            return False
        
        print(f"\n⏰ Vui lòng thực hiện hành động:")
        print(f"   1. Nhấn nút 'Follow' trên TikTok")
        print(f"   2. Đợi {wait_time} giây")
        
        # Đếm ngược
        for remaining in range(wait_time, 0, -1):
            print(f"\r⏳ Đợi {remaining} giây...", end='', flush=True)
            time.sleep(1)
        print()
        
        return True
    
    def auto_like_tiktok(self, link, wait_time=5):
        """Tự động like video TikTok"""
        print(f"📱 Đang mở TikTok video...")
        print(f"🔗 Link: {link}")
        
        # Mở link
        if not self.open_tiktok_profile(link):
            return False
        
        print(f"\n⏰ Vui lòng thực hiện hành động:")
        print(f"   1. Nhấn nút 'Like' ❤️ trên video")
        print(f"   2. Đợi {wait_time} giây")
        
        # Đếm ngược
        for remaining in range(wait_time, 0, -1):
            print(f"\r⏳ Đợi {remaining} giây...", end='', flush=True)
            time.sleep(1)
        print()
        
        return True
    
    def auto_comment_tiktok(self, link, comment_text, wait_time=5):
        """Tự động comment video TikTok"""
        print(f"📱 Đang mở TikTok video...")
        print(f"🔗 Link: {link}")
        print(f"💬 Comment: {comment_text}")
        
        # Mở link
        if not self.open_tiktok_profile(link):
            return False
        
        print(f"\n⏰ Vui lòng thực hiện hành động:")
        print(f"   1. Nhấn vào icon comment 💬")
        print(f"   2. Nhập: {comment_text}")
        print(f"   3. Gửi comment")
        print(f"   4. Đợi {wait_time} giây")
        
        # Đếm ngược
        for remaining in range(wait_time, 0, -1):
            print(f"\r⏳ Đợi {remaining} giây...", end='', flush=True)
            time.sleep(1)
        print()
        
        return True


class FacebookAutomation:
    """Tự động hóa các hành động trên Facebook"""
    
    def __init__(self, use_adb=False):
        self.use_adb = use_adb
        self.adb_path = "adb"
    
    def open_facebook_link(self, link):
        """Mở link Facebook"""
        if self.use_adb:
            try:
                subprocess.run([
                    self.adb_path, "shell", "am", "start", "-a",
                    "android.intent.action.VIEW", "-d", link
                ], timeout=10)
                return True
            except Exception as e:
                print(f"❌ Lỗi ADB: {e}")
                return False
        else:
            import webbrowser
            webbrowser.open(link)
            return True
    
    def auto_like_facebook(self, link, wait_time=5):
        """Tự động like Facebook"""
        print(f"📱 Đang mở Facebook...")
        print(f"🔗 Link: {link}")
        
        if not self.open_facebook_link(link):
            return False
        
        print(f"\n⏰ Vui lòng thực hiện hành động:")
        print(f"   1. Nhấn nút 'Like' 👍")
        print(f"   2. Đợi {wait_time} giây")
        
        for remaining in range(wait_time, 0, -1):
            print(f"\r⏳ Đợi {remaining} giây...", end='', flush=True)
            time.sleep(1)
        print()
        
        return True


class InstagramAutomation:
    """Tự động hóa các hành động trên Instagram"""
    
    def __init__(self, use_adb=False):
        self.use_adb = use_adb
        self.adb_path = "adb"
    
    def open_instagram_link(self, link):
        """Mở link Instagram"""
        if self.use_adb:
            try:
                subprocess.run([
                    self.adb_path, "shell", "am", "start", "-a",
                    "android.intent.action.VIEW", "-d", link
                ], timeout=10)
                return True
            except Exception as e:
                print(f"❌ Lỗi ADB: {e}")
                return False
        else:
            import webbrowser
            webbrowser.open(link)
            return True
    
    def auto_follow_instagram(self, link, wait_time=5):
        """Tự động follow Instagram"""
        print(f"📱 Đang mở Instagram...")
        print(f"🔗 Link: {link}")
        
        if not self.open_instagram_link(link):
            return False
        
        print(f"\n⏰ Vui lòng thực hiện hành động:")
        print(f"   1. Nhấn nút 'Follow'")
        print(f"   2. Đợi {wait_time} giây")
        
        for remaining in range(wait_time, 0, -1):
            print(f"\r⏳ Đợi {remaining} giây...", end='', flush=True)
            time.sleep(1)
        print()
        
        return True
