from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Avg, F, ExpressionWrapper, DecimalField
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, \
ProductImages, ProductReview, Wishlist, Address, ContactUs
from core.forms import ProductReviewFrom
from taggit.models import Tag

def index(request):
	products = Product.objects.filter(product_status='published', featured=True)

	special_offers = Product.objects.filter(product_status='published').annotate(
		discount_percentage=ExpressionWrapper(
			((F('old_price') - F('price')) / F('old_price')) * 100,
			output_field=DecimalField()
		)
    ).order_by('-discount_percentage')[:9]
    
	oldest_products = Product.objects.filter(product_status='published').order_by('date')

	context = {
		"products": products,
		"special_offers": special_offers,
		"oldest_products": oldest_products,
	}
	return render(request, 'core/index.html', context)

def products_list_view(request):
	products = Product.objects.filter(product_status='published')
	context = {
		"products": products
	}
	return render(request, 'core/product-list.html', context)

def category_list_view(request):
	categories = Category.objects.all()
	context = {
		"categories": categories,
	}
	return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
	category = Category.objects.get(cid=cid)
	products = Product.objects.filter(product_status='published', category=category)
	context = {
		"category": category,
		"products": products,
	}
	return render(request, 'core/category-products-list.html', context)

def vendor_list_view(request):
	vendors = Vendor.objects.all()
	context = {
		'vendors': vendors,
	}
	return render(request, 'core/vendor-list.html', context)

def vendor_detail_view(request, vid):
	vendor = Vendor.objects.get(vid=vid)
	products = Product.objects.filter(product_status='published', vendor=vendor)
	context = {
		'vendor': vendor,
		'products': products,
	}
	return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
	product = Product.objects.get(pid=pid)
	# product = get_object_or_404(Product, pid=pid)
	products = Product.objects.filter(category=product.category).exclude(pid=pid)
	p_image = product.p_images.all()

	reviews = ProductReview.objects.filter(product=product).order_by('-date')
	average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
	review_form = ProductReviewFrom()

	make_review = True
	if request.user.is_authenticated:
		user_review_count = ProductReview.objects.filter(user=request.user, product=product).count() 

		if user_review_count > 0:
			make_review = False

	context = {
		'product': product,
		'p_image': p_image,
		'products': products,
		'reviews': reviews,
		'average_rating': average_rating,
		'review_form': review_form,
		'make_review': make_review,
	}
	return render(request, 'core/product-detail.html', context)

def tags_list(request, tag_slug=None):
	products = Product.objects.filter(product_status='published').order_by('-id')

	tag = None
	if tag_slug:
		tag = Tag.objects.get(slug=tag_slug)
		# tag = get_object_or_404(Tag, slug=tag_slug)
		products = products.filter(tags__in=[tag])

	context = {
		'products': products,
		'tag': tag,
	}

	return render(request, 'core/tag.html', context)

def ajax_add_review(request, pid):
	product = Product.objects.get(pk=pid)
	user = request.user
	image = user.image.url

	review = ProductReview.objects.create(
		user=user,
		product=product,
		review=request.POST['review'],
		rating=request.POST['rating'],
	)
	
	context = {
		'user': user.username,
		'review': request.POST['review'],
		'rating': request.POST['rating'],
		'image': image
	}

	average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))


	return JsonResponse(
		{
			'bool': True,
			'context': context,
			'average_reviews': average_reviews,
		}
	)

def search_view(request):
	# query = request.GET['q'] OR
	query = request.GET.get('q') 

	products = Product.objects.filter(title__icontains=query).order_by('-date')

	context = {
		'products': products,
		'query': query,
	}

	return render(request, 'core/search.html', context)

def filter_product(request):
	categories = request.GET.getlist('category[]')
	vendors = request.GET.getlist('vendor[]')

	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')

	products = Product.objects.filter(product_status='published').order_by('-id').distinct()

	products = products.filter(price__gte=min_price)
	products = products.filter(price__lte=max_price)

	if len(categories) > 0:
		products = products.filter(category__id__in=categories).distinct()
	if len(vendors) > 0:
		products = products.filter(vendor__id__in=vendors).distinct()

	context = {
		'products': products
	}

	data = render_to_string('core/async/product-list.html', context)
	return JsonResponse({'data': data})

