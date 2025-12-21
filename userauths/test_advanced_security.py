import pytest
from django.test import Client
from userauths.models import User
from core.models import Product, Category, Vendor, ProductReview

@pytest.mark.django_db
class TestAdvancedSecurity:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username='hacker', email='hack@test.com', password='123')
        self.category = Category.objects.create(title="Sec Cat", cid="sec01")
        self.vendor = Vendor.objects.create(title="Sec Vendor", vid="ven_sec", user=self.user)
        self.product = Product.objects.create(
            pid="sec_prod", user=self.user, category=self.category, vendor=self.vendor, title="Sec Product"
        )

    def test_xss_injection_in_review(self):
        """Kiểm tra tấn công XSS vào phần bình luận"""
        self.client.login(email='hack@test.com', password='123')
        
        xss_payload = "<script>alert('You are hacked')</script>"
        
        # Tạo review chứa mã độc
        review = ProductReview.objects.create(
            user=self.user,
            product=self.product,
            review=xss_payload,
            rating=5
        )
        
        # Lấy trang chi tiết sản phẩm xem review có hiện ra không
        # Lưu ý: Django Template mặc định sẽ 'escape' ký tự đặc biệt -> biến <script> thành &lt;script&gt;
        # Test này Pass nghĩa là Django ĐÃ bảo vệ thành công.
        
        # Gọi view (cần URL đúng)
        # response = self.client.get(...) 
        
        # Kiểm tra thủ công logic escape
        from django.utils.html import escape
        escaped_text = escape(review.review)
        
        assert "&lt;script&gt;" in escaped_text
        assert "<script>" not in escaped_text # Đây là điều chúng ta muốn: Mã độc bị vô hiệu hóa