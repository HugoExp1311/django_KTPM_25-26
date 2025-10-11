=========================================
DJANGO E-COMMERCE PROJECT - REPO STRUCTURE
=========================================

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
│       ├── product_detail.html  
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
✅ Product list + detail page  
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
│       ├── cart.html  
│       ├── checkout.html  
│
└── + all files from Phase 1 & 2  

Test Scope:
✅ Add to cart / remove from cart  
✅ View cart summary  
✅ Checkout page  

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
✅ Admin login  
✅ Manage users/products/orders  
✅ Dashboard analytics  

-----------------------------------------
🧰 ENVIRONMENT SETUP
-----------------------------------------
1️⃣ Create venv:
    python -m venv venv
    venv\Scripts\activate

2️⃣ Install dependencies:
    pip install -r requirements.txt

3️⃣ Apply migrations:
    python manage.py migrate

4️⃣ Run server:
    python manage.py runserver

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
