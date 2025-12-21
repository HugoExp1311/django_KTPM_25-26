from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from userauths.models import User
from django.contrib.messages import get_messages
import pytest

@pytest.mark.smoke  
@pytest.mark.regression
class AuthTestCase(TestCase):
    """
    Test toàn bộ chức năng:
    - Register (sing-up)
    - Login (sing-in)
    - Login sai email
    - Login sai password
    """

    def setUp(self):
        # User dùng cho test login
        self.email = "test@example.com"
        self.password = "Pass12345"

        self.user = User.objects.create_user(
            username="testuser",
            email=self.email,
            password=self.password
        )

    # =====================================================
    # REGISTER TESTS
    # =====================================================

    def test_register_with_valid_data(self):
        """
        Đăng ký hợp lệ:
        - User được tạo
        - User được tự động login
        - Redirect về trang index
        """
        print("🟢 [Integration] Đang test đăng ký với dữ liệu hợp lệ...")
        response = self.client.post(
            reverse("userauths:sing-up"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
            follow=True
        )

        self.assertTrue(
            User.objects.filter(email="newuser@example.com").exists()
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_register_password_mismatch(self):
        """
        Đăng ký sai (password không khớp):
        - User KHÔNG được tạo
        """
        print("🟢 [Integration] Đang test đăng ký với password không khớp...")
        response = self.client.post(
            reverse("userauths:sing-up"),
            {
                "username": "baduser",
                "email": "bad@example.com",
                "password1": "StrongPass123",
                "password2": "WrongPass",
            }
        )

        self.assertFalse(
            User.objects.filter(email="bad@example.com").exists()
        )

    # =====================================================
    # LOGIN TESTS
    # =====================================================

    def test_login_with_valid_credentials(self):
        """
        Login đúng email + password:
        - User được authenticate
        - User được login
        """
        print("🟢 [Integration] Đang test đăng nhập với thông tin hợp lệ...")
        response = self.client.post(
            reverse("userauths:sing-in"),
            {
                "email": self.email,
                "password": self.password,
            },
            follow=True
        )

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_email(self):
        """
        Login sai email:
        - authenticate trả None
        """
        print("🟢 [Integration] Đang test đăng nhập với email không tồn tại...")
        user = authenticate(
            email="wrong@example.com",
            password=self.password
        )
        self.assertIsNone(user)

    def test_login_with_invalid_password(self):
        """
        Login sai password:
        - authenticate trả None
        """
        print("🟢 [Integration] Đang test đăng nhập với password sai...")
        user = authenticate(
            email=self.email,
            password="WrongPassword"
        )
        self.assertIsNone(user)

#=====================================================
#Change


    def test_account_username_with_space(self):
        self.client.force_login(self.user)

        self.client.post(
            reverse("userauths:account"),
            {"username": "abc def"},
            follow=True
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "abcdef")


        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "abcdef")

   

    # def test_account_username_too_short(self):
    #     self.client.login(email="test@example.com", password="pass1234")

    #     response = self.client.post(
    #         reverse("userauths:account"),
    #         {
    #             "username": "ab",  # quá ngắn
    #         },
    #         follow=True
    #     )

    #     messages = list(get_messages(response.wsgi_request))
    #     self.assertTrue(
    #         any("between 3 and 12 characters" in str(message) for message in messages),
    #         f"Messages found: {[str(m) for m in messages]}"        
    #     )

    def test_account_username_too_short(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("userauths:account"),
            {"username": "ab"},
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("between 3 and 12" in str(m) for m in messages),
            f"Messages found: {[str(m) for m in messages]}"
        )



    def test_account_username_duplicate(self):
        User.objects.create_user(
            email="other@example.com",
            username="duplicate",
            password="pass1234"
        )

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("userauths:account"),
            {"username": "duplicate"},
            follow=True
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("already taken" in str(m) for m in messages),
            f"Messages found: {[str(m) for m in messages]}"
        )


