from django.test import TestCase
from django.contrib.auth import get_user_model

class LoginTests(TestCase):
    def setUp(self):
        # Tạo user test
        self.email = "test@example.com"
        self.password = "pass1234"
        User = get_user_model()
        User.objects.create_user(email=self.email, password=self.password)

    def test_login_page_loads(self):
        """Trang login trả về 200 OK"""
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        """Test người dùng có thể đăng nhập thành công"""
        login_data = {
            "email": self.email,
            "password": self.password
        }

        response = self.client.post("/login/", login_data, follow=True)

        # Kiểm tra login thành công → response code 200 + redirect tới dashboard/home
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
