#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from login import GolikeAuth
from menu import GolikeMenu
from auto import GolikeAuto

def clear_screen():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    
    print("="*60)
    print("🎯 GOLIKE AUTO TOOL")
    print("="*60)
    
    # Khởi tạo auth
    auth = GolikeAuth()
    
    # Kiểm tra token đã lưu
    saved_token = auth.load_token()
    
    if saved_token:
        print(f"\n🔑 Tìm thấy token đã lưu trong {auth.auth_file}")
        use_saved = input("👉 Sử dụng token này? (Y/n): ").strip().lower()
        
        if use_saved != 'n':
            print("✅ Đang đăng nhập bằng token đã lưu...")
            success, user_data = auth.login(saved_token)
            
            if success:
                # Đăng nhập thành công, tiếp tục
                pass
            else:
                print("\n⚠️ Token đã lưu không hợp lệ!")
                saved_token = None
    
    # Nếu không có token hoặc token không hợp lệ, yêu cầu nhập mới
    if not saved_token or not auth.is_logged_in():
        print("\n📝 Vui lòng nhập Authorization Token:")
        token_input = input("👉 Token: ").strip()
        
        if not token_input:
            print("❌ Token không được để trống!")
            input("\nNhấn Enter để thoát...")
            return
        
        success, user_data = auth.login(token_input)
    
    if not success:
        print("\n❌ Đăng nhập thất bại! Vui lòng kiểm tra lại token.")
        input("\nNhấn Enter để thoát...")
        return
    
    # Khởi tạo menu và auto
    menu = GolikeMenu(auth.get_headers())
    auto = GolikeAuto(auth.get_headers())
    
    # Vòng lặp menu chính
    while True:
        clear_screen()
        menu.show_main_menu()
        
        try:
            choice = input("\n👉 Chọn chức năng: ").strip()
            
            if choice == "0":
                print("\n👋 Tạm biệt!")
                break
            
            elif choice == "1":
                # Xem thông tin tài khoản
                menu.get_user_info()
                input("\nNhấn Enter để tiếp tục...")
            
            elif choice == "2":
                # Làm nhiệm vụ TikTok
                account = menu.display_accounts("TikTok")
                if account:
                    auto.set_account(account, "TikTok")
                    
                    try:
                        max_jobs = int(input("\n👉 Số lượng nhiệm vụ muốn làm (mặc định 10): ") or "10")
                    except ValueError:
                        max_jobs = 10
                    
                    try:
                        delay = int(input("👉 Delay giữa các nhiệm vụ (giây, mặc định 5): ") or "5")
                        auto.set_delay(delay)
                    except ValueError:
                        auto.set_delay(5)
                    
                    auto.run_auto(max_jobs)
                    input("\nNhấn Enter để tiếp tục...")
            
            elif choice == "3":
                # Làm nhiệm vụ Facebook
                account = menu.display_accounts("Facebook")
                if account:
                    auto.set_account(account, "Facebook")
                    
                    try:
                        max_jobs = int(input("\n👉 Số lượng nhiệm vụ muốn làm (mặc định 10): ") or "10")
                    except ValueError:
                        max_jobs = 10
                    
                    try:
                        delay = int(input("👉 Delay giữa các nhiệm vụ (giây, mặc định 5): ") or "5")
                        auto.set_delay(delay)
                    except ValueError:
                        auto.set_delay(5)
                    
                    auto.run_auto(max_jobs)
                    input("\nNhấn Enter để tiếp tục...")
            
            elif choice == "4":
                # Làm nhiệm vụ Instagram
                account = menu.display_accounts("Instagram")
                if account:
                    auto.set_account(account, "Instagram")
                    
                    try:
                        max_jobs = int(input("\n👉 Số lượng nhiệm vụ muốn làm (mặc định 10): ") or "10")
                    except ValueError:
                        max_jobs = 10
                    
                    try:
                        delay = int(input("👉 Delay giữa các nhiệm vụ (giây, mặc định 5): ") or "5")
                        auto.set_delay(delay)
                    except ValueError:
                        auto.set_delay(5)
                    
                    auto.run_auto(max_jobs)
                    input("\nNhấn Enter để tiếp tục...")
            
            else:
                print("\n❌ Lựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
            input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
