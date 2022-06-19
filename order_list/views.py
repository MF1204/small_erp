import json
import os
import traceback

import pandas as pd

from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from django.utils.dateformat import DateFormat
from django.db.models import Q
from openpyxl import load_workbook

from information.models import Product, Delivery, Pay_type, Order_type, Category, Size, Sheet, Filling, Boxing
from order_list.models import Order
from accounts.models import Member
from accounts.views import session_match
from order_sheet.views import datenum, create_no

# ====================== 전체 주문 목록


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
        print(category_big)
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


class page_list(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}
        data = request.body.decode('utf-8')
        data = json.loads(data)
        idlist = data['order_id']
        sendlist = []
        for pkid in idlist:
            sendone = Order.objects.filter(pno=pkid).values()
            sendlist.append(list(sendone))

        context['list'] = sendlist
        context['success'] = True
        context['message'] = '저장되었습니다.'
        return JsonResponse(context, content_type='application/json')


def order_list_view(request):
    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
        session_match(request.session.session_key, memberno)
    else:
        return redirect('accounts:signin')
    # 전처리
    delivery_table = Delivery.objects.all()
    pay_table = Pay_type.objects.all()
    order_type_table = Order_type.objects.all()

    now = datetime.now()
    # beforeday = now - timedelta(days=1)
    # nextday = now + timedelta(days=1)

    today = DateFormat(now).format('Y-m-d')

    first_day = now.replace(day=1)
    nextmonth = first_day + relativedelta.relativedelta(months=1)
    last_day = nextmonth - timedelta(days=1)
    first_day = DateFormat(first_day).format('Y-m-d')
    last_day = DateFormat(last_day).format('Y-m-d')
    # beginday = DateFormat(beforeday).format('Y-m-d')
    # afterday = DateFormat(nextday).format('Y-m-d')
    # 입력 파라미터
    date = request.GET.get('valuedate', 'order')    # 주문 or 납품일 기준
    # if date == 'order':
    #     startdate = request.GET.get('startdate', today)  # 검색시작일
    #     enddate = request.GET.get('enddate', today)  # 검색종료일
    # elif date == 'deploy':
    #     startdate = request.GET.get('startdate', today)  # 검색시작일
    #     enddate = request.GET.get('enddate', today)  # 검색종료일
    startdate = request.GET.get('startdate', first_day)
    enddate = request.GET.get('enddate', last_day)
    page = request.GET.get('page', '1')  # 페이지
    pagecount = request.GET.get('count', '20')  # 페이지 당 주문의 수
    kwtype = request.GET.get('kwtype', '')  # 검색 분류
    kw = request.GET.get('kw', '')  # 검색키워드
    cakefilter = request.GET.get('cakefilter', 0)   # 케이크 필터링
    deliveryfilter = request.GET.get('deliveryfilter', 0)   # 택배 필터링
    # 날짜, 기간 조회
    if date == 'order':
        orderDetail = Order.objects.filter(usage_flag=1).order_by('-order_date')
        orderDetail = orderDetail.filter(order_date__range=[startdate, enddate])
    elif date == 'deploy':
        orderDetail = Order.objects.filter(usage_flag=1).order_by('-receipt_date')
        orderDetail = orderDetail.filter(receipt_date__range=[startdate, enddate])

    if kw and kwtype == '':
        orderDetail = orderDetail.filter(
            Q(customer__icontains=kw) |     # 고객명
            Q(customer_phone__icontains=kw) |   # 고객 연락처
            Q(recipient__icontains=kw) |   # 수취인
            Q(recipient_phone__icontains=kw)    # 수취인 연락처
        ).distinct()
    elif kw and kwtype == 'customer':
        orderDetail = orderDetail.filter(
            Q(customer__icontains=kw)   # 고객명
        )
    elif kw and kwtype == 'recipient':
        orderDetail = orderDetail.filter(
            Q(customer_phone__icontains=kw)     # 고객연락처
        )
    elif kw and kwtype == 'product':
        orderDetail = orderDetail.filter(
            Q(product_name__icontains=kw)   # 상품명
        )
    elif kw and kwtype == 'recipient_phone':
        orderDetail = orderDetail.filter(
            Q(recipient_phone__icontains=kw)   # 수취인 연락처
        )
    delivery = '0'
    if deliveryfilter == '1':
        orderDetail = orderDetail.exclude(delivery_option_name='일반택배')
        delivery = '1'

    # 페이징
    paginator = Paginator(orderDetail, pagecount)  # 페이지당 보여줄 데이터의 수
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "member_no": memberno,
        "member_name": membername,
        "member_auth": memberauth,
        "orderDetail": page_obj,
        "max_index": max_index,
        "delivery_table": delivery_table,
        "pay_table": pay_table,
        "order_type_table": order_type_table,
        "valuedate": date,
        "startdate": startdate,
        "enddate": enddate,
        "today": today,
        "firstday": first_day,
        "lastday": last_day,
        "page": page,
        "count": pagecount,
        "kwtype": kwtype,
        "kw": kw,
        "delivery": delivery,
    }

    return render(request, "list.html", context)


