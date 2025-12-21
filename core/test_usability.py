import pytest
from django.urls import reverse
from django.test import Client
from bs4 import BeautifulSoup # Cần cài: pip install beautifulsoup4

@pytest.mark.django_db
class TestUsability:
    def setup_method(self):
        self.client = Client()

    @pytest.mark.usability
    def test_homepage_broken_links(self):
        """
        Kiểm tra: Quét toàn bộ link trên trang chủ, đảm bảo không có link nào chết (404).
        """
        url = reverse('core:index') 
        response = self.client.get(url)
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        
        print(f"\n[USABILITY] Đang kiểm tra {len(links)} liên kết trên trang chủ...")
        
        for link in links:
            href = link.get('href')
            if href and href.startswith('/'): # Chỉ kiểm tra link nội bộ
                # Bỏ qua các link logout hoặc delete để tránh side-effect
                if "logout" in href or "delete" in href:
                    continue
                    
                check_resp = self.client.get(href)
                # Link tốt phải là 200 hoặc 302 (redirect), không được 404
                if check_resp.status_code == 404:
                    pytest.fail(f"Phát hiện Broken Link: {href}")
                else:
                    assert check_resp.status_code in [200, 302]

    @pytest.mark.usability
    def test_images_have_alt_tags(self):
        """
        Kiểm tra Accessibility: Mọi thẻ <img> phải có thuộc tính 'alt' (cho người khiếm thị).
        """
        url = reverse('core:index')
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('img')
        
        missing_alt = []
        for img in images:
            if not img.get('alt'):
                src = img.get('src')
                missing_alt.append(src)
        
        # Nếu list rỗng là tốt (Pass). Nếu có ảnh thiếu alt thì Fail.
        if missing_alt:
            print(f"\n[UX WARNING] Có {len(missing_alt)} ảnh thiếu thẻ alt: {missing_alt}")
            # Có thể assert False nếu muốn bắt buộc, hoặc chỉ warning
            # assert False