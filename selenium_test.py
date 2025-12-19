import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_browser_test():
    print("🚀 Bắt đầu kiểm thử tự động trên trình duyệt Chrome...")
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        base_url = "http://127.0.0.1:8000"
        
        # --- SỬA LỖI 1: Cập nhật đúng đường dẫn (sing-in) ---
        # Dựa trên file urls.py của bạn: path("sing-in/", ...)
        login_url = f"{base_url}/user/sing-in/" 
        
        print(f"🔵 Truy cập trang đăng nhập: {login_url}")
        driver.get(login_url)
        time.sleep(2) 

        # Kiểm tra xem có đúng là trang login không
        if "404" in driver.title:
            print("❌ Lỗi: Trang web trả về 404. Hãy kiểm tra lại URL trong urls.py")
            return

        # --- SỬA LỖI 2: Thử tìm cả 'email' và 'username' ---
        try:
            print("   Đang tìm ô nhập email/username...")
            try:
                email_input = driver.find_element(By.NAME, "email")
            except:
                # Nếu không tìm thấy name="email", thử tìm name="username" (Mặc định của Django)
                email_input = driver.find_element(By.NAME, "username")
                print("   (Đã tìm thấy input bằng name='username')")

            password_input = driver.find_element(By.NAME, "password")
            
            # Tìm nút submit (Thử nhiều cách để chắc chắn tìm thấy)
            try:
                submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            except:
                submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Log')]")

            # Điền thông tin (Dùng user bạn đã tạo trong bước Database Test trước đó)
            email_input.send_keys("test@gmail.com") 
            password_input.send_keys("123") 
            
            print("   Đã điền thông tin, đang click đăng nhập...")
            time.sleep(1)
            submit_btn.click()
            
            time.sleep(3)
            print(f"✅ Đăng nhập thành công! (URL hiện tại: {driver.current_url})")
            
        except Exception as e:
            print(f"❌ Không tìm thấy phần tử trên trang web: {e}")
            print("👉 Hãy mở file 'templates/userauths/sing-in.html' để xem thuộc tính name='' của ô input là gì.")

    except Exception as e:
        print(f"❌ Có lỗi hệ thống: {e}")
        
    finally:
        print("🛑 Đóng trình duyệt sau 5 giây...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    run_browser_test()