# CRUD 페이지
def crud(request):
    context = {}
    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']

    pno = request.GET.get('pno')

    searchono = Order.objects.get(pno=pno)
    ono = searchono.order_no

    updatelist = Order.objects.filter(order_no=ono, usage_flag=1)  # 주문 상품 목록
    commondata = Order.objects.filter(order_no=ono).first()  # 상품 첫번째(공통요소를 사용하기 위해 추출)
    '''
    주문테이블을 별도로 분리시켜 가격 연동이 안되기 때문에
    해당하는 옵션의 테이블에서 정보를 다시 탐색해야함
    '''
    info_price = []
    info_size = []
    info_sheet = []
    info_fill = []
    info_box = []
    info_phrase = []
    for one in updatelist :
        name_product = one.product_name
        name_size = one.size_option_name
        name_sheet = one.sheet_option_name
        name_fill = one.filling_option_name
        name_box = one.boxing_option_name

        product = Product.objects.get(product_name=name_product)
        product_price = product.product_price
        product_id = product.product_id
        try:
            option_size = Size.objects.get(product_id=product_id, size_name=name_size)
        except ObjectDoesNotExist:
            option_size = ''
        option_sheet = Sheet.objects.get(sheet_name=name_sheet)
        option_fill = Filling.objects.get(filling_name=name_fill)
        option_box = Boxing.objects.get(boxing_name=name_box)

        info_price.append(product_price)
        if option_size != '':
            info_size.append(option_size.size_price)
        else:
            info_size.append(0)
        if one.phrase != '':
            phrase_price = 5000
        else:
            phrase_price = 0
        info_sheet.append(option_sheet.sheet_price)
        info_fill.append(option_fill.filling_price)
        info_box.append(option_box.boxing_price)
        info_phrase.append(phrase_price)

    context['info_price'] = info_price
    context['info_size'] = info_size
    context['info_sheet'] = info_sheet
    context['info_fill'] = info_fill
    context['info_box'] = info_box
    context['info_phrase'] = info_phrase

    member = Member.objects.all()  # 주문접수자 조회
    order_type = Order_type.objects.all()  # 주문 경로 조회
    delivery = Delivery.objects.all()  # 배송정보
    products = Product.objects.all()  # 상품
    categories = Category.objects.all()  # 상품분류
    sheet = Sheet.objects.all()  # 시트
    filling = Filling.objects.all()
    boxing = Boxing.objects.all()
    pay_type = Pay_type.objects.all()

    context["member_no"] = memberno
    context["member_name"] = membername
    context["member_auth"] = memberauth
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
    context['updatelist'] = updatelist
    context['len'] = len(updatelist)
    context['common'] = commondata
    context['pno'] = pno

    return render(request, 'crud.html', context)


