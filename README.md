
DJANGO E-COMMERCE PROJECT

📦 Project: django-ecommerce
🧩 Framework: Django 4.2.7
🐍 Python: 3.9+
💾 Database: SQLite (default)

-----------------------------------------
PHASE DIVISION (for Unit Testing)
-----------------------------------------

🔹 PHASE 1 - Basic Authentication & Homepage
-----------------------------------------
Includes:  
│  
├── userauths/  
│   ├── views.py  
│   ├── urls.py  
│   ├── models.py  
│   ├── forms.py  
│   └── templates/userauths/  
│       ├── login.html  
│       ├── register.html  
│       └── profile.html  
│
├── templates/  
│   ├── base.html  
│   └── index.html     ← Homepage  
│
├── ecomproject/  
│   ├── settings.py  
│   ├── urls.py   
│   └── wsgi.py  
│
├── manage.py  
├── requirements.txt  
└── db.sqlite3 (auto-generated after migrate)  

Test Scope:
✅ Login / Register pages  
✅ Homepage loading  
✅ Base layout rendering  

-----------------------------------------
🔹 PHASE 2 - Product Display & Search
-----------------------------------------
Includes:  
│  
├── core/  
│   ├── models.py  
│   ├── views.py  
│   ├── urls.py  
│   └── templates/core/  
│       ├── product_list.html   
│       ├── search.html  
│       └── filter.html  
│
├── static/  
│   ├── css/  
│   ├── js/  
│   └── images/  
│
└── + all files from Phase 1

Test Scope:
✅ Product list   
✅ Search & filter logic  

-----------------------------------------
🔹 PHASE 3 - Product Details
-----------------------------------------
Includes:  
│  
├── cart/  
│   ├── models.py  
│   ├── views.py  
│   ├── urls.py  
│   └── templates/cart/  
│       ├── product-details.html  
│       ├── vendors-details.html  
│
└── + all files from Phase 1 & 2  

Test Scope:
✅ View product details
✅ View vendors details
 

-----------------------------------------
🔹 PHASE 4 - Admin Dashboard & Management, Add to cart
-----------------------------------------
Includes:  
│  
├── dashboard/  
│   ├── views.py  
│   ├── urls.py  
│   └── templates/dashboard/  
│       ├── admin_home.html  
│       ├── manage_users.html  
│       └── manage_products.html  
│  
└── + all files from Phase 1, 2, 3  
  
Test Scope:
✅ Add to cart / remove from cart  
✅ View cart summary  
✅ Checkout page  
✅ Admin login  
✅ Manage users/products/orders  
✅ Dashboard analytics  


## Features📚

- User Authentication
- User Profile
- Shopping Cart
- Wishlist
- Product Discount
- Products / Vendors Page
- Product detail / Vendor detail Page
- Tags for Product and Blog
- Category list Page
- Improved Admin Panel
- Product Reviews
- Blog post Comments
- Products Filter
- Search Functionality
- Related Products
- Related Blog posts

-----------------------------------------
🧰 Installation Guide
-----------------------------------------


1. Clone and change to the directory:

```
git clone https://github.com/kolosochok/django-ecommerce
cd django-ecommerce
```

2. Create and activate a virtual environment:

Unix based systems:
```
virtualenv env
source env/bin/activate
```

Windows:
```
python -m venv env
source env/Scripts/activate
```

3. Install Python requirements:

```
pip install -r requirements.txt
```

4. Create a SECRET_KEY and copy:

```
python secret_key.py
```

5. Create a `.env` file and add a SECRET_KEY value to `.env`:

```
SECRET_KEY=generated-secret-key
```

6. Migrate DB:

```
python manage.py migrate
```

7. To create superuser:

```
python manage.py createsuperuser
```

8. Run application:

```
python manage.py
```

-----------------------------------------
🧱 GIT MANAGEMENT GUIDE
-----------------------------------------
Branch naming convention:
- phase1-login-home
- phase2-product-search
- phase3-cart-checkout
- phase4-admin-dashboard

Each branch only contains its respective features + previous phase.

-----------------------------------------
📄 .gitignore RECOMMENDED
-----------------------------------------
venv/
__pycache__/
*.pyc
db.sqlite3
.env
/static/
media/
