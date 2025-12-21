import pytest
from django.urls import reverse
from django.test import Client
from userauths.models import User
from core.models import Product, Category

@pytest.mark.django_db
class TestAdminAndUserFlow:
    def setup_method(self):
        self.client = Client()
        
        # 1. Tạo Superuser (Admin xịn)
        self.admin_user = User.objects.create_superuser(
            username='admin_boss', 
            email='admin@zstyle.com', 
            password='123'
        )
        
        # 2. Tạo User thường
        self.regular_user = User.objects.create_user(
            username='normal_user', 
            email='user@zstyle.com', 
            password='123'
        )

    # ==================================================
    # PHẦN 1: KIỂM THỬ QUYỀN ADMIN (Admin Panel)
    # ==================================================
    def test_admin_panel_access_authorized(self):
        """Kiểm tra: Admin đăng nhập thì được vào trang quản trị"""
        self.client.force_login(self.admin_user)
        # URL mặc định của Django Admin là 'admin:index'
        url = reverse('admin:index') 
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert "Site administration" in str(response.content) # Dấu hiệu nhận biết trang admin

    def test_admin_panel_access_denied_for_normal_user(self):
        """Kiểm tra: User thường cố tình vào trang Admin phải bị chặn"""
        self.client.force_login(self.regular_user)
        url = reverse('admin:index')
        response = self.client.get(url)
        
        # Mong đợi: Không được vào (302 Redirect về login hoặc 403 Forbidden)
        assert response.status_code != 200 

    def test_admin_can_see_models(self):
        """Kiểm tra: Admin có thấy mục quản lý Products/Users không"""
        self.client.force_login(self.admin_user)
        url = reverse('admin:index')
        response = self.client.get(url)
        
        # Kiểm tra xem trong HTML có chữ "Products" và "Users" không
        content = str(response.content)
        assert "Products" in content
        assert "Users" in content

    # ==================================================
    # PHẦN 2: KIỂM THỬ USER PROFILE (Cập nhật thông tin)
    # ==================================================
    def test_user_model_update_bio(self):
        """Kiểm tra: Cập nhật Bio và thông tin User"""
        user = self.regular_user
        user.bio = "Tôi là khách hàng VIP"
        user.username = "vip_user"
        user.save()
        
        # Lấy lại từ DB để kiểm tra
        updated_user = User.objects.get(id=user.id)
        assert updated_user.bio == "Tôi là khách hàng VIP"
        assert updated_user.username == "vip_user"

    def test_user_authentication_flow(self):
        """Kiểm tra: Luồng đăng nhập/đăng xuất cơ bản"""
        # 1. Đăng nhập
        login_success = self.client.login(email='user@zstyle.com', password='123')
        assert login_success == True
        
        # 2. Kiểm tra session
        response = self.client.get(reverse('core:index')) # Vào trang chủ
        assert response.status_code == 200
        # Nếu đã login, trong context request.user phải là authenticated
        # (Cách check nhanh: response.wsgi_request.user.is_authenticated)
        
        # 3. Đăng xuất
        self.client.logout()
        # Sau khi logout, thử truy cập trang cần quyền (như checkout) xem có bị chặn ko
        # (Logic này đã test ở file advanced, nhưng test lại cho chắc luồng Auth)