def update(request):
    context = {}
    if request.method != 'POST':
        context['order'] = '잘못된 요청입니다'
        return JsonResponse(context, content_type="application/json")

    databody = request.body.decode('utf-8')
    datajson = json.loads(databody)
    # 추가, 변경, 삭제 list
    order, updatelist, deletelist = datajson['order'], datajson['update'], datajson['delete']

    # update할 번호
    firstorder = Order.objects.get(pno=datajson['pno'])

    # 공통정보
    emp = order['emp']
    order_date = order['order_date']
    format = '%Y-%m-%d'
    orderday = datetime.strptime(order_date, format).date()
    if firstorder.order_date == orderday:
        print('=====================')
        date_no = firstorder.date_no
        order_no = firstorder.order_no
    else:
        date_no = datenum(order_date)
        order_no = create_no(emp, order_date, date_no)
    order_type = order['order_type']
    customer = order['customer']
    customer_phone = order['customerphone']
    delivery = order['delivery']
    receipt_date = order['receiptdate']
    receipt_hour = datetime.strptime(order['receipthour'], '%H:%M')
    pay_price = order['payprice']
    pay_check = order['paycheck']
    pay_type = order['paytype']
    recipient = order['recipient']
    recipientphone = order['recipientphone']
    address1 = order['address1']
    address2 = order['address2']
    memo = order['memo']

    # 개별상품정보
    product = order['_productList']
    alarm = ''

    for ea in product:
        pno = int(ea['pno'])
        name = ea['name']
        size = ea['size']
        fill = ea['fill']
        sheet = ea['sheet']
        box = ea['box']
        phrase = ea['phrase']
        count = ea['count']
        price = int(ea['price']) * int(count)

        if pno != 0:
            updateorder = Order.objects.get(pno=pno)
            updateorder.order_date = order_date
            updateorder.order_no = order_no
            updateorder.date_no = date_no
            updateorder.employee_name = emp
            updateorder.order_type = order_type
            updateorder.customer = customer
            updateorder.customer_phone = customer_phone
            updateorder.delivery = delivery
            updateorder.receipt_date = receipt_date
            updateorder.receipt_hour = receipt_hour
            updateorder.total_price = pay_price
            updateorder.pay_check = pay_check
            updateorder.pay_type_name = pay_type
            updateorder.recipient = recipient
            updateorder.recipient_phone = recipientphone
            updateorder.address1 = address1
            updateorder.address2 = address2
            updateorder.memo = memo
            updateorder.product_name = name
            updateorder.size_option_name = size
            updateorder.filling_option_name = fill
            updateorder.sheet_option_name = sheet
            updateorder.boxing_option_name = box
            updateorder.phrase = phrase
            updateorder.count = count
            updateorder.product_price = price
            updateorder.save()
            alarm += f'{name}, {count}개 수정완료' + '\n'
        elif pno == 0:
            rs = Order.objects.create(order_no=order_no, employee_name=emp,
                                      order_date=order_date, customer=customer, date_no=date_no,
                                      customer_phone=customer_phone, order_type_name=order_type,
                                      pay_type_name=pay_type, pay_check=pay_check,
                                      product_name=name, state='주문완료',
                                      receipt_date=receipt_date, receipt_hour=receipt_hour,
                                      size_option_name=size, sheet_option_name=sheet,
                                      filling_option_name=fill, boxing_option_name=box,
                                      count=count, total_price=pay_price, product_price=price,
                                      recipient=recipient, recipient_phone=recipientphone,
                                      delivery_option_name=delivery, address1=address1, address2=address2,
                                      phrase=phrase, memo=memo)
            alarm += f'{name}, {count}개 등록완료' + '\n'

    if len(deletelist) != 0:
        for i in deletelist:
            deleteobject = Order.objects.get(pno=i)
            deleteobject.usage_flag = 0
            deleteobject.save()
            alarm += f'{deleteobject.product_name}, {deleteobject.count}개 삭제완료' + '\n'

    context['alarm'] = alarm

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def delete(request):
    context = {}
    if request.method == 'POST':
        databody = request.body.decode('utf-8')
        datajson = json.loads(databody)

        # delete 대상
        pno = datajson['pno']
        print(pno)

        for number in pno:
            deleteorder = Order.objects.get(pno=number)
            deleteorder.usage_flag = 0
            deleteorder.save()

        context['flag'] = 1
        context['msg'] = f'{len(pno)}건 삭제완료'

    else:
        context['flag'] = 0
        context['msg'] = '에러발생'
    return JsonResponse(context, content_type="application/json")


def printall(request):
    context = {}
    jsondata = json.loads(request.body.decode('utf-8'))
    pnolist = jsondata['pnoList']
    pnolist = pnolist.split(',')
    jsonlist = []
    for pno in pnolist:
        select_order = Order.objects.filter(pno=pno).values()
        jsonlist.append(list(select_order))

    deposit = jsonlist
    transferlist = []
    savelist = []
    n = 0
    name = 1
    for i in deposit:

        if n % 6 == 0:
            transferlist = []

        transferlist.append(i)

        if n == len(deposit) - 1 or n % 6 == 5:
            savelist.append(transferlist)
            name += 1

        n += 1

    context['printlist'] = savelist
    context['flag'] = True
    return JsonResponse(context, content_type="application/json")


