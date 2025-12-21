import pytest
from django.urls import reverse
from core.models import Category, Product, User

@pytest.mark.smoke
@pytest.mark.django_db
class TestCoreViews:
    def setup_method(self):
        self.user = User.objects.create_user(username='viewtest', password='123')
        self.category = Category.objects.create(title="View Cat", cid="viewcat")
        self.product = Product.objects.create(
            user=self.user, 
            category=self.category, 
            title="View Prod",
            price=10.00,
            stock_count=5
        )

    def test_product_detail_view(self, client):
        """Kiểm tra trang chi tiết sản phẩm"""
        url = reverse('core:products-detail', args=[self.product.pid])
        response = client.get(url)
        assert response.status_code == 200
        assert "View Prod" in str(response.content)

    def test_category_product_list_view(self, client):
        """Kiểm tra trang danh sách sản phẩm theo danh mục"""
        url = reverse('core:category-product-list', args=[self.category.cid])
        response = client.get(url)
        assert response.status_code == 200
        assert "View Cat" in str(response.content)

    def test_search_view(self, client):
        """Kiểm tra chức năng tìm kiếm"""
        url = reverse('core:search')
        response = client.get(url, {'q': 'View Prod'})
        assert response.status_code == 200
        assert "View Prod" in str(response.content)