import pytest
from decimal import Decimal
from unittest.mock import MagicMock

class TestCouponLogic:
    """
    Test logic giảm giá (sử dụng Mock vì chưa có Model Coupon thực tế)
    """
    
    def calculate_discount(self, order_total, coupon_code):
        # Đây là hàm giả lập logic backend (sau này bạn sẽ code thật)
        if coupon_code == "SAVE10":
            return order_total * Decimal('0.9') # Giảm 10%
        elif coupon_code == "MINUS50":
            return order_total - Decimal('50.00') # Giảm 50$
        elif coupon_code == "EXPIRED":
            raise ValueError("Coupon Expired")
        return order_total

    def test_apply_percentage_coupon(self):
        """Test mã giảm giá theo phần trăm"""
        original_price = Decimal('100.00')
        new_price = self.calculate_discount(original_price, "SAVE10")
        assert new_price == Decimal('90.00')

    def test_apply_fixed_amount_coupon(self):
        """Test mã giảm giá tiền mặt"""
        original_price = Decimal('100.00')
        new_price = self.calculate_discount(original_price, "MINUS50")
        assert new_price == Decimal('50.00')

    def test_expired_coupon(self):
        """Test mã hết hạn phải báo lỗi"""
        with pytest.raises(ValueError) as excinfo:
            self.calculate_discount(Decimal('100.00'), "EXPIRED")
        assert "Coupon Expired" in str(excinfo.value)