def popup(request):
    return render(request, 'printall.html')


def printlist(request):

    now = datetime.now()
    beforeday = now - timedelta(days=1)
    nextday = now + timedelta(days=1)

    today = DateFormat(now).format('Y-m-d')
    beginday = DateFormat(beforeday).format('Y-m-d')
    afterday = DateFormat(nextday).format('Y-m-d')
    # 입력 파라미터
    date = request.GET.get('valuedate', 'order')  # 주문 or 납품일 기준
    if date == 'order':
        startdate = request.GET.get('startdate', beginday)  # 검색시작일
        enddate = request.GET.get('enddate', today)  # 검색종료일
    elif date == 'deploy':
        startdate = request.GET.get('startdate', today)  # 검색시작일
        enddate = request.GET.get('enddate', afterday)  # 검색종료일
    page = request.GET.get('page', '1')  # 페이지
    pagecount = request.GET.get('count', '20')  # 페이지 당 주문의 수
    kwtype = request.GET.get('kwtype', '')  # 검색 분류
    kw = request.GET.get('kw', '')  # 검색키워드
    # 날짜, 기간 조회
    if date == 'order':
        orderDetail = Order.objects.filter(usage_flag='1').order_by('-order_date')
        orderDetail = orderDetail.filter(order_date__range=[startdate, enddate])
    elif date == 'deploy':
        orderDetail = Order.objects.filter(usage_flag='1').order_by('-receipt_date')
        orderDetail = orderDetail.filter(receipt_date__range=[startdate, enddate])

    if kw and kwtype == '':
        orderDetail = orderDetail.filter(
            Q(customer__icontains=kw) |  # 고객명
            Q(customer_phone__icontains=kw) |  # 고객 연락처
            Q(recipient__icontains=kw) |  # 수취인
            Q(recipient_phone__icontains=kw)  # 수취인 연락처
        ).distinct()
    elif kw and kwtype == 'customer':
        orderDetail = orderDetail.filter(
            Q(customer__icontains=kw)  # 고객명
        )
    elif kw and kwtype == 'recipient':
        orderDetail = orderDetail.filter(
            Q(customer_phone__icontains=kw)  # 고객연락처
        )
    elif kw and kwtype == 'product':
        orderDetail = orderDetail.filter(
            Q(product_name__icontains=kw)  # 상품명
        )
    elif kw and kwtype == 'recipient_phone':
        orderDetail = orderDetail.filter(
            Q(recipient_phone__icontains=kw)  # 수취인 연락처
        )

    # 페이징
    paginator = Paginator(orderDetail, pagecount)  # 페이지당 보여줄 데이터의 수
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "orderDetail": page_obj,
        "max_index": max_index,
        "valuedate": date,
        "startdate": startdate,
        "enddate": enddate,
        "today": today,
        "beginday": beginday,
        "afterday": afterday,
        "page": page,
        "count": pagecount,
        "kwtype": kwtype,
        "kw": kw
    }
    return render(request, 'printlist.html', context)


@csrf_exempt
def changestatus(request):
    context = {}

    if request.method == "POST":
        bodydata = request.body.decode('utf-8')
        bodyjson = json.loads(bodydata)
        status = bodyjson['status']
        order = bodyjson['order']
        for i in order:
            pno = i
            orderlist = Order.objects.get(pno=pno)
            if status == 1:
                orderlist.state = '제작완료'
            elif status == 2:
                orderlist.state = '출고완료'
            elif status == 3:
                orderlist.state = '출고보류'
            elif status == 4:
                orderlist.state = '출고취소'
            elif status == 5:
                orderlist.state = '기타'
            elif status == 0:
                orderlist.state = '주문완료'
            orderlist.save()

        context["flag"] = "0"
        context["result_msg"] = f'{len(order)}건 처리완료'
        return JsonResponse(context, content_type="application/json")


