# tests/test_login_pytest.py
import pytest
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from django.contrib import messages

User = get_user_model()

# ==================== UNIT TESTS ====================
class TestAuthenticationLogic:
    """Test các hàm logic xác thực cơ bản"""
    
    def test_authenticate_valid_user(self, db, create_user):
        """Test hàm authenticate() với thông tin hợp lệ"""
        # Arrange: Tạo user
        user = create_user(username='john_doe')
        
        # Act: Xác thực
        auth_user = authenticate(username='john_doe', password='TestPass123!')
        
        # Assert
        assert auth_user is not None
        assert auth_user.username == 'john_doe'
        assert auth_user.is_authenticated
        assert auth_user.pk == user.pk
    
    @pytest.mark.parametrize('username,password,expected', [
        ('wrong_user', 'TestPass123!', None),  # Sai username
        ('john_doe', 'wrong_password', None),  # Sai password
        ('', 'TestPass123!', None),           # Username rỗng
        ('john_doe', '', None),               # Password rỗng
    ])
    def test_authenticate_invalid_credentials(self, db, create_user, 
                                             username, password, expected):
        """Test authenticate với các trường hợp thông tin sai"""
        # Arrange
        create_user(username='john_doe')
        
        # Act & Assert
        result = authenticate(username=username, password=password)
        assert result == expected
    
    def test_check_password(self, db, create_user):
        """Test kiểm tra password"""
        user = create_user(username='test_user')
        assert user.check_password('TestPass123!') is True
        assert user.check_password('WrongPass!') is False

# ==================== VIEW TESTS ====================
class TestLoginView:
    """Test view đăng nhập"""
    
    def test_login_page_loads_successfully(self, client, login_url):
        """Test trang login hiển thị đúng"""
        # Act
        response = client.get(login_url)
        
        # Assert
        assert response.status_code == 200
        assert 'form' in response.content.decode().lower()
        assert 'username' in response.content.decode().lower()
        assert 'password' in response.content.decode().lower()
        assert 'csrfmiddlewaretoken' in response.content.decode()
    
    def test_login_success_redirects_to_home(self, client, create_user, login_url):
        """Test đăng nhập thành công và redirect"""
        # Arrange
        user = create_user(username='success_user')
        
        # Act
        response = client.post(login_url, {
            'username': 'success_user',
            'password': 'TestPass123!'
        }, follow=True)
        
        # Assert - Check login
        assert response.status_code == 200
        assert response.wsgi_request.user.is_authenticated is True
        assert response.wsgi_request.user.username == 'success_user'
        
        # Check redirect (thay 'home' bằng URL thực tế)
        # assert response.redirect_chain[-1][0] == reverse('home')
        
        # Check session
        assert '_auth_user_id' in client.session
        assert int(client.session['_auth_user_id']) == user.pk
    
    def test_login_failure_stays_on_page(self, client, create_user, login_url):
        """Test đăng nhập thất bại hiển thị form với lỗi"""
        # Arrange
        create_user(username='fail_user')
        
        # Act
        response = client.post(login_url, {
            'username': 'fail_user',
            'password': 'WRONG_PASSWORD'
        })
        
        # Assert
        assert response.status_code == 200  # Vẫn ở trang login
        assert response.wsgi_request.user.is_authenticated is False
        
        # Kiểm tra có thông báo lỗi (tùy cách bạn hiển thị lỗi)
        content = response.content.decode().lower()
        assert any(word in content for word in ['error', 'invalid', 'sai', 'không'])
    
    @pytest.mark.parametrize('form_data', [
        {'username': '', 'password': 'TestPass123!'},      # Username rỗng
        {'username': 'testuser', 'password': ''},          # Password rỗng
        {'username': '', 'password': ''},                  # Cả hai rỗng
        {},                                                # Không gửi gì
    ])
    def test_login_empty_fields(self, client, login_url, form_data):
        """Test submit form với trường trống"""
        response = client.post(login_url, form_data)
        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated
    
    def test_login_already_logged_in_redirect(self, authenticated_client, login_url):
        """Test user đã login truy cập trang login sẽ redirect"""
        client, user = authenticated_client
        
        response = client.get(login_url)
        
        # Nếu đã login, thường redirect về trang chủ
        assert response.status_code in [302, 200]  # 302 redirect hoặc 200 nếu vẫn hiển thị
        if response.status_code == 302:
            # assert response.url == reverse('home')
            pass

# ==================== FORM TESTS ====================
class TestLoginForm:
    """Test Django form cho login"""
    
    def test_valid_form_data(self):
        """Test form với dữ liệu hợp lệ"""
        # Giả sử bạn có LoginForm
        # from .forms import LoginForm
        
        # form_data = {'username': 'testuser', 'password': 'TestPass123!'}
        # form = LoginForm(data=form_data)
        # assert form.is_valid() is True
        
        pytest.skip("Chưa implement LoginForm")  # Tạm bỏ qua nếu chưa có form
    
    def test_form_missing_fields(self):
        """Test form thiếu trường bắt buộc"""
        # from .forms import LoginForm
        
        # form_data = {'username': 'testuser'}  # Thiếu password
        # form = LoginForm(data=form_data)
        # assert form.is_valid() is False
        # assert 'password' in form.errors
        
        pytest.skip("Chưa implement LoginForm")

