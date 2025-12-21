import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.test import Client

# --- Giả lập Hàm gửi mail background (Celery Task) ---
# Giả sử bạn có hàm tasks.send_email_task(user_id)
def mock_celery_task_send_email(user_email):
    print(f"Mocking sending email to {user_email} via Redis...")
    return "Task ID: 123-456"

# --- Giả lập Hàm xử lý Webhook từ PayPal ---
def process_paypal_webhook(payload):
    if payload.get('event_type') == 'PAYMENT.CAPTURE.COMPLETED':
        return True
    return False

class TestBackgroundServices:
    
    def test_celery_email_task_execution(self):
        """
        Kiểm thử: Đảm bảo tác vụ gửi mail được gọi (giả lập Celery)
        """
        # Patch vào nơi hàm được gọi
        with patch('core.test_services_mock.mock_celery_task_send_email') as mock_task:
            # Cấu hình mock
            mock_task.return_value = "Task Queued"
            
            # Thực thi logic (ví dụ: User đăng ký xong thì gọi hàm này)
            user_email = "newuser@test.com"
            result = mock_celery_task_send_email(user_email)
            
            # Assert
            assert result == "Task Queued"
            # Quan trọng: Kiểm tra hàm đã được gọi đúng tham số chưa
            mock_task.assert_called_once_with("newuser@test.com")

    def test_webhook_payment_confirmed(self):
        """
        Kiểm thử: Xử lý Webhook khi PayPal báo tiền đã về
        """
        fake_payload = {
            'id': 'WH-12345',
            'event_type': 'PAYMENT.CAPTURE.COMPLETED',
            'resource': {'amount': {'value': '100.00'}}
        }
        
        # Gọi hàm xử lý logic
        is_success = process_paypal_webhook(fake_payload)
        
        assert is_success is True, "Webhook phải trả về True khi thanh toán hoàn tất"

    def test_webhook_payment_denied(self):
        """
        Kiểm thử: Webhook báo lỗi hoặc sự kiện không quan trọng
        """
        fake_payload = {
            'event_type': 'PAYMENT.FAILED'
        }
        is_success = process_paypal_webhook(fake_payload)
        assert is_success is False