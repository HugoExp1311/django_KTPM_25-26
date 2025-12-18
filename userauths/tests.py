# from django.test import TestCase
# from django.contrib.auth import get_user_model

# class UserAuthTest(TestCase):
#     def setUp(self):
#         # Lấy model User hiện tại
#         User = get_user_model()
        
#         # 1. Tạo user
#         self.user = User.objects.create_user(
#             username='testuser', 
#             email='testuser@gmail.com', 
#             password='testpassword123'
#         )
        
#         # 2. Quan trọng: Kích hoạt user thủ công để chắc chắn không bị chặn
#         self.user.is_active = True
#         self.user.save()

#     def test_login_successful(self):
#         print("🟢 Đang test chức năng Đăng nhập...")
        
#         # 3. THỬ NGHIỆM: Đa số web bán hàng dùng EMAIL để login
#         # Chúng ta sẽ thử login bằng email trước
#         logged_in = self.client.login(email='testuser@gmail.com', password='testpassword123')
        
#         # Nếu login bằng email thất bại, thử login bằng username
#         if not logged_in:
#             print("   ⚠️ Login bằng Email thất bại, thử lại bằng Username...")
#             logged_in = self.client.login(username='testuser', password='testpassword123')

#         # Kiểm tra kết quả cuối cùng
#         self.assertTrue(logged_in, "❌ Lỗi: Không thể đăng nhập bằng cả Email lẫn Username")

#     def test_login_failed(self):
#         print("🟢 Đang test Đăng nhập sai pass...")
#         # Thử đăng nhập sai pass
#         logged_in = self.client.login(email='testuser@gmail.com', password='wrongpass')
#         self.assertFalse(logged_in)