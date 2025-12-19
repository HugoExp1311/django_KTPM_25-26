from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Thời gian nghỉ ngẫu nhiên giữa các hành động (từ 1 đến 5 giây)
    # Giúp mô phỏng hành vi người thật đọc nội dung trước khi click tiếp
    wait_time = between(1, 5)

    @task(3)
    def view_homepage(self):
        """Giả lập vào trang chủ (xác suất cao nhất)"""
        self.client.get("/")

    @task(1)
    def view_login_page(self):
        """Giả lập vào trang đăng nhập"""
        # Lưu ý: URL này phải đúng với urls.py của bạn (đã sửa thành sing-in)
        self.client.get("/user/sing-in/")

    @task(2)
    def browse_products(self):
        """Giả lập xem danh sách sản phẩm"""
        # Kiểm tra file urls.py xem đường dẫn shop/product là gì. 
        # Tạm thời mình để trang chủ hoặc bạn thay bằng đường dẫn thật nếu có.
        self.client.get("/") 

    @task(1)
    def view_cart(self):
        """Giả lập vào giỏ hàng"""
        self.client.get("/cart/")