import datetime
from django.http import JsonResponse, HttpResponse
import json
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from information.models import Product, Category, Order_type, Pay_type, Delivery, Size, Sheet, Filling, Boxing
from order_list.models import Order
from accounts.models import Member
from datetime import datetime
import re


# ====================== POST TEST
@csrf_exempt
def post_create(request):
    context = {}
    size = ''
    if request.method == "POST":
        bodydata = request.body.decode('utf-8')
        bodyjson = json.loads(bodydata)
        size = bodyjson['size']

    context['size'] = size
    context['result_msg'] = '통신성공'

    return JsonResponse(context, content_type="application/json")


# ====================== 주문서 페이지 출력
def new_order(request):

    context = {}
    # # 사용자 권한 제어==========================================
    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    context["member_no"] = memberno
    context["member_name"] = membername
    context["member_auth"] = memberauth
    # =============================================================

    member = Member.objects.all() # 주문접수자 조회
    order_type = Order_type.objects.all() # 주문 경로 조회
    delivery = Delivery.objects.all() # 배송정보
    products = Product.objects.all() # 상품
    categories = Category.objects.all() # 상품분류
    sheet = Sheet.objects.all() #시트
    filling = Filling.objects.all()
    boxing = Boxing.objects.all()
    pay_type = Pay_type.objects.all()

    context["member_table"] = member
    context["order_type_table"] = order_type
    context["delivery_table"] = delivery
    context["products_table"] = products
    context["categories_table"] = categories
    context["sheet_table"] = sheet
    context["sheet_first"] = sheet.first()
    context["filling_table"] = filling
    context["filling_first"] = filling.first()
    context["boxing_table"] = boxing
    context["boxing_first"] = boxing.first()
    context["pay_type_table"] = pay_type

    return render(request, 'sheet.html', context)


@csrf_exempt
def option_view(request):
    context = {}
    name = request.GET.get('name', '')
    print(f'상품이름 : {name}')

    # 옵션테이블 조회
    if Product.objects.filter(product_name=name).exists():
        product = Product.objects.get(product_name=name)
        size = Size.objects.filter(product_id=product.product_id)
        category_id = product.category_id.category_id
        category = Category.objects.get(category_id=category_id)
        category_big = category.category_big
        context["category"] = category_big
        context["price"] = int(product.product_price)
        context["flag"] = 1
        if size.exists():
            context["size"] = list(size.values())
        else:
            context["size"] = ''
    else:
        context["flag"] = 0

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def product_price(request):
    context = {}

    if request.method == "POST":
        bodydata = request.body.decode('utf-8')
        bodyjson = json.loads(bodydata)
        size = bodyjson['size']


    return JsonResponse(context, content_type="application/json")


# ====================== 새로운 주문서 작성
@csrf_exempt
def create_order(request):
    context = {}
    if request.method == 'POST':
        databody = request.body.decode('utf-8')
        datajson = json.loads(databody)

        # 공통정보
        newOrder = datajson['order']
        emp = newOrder['emp']
        order_date = newOrder['order_date']
        date_no = datenum(order_date)
        order_no = create_no(emp, order_date, date_no)
        order_type = newOrder['order_type']
        customer = newOrder['customer']
        customer_phone = newOrder['customerphone']
        delivery = newOrder['delivery']
        receipt_date = newOrder['receiptdate']
        receipt_hour = newOrder['receipthour']
        pay_price = newOrder['payprice']
        pay_check = newOrder['paycheck']
        pay_type = newOrder['paytype']
        recipient = newOrder['recipient']
        recipientphone = newOrder['recipientphone']
        address1 = newOrder['address1']
        address2 = newOrder['address2']
        memo = newOrder['memo']
        if memo == '':
            memo = '메모없음'
        status = newOrder['status']

        # 개별상품정보
        product = newOrder['_productList']
        i = 0
        alarm = ''
        for ea in product:
            name = ea['name']
            size = ea['size']
            fill = ea['fill']
            sheet = ea['sheet']
            box = ea['box']
            phrase = ea['phrase']
            count = ea['count']
            price = ea['price']

            rs = Order.objects.create(order_no=order_no, employee_name=emp,
                                      order_date=order_date, customer=customer, date_no=date_no,
                                      customer_phone=customer_phone, order_type_name=order_type,
                                      pay_type_name=pay_type, pay_check=pay_check,
                                      product_name=name, state=status,
                                      receipt_date=receipt_date, receipt_hour=receipt_hour,
                                      size_option_name=size, sheet_option_name=sheet,
                                      filling_option_name=fill, boxing_option_name=box,
                                      count=count, total_price=pay_price, product_price=price,
                                      recipient=recipient, recipient_phone=recipientphone,
                                      delivery_option_name=delivery, address1=address1, address2=address2,
                                      phrase=phrase, memo=memo)
            alarm += f'{name}, {count}개 등록완료' + '\n'
            i = i + 1

        context['alarm'] = alarm

    else:
        context['order'] = '잘못된 요청입니다'
    return JsonResponse(context, content_type="application/json")


def create_no(employee, order_date, date_no):

    if str(type(order_date)) == "<class 'datetime.datetime'>":
        order_date = order_date.strftime('%Y-%m-%d')
        order_date = str(order_date)
    else:
        order_date = datetime.strptime(order_date, '%Y-%m-%d')
        order_date = str(order_date.strftime('%Y-%m-%d'))

    today = re.sub('-', '', order_date)
    countstr = str(date_no).zfill(3)
    order_no = f'{today}_{employee}_{countstr}'

    return order_no


def datenum(order_date):

    if str(type(order_date)) == "<class 'datetime.datetime'>":
        orderday = order_date.strftime('%Y-%m-%d')
    else:
        orderday = datetime.strptime(order_date, '%Y-%m-%d')

    if Order.objects.filter(order_date=orderday).exists():
        last = Order.objects.filter(order_date=orderday).order_by('-date_no').first()
        count = last.date_no + 1

    else:
        count = 1

    return count
