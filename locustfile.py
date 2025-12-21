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

    @task(3)
    def view_homepage(self):
        """Mô phỏng xem trang chủ (tần suất cao)"""
        self.client.get("/")

    @task(2)
    def view_shop(self):
        """Mô phỏng xem trang shop"""
        # Sửa đường dẫn '/shop/' thành đường dẫn thật của bạn nếu khác
        self.client.get("/products/") 

    @task(1)
    def view_product_detail(self):
        """Mô phỏng xem chi tiết 1 sản phẩm cụ thể (cần pid thật)"""
        # Thay 'post12345' bằng 1 pid có thật trong DB của bạn để test chuẩn
        self.client.get("/product/42fd2f1fcb/", name="/product/[pid]")