def add_to_cart(request):
	cart_product = {}

	cart_product[str(request.GET['id'])] = {
		'qty': request.GET['qty'],
		'title': request.GET['title'],
		'price': request.GET['price'],
		'image': request.GET['image'],
		'pid': request.GET['pid'],
	}

	if 'cart_data_object' in request.session:
		if str(request.GET['id']) in request.session['cart_data_object']:
			cart_data = request.session['cart_data_object']
			cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cart_data_object'] = cart_data
		else:
			cart_data = request.session['cart_data_object']
			cart_data.update(cart_product)
			request.session['cart_data_object'] = cart_data
	else:
		request.session['cart_data_object'] = cart_product

	return JsonResponse({
			'data':request.session['cart_data_object'],
			'totalcartitems':len(request.session['cart_data_object'])
		})

def cart_view(request):
	cart_total_amount = 0
	if 'cart_data_object' in request.session:
		for product_id, item in request.session['cart_data_object'].items():
			cart_total_amount += int(item['qty']) * float(item['price'])

		return render(request, 'core/cart.html', {
			'cart_data': request.session['cart_data_object'],
			'totalcartitems': len(request.session['cart_data_object']),
			'cart_total_amount': cart_total_amount
		})
		
	else:
		return render(request, 'core/cart.html')

def delete_from_cart(request):
	product_id = str(request.GET['id'])
	if 'cart_data_object' in request.session:
		if product_id in request.session['cart_data_object']:
			cart_data = request.session['cart_data_object']
			del request.session['cart_data_object'][product_id]
			request.session['cart_data_object'] = cart_data

	cart_total_amount = 0
	if 'cart_data_object' in request.session:
		for product_id, item in request.session['cart_data_object'].items():
			cart_total_amount += int(item['qty']) * float(item['price'])

	context = render_to_string('core/async/cart-list.html', {
			'cart_data': request.session['cart_data_object'],
			'totalcartitems': len(request.session['cart_data_object']),
			'cart_total_amount': cart_total_amount
		})
	return JsonResponse({
			'data': context,
			'totalcartitems': len(request.session['cart_data_object']),
		})

def update_cart(request):
	product_id = str(request.GET['id'])
	product_qty = request.GET['qty']
	if 'cart_data_object' in request.session:
		if product_id in request.session['cart_data_object']:
			cart_data = request.session['cart_data_object']
			cart_data[str(request.GET['id'])]['qty'] = product_qty
			request.session['cart_data_object'] = cart_data

	cart_total_amount = 0
	if 'cart_data_object' in request.session:
		for product_id, item in request.session['cart_data_object'].items():
			cart_total_amount += int(item['qty']) * float(item['price'])


	context = render_to_string('core/async/cart-list.html', {
			'cart_data': request.session['cart_data_object'],
			'totalcartitems': len(request.session['cart_data_object']),
			'cart_total_amount': cart_total_amount
		})
	return JsonResponse({
			'data': context,
			'totalcartitems': len(request.session['cart_data_object']),
		})

@login_required
def wishlist_view(request):
	try:
		wishlist = Wishlist.objects.filter(user=request.user)
	except:
		wishlist = None

	context = {
		'wishlist': wishlist
	}
	return render(request, 'core/wishlist.html', context)

@login_required
def add_to_wishlist(request):
	product_id = request.GET['id']
	product = Product.objects.get(id=product_id)

	context = {}

	wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()

	if wishlist_count > 0:
		context	= {
			'bool': True,
			'wishlist_count': Wishlist.objects.filter(user=request.user).count()
		}
	else:
		new_wishlist = Wishlist.objects.create(
			product=product,
			user=request.user
		)
		context = {
			'bool': True,
			'wishlist_count': Wishlist.objects.filter(user=request.user).count()
		}

	return JsonResponse(context)

