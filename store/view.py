# store/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order, OrderItem

@login_required
def order_history(request):
    # Lấy tất cả orders của user hiện tại, sắp xếp theo thời gian mới nhất
    orders = Order.objects.filter(user=request.user, complete=True).order_by('-date_ordered')
    
    # Tạo danh sách orders với thông tin chi tiết
    order_list = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        order_list.append({
            'order': order,
            'items': order_items,
            'total': order.get_cart_total
        })
    
    context = {
        'orders': order_list
    }
    return render(request, 'store/order_history.html', context)

@login_required
def order_detail(request, order_id):
    try:
        # Chỉ cho phép user xem order của chính họ
        order = Order.objects.get(id=order_id, user=request.user, complete=True)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'items': order_items,
            'total': order.get_cart_total
        }
        return render(request, 'store/order_detail.html', context)
    except Order.DoesNotExist:
        return render(request, 'store/404.html')
    
    # store/views.py
@login_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # Gán user cho order nếu user đã đăng nhập
    if request.user.is_authenticated:
        order.user = request.user
        order.save()

    return JsonResponse('Payment submitted..', safe=False)