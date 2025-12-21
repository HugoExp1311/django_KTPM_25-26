import os
import django

# 1. Cấu hình môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Category, Product, Vendor

def initialize_data():
    print("🚀 Đang khởi tạo dữ liệu mẫu cho Selenium...")
    User = get_user_model()

    # --- 1. TẠO USER TEST ---
    email = "test@gmail.com"
    password = "123"
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': 'SeleniumUser'}
    )
    
    user.set_password(password)
    user.save()
    print(f"   ✅ User: Đã xử lý user '{email}'")

    # --- 2. TẠO CATEGORY ---
    # Chỉ tìm theo cid (khóa duy nhất)
    cat, _ = Category.objects.get_or_create(
        cid="phone01", 
        defaults={'title': "Điện thoại"}
    )

    # --- 3. TẠO VENDOR (SỬA LỖI Ở ĐÂY) ---
    # Chỉ tìm theo vid, nếu không có mới tạo với các thông tin trong defaults
    ven, _ = Vendor.objects.get_or_create(
        vid="apple01", 
        defaults={
            'title': "Apple Store", 
            'user': user,
            'image': 'vendor.jpg'
        }
    )

    # --- 4. TẠO PRODUCT ---
    # Chỉ tìm theo pid, tránh lỗi trùng lặp
    prod, p_created = Product.objects.get_or_create(
        pid="iphone15",
        defaults={
            'title': "iPhone 15 Pro Max",
            'user': user,
            'category': cat,
            'vendor': ven,
            'price': 1000.00,
            'old_price': 1200.00,
            'stock_count': 10,
            'product_status': 'published',
            'status': True,
            'in_stock': True,
            'image': 'product.jpg' 
        }
    )
    
    status_msg = "Tạo mới" if p_created else "Đã có sẵn"
    print(f"   ✅ Product: {status_msg} sản phẩm '{prod.title}'.")
    
    print("\n🏁 XONG! Database đã sẵn sàng.")

if __name__ == "__main__":
    initialize_data()