def remove_from_wishlist(request):
	product_id = request.GET['id']
	wishlist = Wishlist.objects.filter(user=request.user)

	product = Wishlist.objects.get(id=product_id)
	product.delete()

	context = {
		'bool': True,
		'wishlist': wishlist
	}
	qs_json = serializers.serialize('json', wishlist)
	data = render_to_string('core/async/wishlist-list.html', context)
	return JsonResponse({'data': data, 'wishlist': qs_json})

def contact(request):
	return render(request, 'core/contact.html')

def ajax_contact_form(request):
	name = request.GET['name']
	email = request.GET['email']
	message = request.GET['message']

	contact = ContactUs.objects.create(
		name=name,		
		email=email,		
		message=message,		
	)

	data = {
		'bool': True,
	}

	return JsonResponse({'data': data})

def about(request):
	return render(request, 'core/about.html')


 # Add new payment function
import shortuuid
from django.contrib import messages

@login_required(login_url='userauths:sing-in') # <--- Thêm login_url để chắc chắn chuyển đúng trang
def checkout(request):
    cart_total_amount = 0
    cart_items = []
    
    if 'cart_data_object' in request.session:
        # Chuyển đổi dữ liệu session thành danh sách sản phẩm
        for product_id, item in request.session['cart_data_object'].items():
            try:
                product = Product.objects.get(id=product_id)
                quantity = int(item['qty'])
                price = float(item['price'])
                total_price = quantity * price
                
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price,
                    'title': item['title'],
                    'image': item['image'],
                    'product_id': product_id
                })
                cart_total_amount += total_price
            except Product.DoesNotExist:
                continue
    
    shipping_fee = 30000  # Phí vận chuyển
    total_with_shipping = cart_total_amount + shipping_fee
    
    # XỬ LÝ KHI SUBMIT FORM CHECKOUT - THÊM PHẦN NÀY
    if request.method == 'POST' and request.user.is_authenticated:
        # Lấy thông tin từ form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        
        # Kiểm tra giỏ hàng có sản phẩm không
        if not cart_items:
            messages.error(request, "Giỏ hàng của bạn đang trống!")
            return redirect('core:cart')
        
        # Tạo order mới
        order = CartOrder.objects.create(
            user=request.user,
            price=total_with_shipping,
            paid_status=True,  # Giả sử thanh toán thành công
            product_status='process'  # Trạng thái xử lý
        )
        
        # Lưu các order items
        for item in cart_items:
            CartOrderItems.objects.create(
                order=order,
                invoice_no=f"INV-{shortuuid.uuid()[:8].upper()}",
                product_status='process',
                item=item['title'],
                image=item['image'],
                qty=item['quantity'],
                price=item['product'].price,
                total=item['total_price']
            )
        
        # Xóa giỏ hàng sau khi đặt hàng thành công
        if 'cart_data_object' in request.session:
            del request.session['cart_data_object']
        
        messages.success(request, f"Đặt hàng thành công! Mã đơn hàng: #{order.id}")
        return redirect('core:order-history')
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total_amount,
        'total_with_shipping': total_with_shipping,
        'shipping_fee': shipping_fee,
        'cart_data': request.session.get('cart_data_object', {})
    }
    return render(request, 'core/checkout.html', context)

# core/views.py - viewing user orders

# core/views.py
@login_required
def order_history(request):
    # Lấy tất cả orders của user hiện tại, sắp xếp theo thời gian mới nhất
    orders = CartOrder.objects.filter(user=request.user, paid_status=True).order_by('-id')
    
    context = {
        'orders': orders
    }
    return render(request, 'core/order_history.html', context)  # Đổi thành order_history.html

@login_required
def order_detail(request, order_id):
    try:
        # Chỉ cho phép user xem order của chính họ
        order = CartOrder.objects.get(id=order_id, user=request.user, paid_status=True)
        order_items = CartOrderItems.objects.filter(order=order)
        
        # Tính tổng tiền từ các items
        total_amount = sum([item.total for item in order_items])
        
        context = {
            'order': order,
            'order_items': order_items,
            'total_amount': total_amount
        }
        return render(request, 'core/order_detail.html', context)  # Cũng đổi thành order_detail.html
    except CartOrder.DoesNotExist:
        return render(request, 'core/404.html')