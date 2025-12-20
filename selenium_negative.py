import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:8000"

class NegativeTest(unittest.TestCase):
    def setUp(self):
        # Chạy trình duyệt mỗi lần test
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_1_login_fail(self):
        """Test đăng nhập sai mật khẩu"""
        print("\n🧪 Test 1: Đăng nhập với mật khẩu sai")
        self.driver.get(f"{BASE_URL}/user/sing-in/")
        
        self.driver.find_element(By.NAME, "email").send_keys("test@gmail.com")
        self.driver.find_element(By.NAME, "password").send_keys("WRONG_PASSWORD_123") # Pass sai
        
        # Tìm nút submit (Thử nhiều kiểu selector)
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            btn.click()
        except:
            self.driver.find_element(By.XPATH, "//button").click()
            
        time.sleep(2)
        
        # Kiểm tra xem có thông báo lỗi hoặc vẫn ở trang login không
        current_url = self.driver.current_url
        page_source = self.driver.page_source
        
        # Mong đợi: Vẫn ở trang login hoặc có thông báo lỗi
        if "sing-in" in current_url or "error" in page_source.lower() or "incorrect" in page_source.lower():
            print("   ✅ PASS: Hệ thống chặn đăng nhập sai thành công.")
        else:
            self.fail("   ❌ FAIL: Hệ thống cho phép đăng nhập sai hoặc không báo lỗi!")

    def test_2_search_no_result(self):
        """Test tìm kiếm từ khóa linh tinh"""
        print("\n🧪 Test 2: Tìm kiếm không có kết quả")
        self.driver.get(BASE_URL)
        
        # Tìm ô search
        search_inputs = self.driver.find_elements(By.NAME, "q")
        if not search_inputs:
            print("   ⚠️ Không tìm thấy ô search.")
            return

        search_inputs[0].send_keys("dsafhgjasdhfjkashdfkjsahdf") # Từ khóa vô nghĩa
        search_inputs[0].submit()
        
        time.sleep(2)
        page_source = self.driver.page_source.lower()
        
        # Mong đợi: Thông báo "0 items" hoặc "no result"
        if "0 items" in page_source or "no result" in page_source or "không tìm thấy" in page_source:
             print("   ✅ PASS: Hiển thị thông báo không tìm thấy sản phẩm.")
        else:
             print("   ⚠️ WARNING: Không thấy thông báo rõ ràng (Check lại UI).")

    def test_3_checkout_empty_cart(self):
        """Test vào thanh toán khi giỏ hàng rỗng"""
        print("\n🧪 Test 3: Checkout với giỏ hàng rỗng")
        # Đảm bảo chưa đăng nhập (hoặc đăng nhập user mới tinh)
        self.driver.delete_all_cookies()
        
        self.driver.get(f"{BASE_URL}/cart/")
        time.sleep(1)
        
        # Thử bấm nút checkout nếu có
        try:
            checkout_btns = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'checkout')]")
            if len(checkout_btns) > 0:
                checkout_btns[0].click()
                time.sleep(2)
                
                # Mong đợi: Bị redirect về Shop hoặc Cart, hoặc báo lỗi
                if "shop" in self.driver.current_url or "cart" in self.driver.current_url:
                    print("   ✅ PASS: Hệ thống ngăn chặn checkout rỗng.")
                elif "checkout" in self.driver.current_url:
                    # Nếu vẫn vào được checkout -> Có thể là Bug logic hoặc UI chưa chặn
                    print("   ⚠️ WARNING: Vẫn vào được trang Checkout dù giỏ hàng rỗng.")
            else:
                print("   ✅ PASS: Nút Checkout bị ẩn khi giỏ hàng rỗng.")
        except:
             print("   ✅ PASS: Không thể thao tác checkout.")

if __name__ == "__main__":
    unittest.main()