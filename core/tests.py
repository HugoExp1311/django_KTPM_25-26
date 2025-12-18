from django.test import TestCase
from core.models import Product, Category
from django.contrib.auth import get_user_model

# --- PHẦN 1: UNIT TEST (Kiểm tra Lớp, Hàm, Logic Model) ---
class ProductUnitTests(TestCase):
    def setUp(self):
        # Chuẩn bị dữ liệu (Mock data)
        User = get_user_model()
        self.user = User.objects.create_user(username='test_unit', password='123')
        self.category = Category.objects.create(cid='cat01', title='Rau')
        
        # Test tạo đối tượng (Kiểm tra Lớp/Class)
        self.product = Product.objects.create(
            user=self.user,
            category=self.category,
            title="Cà rốt",
            price=20000
        )

    def test_model_str_function(self):
        print("🔵 [Unit Test] Kiểm tra hàm __str__ của Model Product...")
        # Kiểm tra xem hàm __str__ có trả về đúng title không (Kiểm tra Hàm)
        self.assertEqual(str(self.product), "Cà rốt")

    def test_model_database_connection(self):
        print("🔵 [Unit Test] Kiểm tra mối nối Database...")
        # Kiểm tra xem dữ liệu đã thực sự nằm trong DB chưa
        count = Product.objects.count()
        self.assertEqual(count, 1)

# --- PHẦN 2: INTEGRATION TEST (Kiểm tra Tích hợp URL - View - Template) ---
class CoreIntegrationTests(TestCase):
    def test_homepage_access(self):
        print("🟢 [Integration Test] Kiểm tra tích hợp Trang chủ...")
        # Giả lập client truy cập URL -> Gọi View -> Render Template
        response = self.client.get('/')
        
        # Kiểm tra kết nối tổng thể
        self.assertEqual(response.status_code, 200) # Kết nối thành công
        self.assertTemplateUsed(response, 'core/index.html') # Dùng đúng giao diện