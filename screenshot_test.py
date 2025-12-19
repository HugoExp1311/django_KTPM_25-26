import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Cấu hình các kích thước màn hình cần test
Viewports = {
    "Mobile_iPhoneX": (375, 812),
    "Tablet_iPad": (768, 1024),
    "Desktop_HD": (1366, 768),
    "Desktop_FullHD": (1920, 1080)
}

# Các trang cần chụp ảnh (Kiểm tra lại URL của bạn)
Target_URLs = [
    ("/", "Home"),
    ("/user/sing-in/", "Login"),  # Lưu ý: URL của bạn là 'sing-in'
    ("/user/sing-up/", "Signup"), # URL 'sing-up'
    # ("/shop/", "Shop"), # Bỏ comment nếu có trang này
]

def capture_screenshots():
    # Tạo thư mục lưu ảnh
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        
    print("📸 Bắt đầu quy trình chụp ảnh giao diện...")
    
    # Chạy Chrome chế độ ẩn (Headless) để nhanh hơn
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        base_url = "http://127.0.0.1:8000"
        
        for path, name in Target_URLs:
            full_url = base_url + path
            print(f"\n🔵 Đang xử lý trang: {name} ({full_url})")
            driver.get(full_url)
            time.sleep(1) # Đợi trang load
            
            for device, (width, height) in Viewports.items():
                # Đổi kích thước trình duyệt
                driver.set_window_size(width, height)
                
                # Cuộn xuống cuối trang để load hết nội dung (nếu có lazy load)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(0.5)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.5)
                
                # Đặt tên file: screenshots/Home_Mobile_iPhoneX.png
                file_name = f"screenshots/{name}_{device}.png"
                driver.save_screenshot(file_name)
                print(f"   ✅ Đã chụp: {device} ({width}x{height})")

    except Exception as e:
        print(f"❌ Có lỗi: {e}")
    finally:
        driver.quit()
        print("\n🏁 Hoàn tất! Hãy mở thư mục 'screenshots' để kiểm tra.")

if __name__ == "__main__":
    capture_screenshots()