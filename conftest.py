# conftest.py
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

User = get_user_model()

@pytest.fixture
def client():
    """Fixture cung cấp Django test client"""
    return Client()

@pytest.fixture
def create_user(db):
    """Fixture tạo user test"""
    def make_user(**kwargs):
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return make_user

@pytest.fixture
def authenticated_client(client, create_user):
    """Fixture tạo client đã đăng nhập"""
    user = create_user(username='auth_user')
    client.force_login(user)
    return client, user

@pytest.fixture
def login_url():
    """Fixture trả về URL login"""
    return reverse('login')  # Thay bằng tên URL thực tế