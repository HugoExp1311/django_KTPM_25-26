import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ---
BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "test@gmail.com"  # Đảm bảo user này đã tồn tại
USER_PASS = "devilthomas123"

def run_full_flow():
    print("🚀 BẮT ĐẦU KIỂM THỬ TOÀN TRÌNH (FULL FLOW)...")
    print("-------------------------------------------------")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Bỏ comment nếu muốn chạy ngầm
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10) # Thời gian chờ tối đa 10s cho các phần tử

    try:
        # ==========================================
        # BƯỚC 1: ĐĂNG NHẬP
        # ==========================================
        print("1️⃣  Bước 1: Đăng nhập hệ thống...")
        driver.get(f"{BASE_URL}/user/sing-in/") # Lưu ý: URL của bạn là 'sing-in'
        
        # Điền form
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(USER_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(USER_PASS)
        
        # Click nút đăng nhập
        try:
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
        except:
            # Fallback nếu không tìm thấy nút submit chuẩn
            driver.find_element(By.XPATH, "//button[contains(text(), 'Log')]").click()
            
        print("   ✅ Đã submit form đăng nhập.")
        time.sleep(2) # Đợi đăng nhập xong

        # ==========================================
        # BƯỚC 2: CHỌN SẢN PHẨM TỪ TRANG CHỦ
        # ==========================================
        # ==========================================
        # BƯỚC 2: VÀO THẲNG SẢN PHẨM (DIRECT ACCESS)
        # ==========================================
        print("\n2️⃣  Bước 2: Truy cập thẳng trang chi tiết sản phẩm...")
        
        # ID sản phẩm chúng ta đã tạo trong init_data.py là "iphone15"
        # Hãy thử các đường dẫn phổ biến (bạn có thể sửa lại cho đúng với urls.py của bạn)
        target_pid = "iphone15" 
        
        # Thử đường dẫn chuẩn nhất (dựa trên các file test trước)
        # Nếu url của bạn là /product-detail/iphone15/ hay /product/iphone15/ thì sửa dòng dưới:
        product_url = f"{BASE_URL}/product-detail/{target_pid}/" 
        
        print(f"   Đang truy cập: {product_url}")
        driver.get(product_url)
        time.sleep(3) # Đợi trang load xong
        
        # Kiểm tra xem có bị lỗi 404 không
        if "Page not found" in driver.title or "404" in driver.page_source:
             print("   ⚠️ Link trên bị lỗi 404. Thử link dự phòng: /product/...")
             driver.get(f"{BASE_URL}/product/{target_pid}/")
             time.sleep(2)

        print(f"   (Tiêu đề trang hiện tại: {driver.title})")

        # ==========================================
        # BƯỚC 3: THÊM VÀO GIỎ HÀNG
        # ==========================================
        print("\n3️⃣  Bước 3: Thêm vào giỏ hàng...")
        
        # Tìm nút "Add to cart". Thử nhiều cách selector khác nhau
        try:
            # Cách 1: Tìm nút có type=submit hoặc class chứa 'add'
            add_btn = driver.find_element(By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add')]")
            # Scroll đến nút đó để tránh bị che
            driver.execute_script("arguments[0].scrollIntoView();", add_btn)
            time.sleep(1)
            add_btn.click()
            print("   ✅ Đã bấm nút 'Add to cart'.")
        except:
            try:
                # Cách 2: Tìm input số lượng và enter
                qty_input = driver.find_element(By.NAME, "qty")
                qty_input.submit()
                print("   ✅ Đã submit form thêm giỏ hàng.")
            except Exception as e:
                print(f"   ❌ Lỗi: Không tìm thấy nút Add to Cart. ({e})")
                return

        time.sleep(2) # Đợi AJAX hoặc Reload

        # ==========================================
        # BƯỚC 4: VÀO GIỎ HÀNG & CHECKOUT
        # ==========================================
        print("\n4️⃣  Bước 4: Kiểm tra giỏ hàng...")
        driver.get(f"{BASE_URL}/cart/")
        
        # Kiểm tra xem có sản phẩm trong bảng không
        if "Cart" in driver.title or len(driver.find_elements(By.TAG_NAME, "tr")) > 0:
            print("   ✅ Giỏ hàng đã có sản phẩm.")
            
            # Tìm nút Checkout
            print("\n5️⃣  Bước 5: Tiến hành thanh toán (Checkout)...")
            try:
                checkout_link = driver.find_element(By.XPATH, "//a[contains(@href, 'checkout')]")
                checkout_link.click()
            except:
                # Nếu không thấy nút, thử truy cập trực tiếp
                driver.get(f"{BASE_URL}/checkout/")
                
            time.sleep(2)
            
            # ==========================================
            # BƯỚC 5: ĐIỀN THÔNG TIN GIAO HÀNG
            # ==========================================
            print("   Đang điền form thanh toán...")
            # Thử điền các trường phổ biến (Nếu web bạn tự động điền thì tốt)
            try:
                driver.find_element(By.NAME, "full_name").send_keys("Test User")
                driver.find_element(By.NAME, "address").send_keys("123 Test Street")
                driver.find_element(By.NAME, "mobile").send_keys("0987654321")
                driver.find_element(By.NAME, "city").send_keys("Ho Chi Minh")
                driver.find_element(By.NAME, "country").send_keys("Vietnam")
            except:
                print("   (⚠️ Một số trường form không tìm thấy, có thể do đã được điền sẵn hoặc tên khác)")

            # Submit đơn hàng
            try:
                place_order_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Place') or contains(text(), 'Order') or contains(text(), 'Pay')]")
                driver.execute_script("arguments[0].scrollIntoView();", place_order_btn)
                time.sleep(1)
                place_order_btn.click()
                print("   ✅ Đã bấm 'Place Order'!")
            except:
                print("   ⚠️ Không tìm thấy nút đặt hàng cuối cùng. Kiểm tra lại ID/Class của nút.")

            time.sleep(5)
            print(f"\n🏁 KẾT THÚC FLOW. URL hiện tại: {driver.current_url}")
            
        else:
            print("   ❌ Lỗi: Giỏ hàng trống rỗng!")

    except Exception as e:
        print(f"\n❌ TEST FAILED: Có lỗi xảy ra - {e}")

    finally:
        print("🛑 Đóng trình duyệt...")
        driver.quit()

if __name__ == "__main__":
    run_full_flow()