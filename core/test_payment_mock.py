import pytest
from unittest.mock import patch, MagicMock

# Giả sử bạn có hàm process_payment trong core/utils.py hoặc views.py
# Nếu chưa có, test này đóng vai trò minh họa logic

def mock_process_payment(amount, currency='USD'):
    """Hàm giả lập xử lý thanh toán của Stripe/PayPal"""
    if amount <= 0:
        return False, "Invalid amount"
    return True, "Transaction ID: 12345XYZ"

class TestPaymentGateway:
    
    def test_payment_success_scenario(self):
        """Giả lập thanh toán thành công"""
        # Sử dụng Mock để thay thế việc gọi API thật
        with patch('core.test_payment_mock.mock_process_payment') as mock_payment:
            # Cấu hình cho Mock: Luôn trả về Thành công
            mock_payment.return_value = (True, "Success")
            
            # Gọi hàm (giả)
            result, message = mock_process_payment(100)
            
            assert result is True
            assert message == "Success"
            # Kiểm tra xem hàm đã được gọi đúng 1 lần chưa
            mock_payment.assert_called_once_with(100)

    def test_payment_failure_scenario(self):
        """Giả lập thanh toán thất bại (Thẻ hết tiền)"""
        with patch('core.test_payment_mock.mock_process_payment') as mock_payment:
            # Cấu hình Mock: Trả về thất bại
            mock_payment.return_value = (False, "Insufficient Funds")
            
            result, message = mock_process_payment(100)
            assert result is False
            assert message == "Insufficient Funds"