# ==================== EDGE CASES ====================
class TestLoginEdgeCases:
    """Test các trường hợp đặc biệt"""
    
    def test_login_case_sensitive(self, client, db, create_user, login_url):
        """Test phân biệt hoa thường (nếu hệ thống yêu cầu)"""
        # Tùy cấu hình Django, username mặc định KHÔNG phân biệt hoa thường
        user = create_user(username='CaseUser')
        
        # Test các biến thể
        test_cases = [
            ('CaseUser', True),    # Đúng
            ('caseuser', True),    # Thường - Django mặc định không phân biệt
            ('CASEUSER', True),    # Hoa - Django mặc định không phân biệt
        ]
        
        for username, should_login in test_cases:
            response = client.post(login_url, {
                'username': username,
                'password': 'TestPass123!'
            })
            
            if should_login:
                assert response.wsgi_request.user.is_authenticated
                # Đăng xuất để test tiếp
                client.logout()
            else:
                assert not response.wsgi_request.user.is_authenticated
    
    def test_login_rate_limiting(self, client, create_user, login_url):
        """Test giới hạn số lần thử login (nếu có)"""
        create_user(username='limited_user')
        
        # Thử login sai nhiều lần
        for i in range(5):
            response = client.post(login_url, {
                'username': 'limited_user',
                'password': f'wrong_pass_{i}'
            })
        
        # Sau nhiều lần thất bại, có thể bị block hoặc captcha
        # (Tùy implementation của bạn)
        response = client.post(login_url, {
            'username': 'limited_user',
            'password': 'TestPass123!'  # Password đúng
        })
        
        # Ghi chú: Test này cần custom implementation
        assert response.status_code in [200, 403, 429]
    
    def test_session_after_login(self, client, create_user, login_url):
        """Test session được tạo đúng sau login"""
        user = create_user(username='session_test')
        
        # Lấy session trước login
        session_before = dict(client.session)
        
        # Login
        response = client.post(login_url, {
            'username': 'session_test',
            'password': 'TestPass123!'
        })
        
        # Kiểm tra session sau login
        assert '_auth_user_id' in client.session
        assert '_auth_user_backend' in client.session
        assert '_auth_user_hash' in client.session
        
        # Session key nên thay đổi sau login (bảo mật)
        if 'session_key' in session_before:
            assert client.session.session_key != session_before['session_key']
    
    def test_remember_me_functionality(self, client, create_user, login_url):
        """Test tính năng 'Remember me' (nếu có)"""
        user = create_user(username='remember_user')
        
        # Gửi request với remember_me
        response = client.post(login_url, {
            'username': 'remember_user',
            'password': 'TestPass123!',
            'remember_me': 'on'  # Trường remember_me
        })
        
        # Kiểm tra session expiry
        # Mặc định: SESSION_COOKIE_AGE = 1209600 (2 tuần)
        # Với remember_me: có thể set expiry dài hơn
        
        # Lấy session expiry từ response cookies
        cookies = response.cookies.get('sessionid')
        if cookies:
            # Kiểm tra max-age hoặc expires
            pass
        
        pytest.mark.skip("Cần implementation remember_me")

# ==================== INTEGRATION TESTS ====================
class TestLoginIntegration:
    """Test tích hợp với các thành phần khác"""
    
    def test_login_then_access_protected_page(self, client, create_user, login_url):
        """Test sau khi login có thể truy cập trang cần authentication"""
        # Arrange
        user = create_user(username='protected_user')
        
        # Login
        client.post(login_url, {
            'username': 'protected_user',
            'password': 'TestPass123!'
        })
        
        # Truy cập trang protected (thay URL thực tế)
        # profile_url = reverse('profile')
        # response = client.get(profile_url)
        # assert response.status_code == 200
        
        pytest.mark.skip("Cần URL protected page")
    
    def test_logout_functionality(self, authenticated_client, login_url):
        """Test chức năng logout"""
        client, user = authenticated_client
        
        # Đảm bảo đã login
        assert user.is_authenticated
        
        # Logout
        logout_url = reverse('logout')  # Thay bằng URL logout thực tế
        response = client.get(logout_url)
        
        # Kiểm tra đã logout
        assert not response.wsgi_request.user.is_authenticated
        assert '_auth_user_id' not in client.session
        
        # Sau logout thường redirect về trang chủ hoặc login
        assert response.status_code in [302, 200]
    
    def test_user_inactive_cannot_login(self, db, client, login_url):
        """Test user bị inactive không thể login"""
        # Tạo user inactive
        user = User.objects.create_user(
            username='inactive_user',
            password='TestPass123!',
            is_active=False
        )
        
        # Thử login
        response = client.post(login_url, {
            'username': 'inactive_user',
            'password': 'TestPass123!'
        })
        
        # User inactive không thể login
        assert not response.wsgi_request.user.is_authenticated
        assert response.status_code == 200

# ==================== MOCK TESTS ====================
class TestLoginWithMocks:
    """Test sử dụng mock cho các phụ thuộc"""
    
    def test_external_auth_service_mock(self, mocker):
        """Test login với external service (mock)"""
        # Giả sử có hàm gọi API bên ngoài
        # mocker.patch('module.external_auth', return_value=True)
        
        # Thực hiện test với service đã được mock
        pass

# ==================== FIXTURE EXAMPLES ====================
@pytest.fixture
def admin_user(db):
    """Fixture tạo admin user"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='AdminPass123!'
    )

@pytest.fixture
def multiple_users(db):
    """Fixture tạo nhiều users"""
    users = []
    for i in range(3):
        user = User.objects.create_user(
            username=f'user_{i}',
            password=f'Pass_{i}!',
            email=f'user_{i}@example.com'
        )
        users.append(user)
    return users

def test_multiple_users_login(multiple_users, client, login_url):
    """Test login với nhiều users"""
    for i, user in enumerate(multiple_users):
        response = client.post(login_url, {
            'username': f'user_{i}',
            'password': f'Pass_{i}!'
        })
        assert response.wsgi_request.user.is_authenticated
        client.logout()  # Đăng xuất để test user tiếp theo