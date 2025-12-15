# tests/test_auth.py
from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

User = get_user_model()

class LoginTestCase(TestCase):
    """
    Test case cho chức năng đăng nhập.
    """

    def setUp(self):
        """
        Thiết lập dữ liệu test chung.
        """
        # Tạo một user để test đăng nhập
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='test@example.com'
        )

    # def test_login_with_valid_credentials(self):
    #     """
    #     Test đăng nhập với thông tin hợp lệ.
    #     """
    #     # Gọi hàm authenticate
    #     user = authenticate(username=self.username, password=self.password)
        
    #     # Kiểm tra xác thực thành công
    #     self.assertIsNotNone(user)
    #     self.assertEqual(user.username, self.username)

    #     # Có thể test view login nếu cần
    #     login_url = reverse('sing-in')  # Thay 'login' bằng tên URL pattern của bạn
    #     response = self.client.post(login_url, {
    #         'username': self.username,
    #         'password': self.password
    #     })
        
    #     # Kiểm tra chuyển hướng sau khi login thành công (giả sử redirect tới 'home')
    #     self.assertRedirects(response, reverse('core:index'))
def test_login_with_valid_credentials(self):
    response = self.client.post(
        reverse("userauths:sing-in"),
        {
            "email": "test@example.com",
            "password": "pass1234"
        },
        follow=True
    )

    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_invalid_username(self):
        """
        Test đăng nhập với username không tồn tại.
        """
        user = authenticate(username='wronguser', password=self.password)
        self.assertIsNone(user)

    def test_login_with_invalid_password(self):
        """
        Test đăng nhập với password sai.
        """
        user = authenticate(username=self.username, password='wrongpass')
        self.assertIsNone(user)

    def test_login_view_returns_correct_template(self):
        """
        Test rằng trang login sử dụng đúng template.
        """
        response = self.client.get(reverse('userauths:sing-in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauths/sing-in.html')  # Thay bằng template thực tế

    def test_login_required_redirect_for_anonymous_user(self):
        """
        Test rằng một view yêu cầu đăng nhập sẽ chuyển hướng người dùng chưa đăng nhập.
        """
        # Giả sử 'profile' là view cần đăng nhập
        profile_url = reverse('userauths:account')
        response = self.client.get(profile_url)
        
        # Kiểm tra redirect tới trang login
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('userauths:sing-in'), response.url)