@csrf_exempt
def autocomplete(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    kwList = bodyjson['fwvalue']
    kwtype = bodyjson['fwtype']

    orderDetail = Order.objects.all().order_by('-order_date')

    autokw = set()
    if kwList and kwtype == '':

        customer = orderDetail.filter(Q(customer__icontains=kwList))
        if customer.exists():
            for order in customer:
                autokw.add(order.customer)

        recipient = orderDetail.filter(Q(recipient__icontains=kwList))
        if recipient.exists():
            for order in recipient:
                autokw.add(order.recipient)

        rphone = orderDetail.filter(Q(recipient_phone__icontains=kwList))
        if rphone.exists():
            for order in rphone:
                autokw.add(order.recipient_phone)

        product = orderDetail.filter(Q(product_name__icontains=kwList))
        if product.exists():
            for order in product:
                autokw.add(order.product_name)

    elif kwList and kwtype == 'customer':

        customer = orderDetail.filter(Q(customer__icontains=kwList))
        if customer.exists():
            for order in customer:
                autokw.add(order.customer)

    elif kwList and kwtype == 'recipient':

        recipient = orderDetail.filter(Q(recipient__icontains=kwList))
        if recipient.exists():
            for order in recipient:
                autokw.add(order.recipient)

    elif kwList and kwtype == 'recipient_phone':

        rphone = orderDetail.filter(Q(recipient_phone__icontains=kwList))
        if rphone.exists():
            for order in rphone:
                autokw.add(order.recipient_phone)

    elif kwList and kwtype == 'product':

        product = orderDetail.filter(Q(product_name__icontains=kwList))
        if product.exists():
            for order in product:
                autokw.add(order.product_name)

    print(autokw)
    autolist = list(autokw)
    print(autolist)
    context["flag"] = "0"
    context["kwList"] = autolist
    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def exceldown(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    filename = bodyjson["name"]
    order = bodyjson["order"]
    customer = []
    phone_main = []
    phone_sub = []
    address = []
    product = []
    product_sub = []
    product_ea = []
    message = []

    for one in order:
        customer.append(one['recipient'])
        phone_main.append(one['recipientphone'])
        phone_sub.append(one['customerphone'])
        ad = one['address1'] + '' + one['address2']
        address.append(ad)
        product.append(one['category'])
        # detail = one['name'] + '(' + one['size'] + ', ' + one['fill'] + ', ' + one['sheet'] + ', ' + one['box'] + ')'
        detail = one['name']
        product_sub.append(detail)
        product_ea.append(one['count'])
        message.append(one['memo'])

    raw_data = {
        '받는분성명': customer,
        '받는분전화번호': phone_main,
        '받는분기타연락처': phone_sub,
        '받는분주소(전체, 분할)': address,
        '품목명': product,
        '내품명': product_sub,
        '내품수량': product_ea,
        '배송메세지1': message
    }
    raw_data = pd.DataFrame(raw_data)
    try:
        raw_data.to_excel(excel_writer='static/excel/{}.xlsx'.format(filename), index=None)
        context['flag'] = 1
    except PermissionError:
        context['flag'] = 0
        context['msg'] = '파일이 열려 있습니다. 종료 후 다시 시도해주세요.'

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def exceldel(request):
    context = {}
    filename = request.GET.get('name', 'null')
    if filename != '':
        os.remove('static/excel/{}.xlsx'.format(filename))
        context['msg'] = '삭제완료'

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def upload(request):
    membername = request.session['member_name']
    context = {}
    s_count = 0
    f_count = 0
    if request.method == 'POST':
        file = request.FILES['file_excel']

        load_wb = load_workbook(file, data_only=True)

        load_ws = load_wb['Sheet1']

        all_values = []
        for row in load_ws.rows:
            row_value = []
            for cell in row:
                row_value.append(cell.value)
            all_values.append(row_value)

        i = 1
        row = all_values
        dno = 1     # 이전 date_no 저장

        while i < len(row):

            if str(type(row[i][0])) == "<class 'datetime.datetime'>":
                order_date = row[i][0].strftime('%Y-%m-%d')
            else:
                order_date = datetime.strptime(row[i][0], '%Y-%m-%d')
                order_date = order_date.strftime('%Y-%m-%d')

            if str(type(row[i][5])) == "<class 'datetime.datetime'>":
                receipt_date = row[i][5].strftime('%Y-%m-%d')
            else:
                receipt_date = datetime.strptime(row[i][5], '%Y-%m-%d')
                receipt_date = receipt_date.strftime('%Y-%m-%d')

            if i == 1:
                date_no = datenum(order_date)
                dno = date_no
            elif i > 1 and row[i - 1][3] != row[i][3]:
                date_no = datenum(order_date)
                dno = date_no
            else:
                date_no = dno

            try:
                autoorder(row[i], membername, order_date, date_no, receipt_date)
                s_count += 1
            except Exception as e:
                print('번호:{}'.format(s_count + f_count))
                print('error:{}'.format(e))
                traceback.print_exc()
                f_count += 1
            i += 1

        context['s_count'] = s_count
        context['f_count'] = f_count
        context['rtnmsg'] = '성공:{}건, 에러:{}건'.format(s_count, f_count)
        return JsonResponse(context, content_type="application/json")

    return render(request, 'upload.html', context)


def autoorder(row, name, order_date, date_no, receipt_date):
    emp = name  # 사용자 자동등록
    order_no = create_no(emp, order_date, date_no)  # 자동생성
    order_type = row[1]
    customer = row[2]
    customer_phone = row[3]
    delivery = row[4]
    receipt_hour = row[6]
    box = row[7]
    phrase = row[8]
    memo = row[9]
    if memo is None:
        memo = '메모없음'
    pay_price = row[10]
    name = row[11]
    size = row[12]
    sheet = row[13]
    fill = row[14]
    count = row[15]
    price = row[16]
    recipient = row[17]
    recipientphone = row[18]
    address1 = row[19]
    address2 = row[20]
    pay_check = row[21]
    pay_type = row[22]
    cafe24_no = row[23]
    status = '주문완료'
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
                              phrase=phrase, memo=memo, cafe24_no=cafe24_no)
    return


@csrf_exempt
def filedown(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    filename = bodyjson["name"]
    order = bodyjson["order"]
    order_date = []
    date_no = []
    order_type = []
    customer = []
    phone_cus = []
    delivery = []
    receipt_date = []
    receipt_hour = []
    box = []
    phrase = []
    memo = []
    pay_price = []
    product = []
    size = []
    sheet = []
    fill = []
    count = []
    price = []
    recipient = []
    phone_rec = []
    address1 = []
    address2 = []
    pay_check = []
    pay_type = []
    status = []
    cafe24_no = []

    for one in order:
        order_date.append(one['order_date'])
        date_no.append(one['date_no'])
        order_type.append(one['order_type_name'])
        customer.append(one['customer'])
        phone_cus.append(one['customerphone'])
        delivery.append(one['delivery'])
        receipt_date.append(one['receipt_date'])
        receipt_hour.append(one['receipt_hour'])
        box.append(one['box'])
        phrase.append(one['phrase'])
        memo.append(one['memo'])
        pay_price.append(one['pay_price'])
        product.append(one['product'])
        size.append(one['size'])
        sheet.append(one['sheet'])
        fill.append(one['fill'])
        count.append(one['count'])
        price.append(one['price'])
        recipient.append(one['recipient'])
        phone_rec.append(one['recipientphone'])
        address1.append(one['address1'])
        address2.append(one['address2'])
        pay_check.append(one['pay_check'])
        pay_type.append(one['pay_type'])
        status.append(one['status'])
        cafe24_no.append(one['cafe24_no'])

    raw_data = {
        '주문일': order_date,
        '주문No': date_no,
        '주문경로': order_type,
        '주문고객': customer,
        '고객연락처': phone_cus,
        '배송방법': delivery,
        '출고일': receipt_date,
        '출고시간': receipt_hour,
        '포장': box,
        '문구': phrase,
        '메모': memo,
        '결제금액': pay_price,
        '상품명': product,
        '사이즈': size,
        '시트': sheet,
        '필링': fill,
        '수량': count,
        '상품가격': price,
        '수령인': recipient,
        '수령인연락처': phone_rec,
        '주소': address1,
        '상세주소': address2,
        '결제여부': pay_check,
        '결제방법': pay_type,
        '주문상태': status,
        '쇼핑몰 주문번호': cafe24_no,
    }
    raw_data = pd.DataFrame(raw_data)
    try:
        raw_data.to_excel(excel_writer='static/excel/{}.xlsx'.format(filename), index=None)
        context['flag'] = 1
    except PermissionError:
        context['flag'] = 0
        context['msg'] = '파일이 열려 있습니다. 종료 후 다시 시도해주세요.'

    return JsonResponse(context, content_type="application/json")
