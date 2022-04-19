from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Size, Category, Product
from django.db.models import Q
from django.core.paginator import Paginator


# page view
def size_view(request):
    context = {}

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    context["member_no"] = memberno
    context["member_name"] = membername
    context["member_auth"] = memberauth

    page = request.GET.get('page', '1')  # 페이지
    pagecount = request.GET.get('count', '10')  # 페이지 당 주문의 수
    kw = request.GET.get('kw', '')  # 검색키워드

    size = Size.objects.all().order_by('-product_id', '-size_name')

    if kw:
        size = size.filter(
            Q(size_name__icontains=kw)|
            Q(product_id__product_name__icontains=kw)
        ).distinct()

    # 페이징
    paginator = Paginator(size, pagecount)
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    # size table 조회
    # category table 조회
    category = Category.objects.all().order_by('category_big')

    product_dict = {}
    # 존재하는 카테고리 수만큼 반복
    for i in category:
        # 카테고리 id가 일치하는 product
        product = Product.objects.filter(category_id=i.category_id)
        product_list = list()
        for j in product:
            # 카테고리에 해당하는 '상품이름' 리스트 생성
            product_list.append(j)
        # i -> 카테고리, product_list -> 해당하는 품목 리스트
        # {i[0]:product_list, i[1]:product_list...i[n]:product_list} dictionary
        product_dict[i] = product_list

    if Size.objects.first() is not None:
        last_id = Size.objects.last().size_id + 1
    else:
        last_id = 1

    context["last_id"] = last_id
    context["size"] = page_obj
    context["max_index"] = max_index
    context["page"] = max_index
    context["count"] = pagecount
    context["kw"] = kw
    context["product_dict"] = product_dict
    context["member_no"] = memberno
    context["member_name"] = membername

    return render(request, 'size.html', context)


# size insert
def size_insert(request):
    size_product = request.GET['size_product']
    print(size_product)
    size_name = request.GET['size_name']
    size_price = request.GET['size_price']
    if size_product and size_name and size_price != "":
        rows = Size.objects.create(product_id_id=size_product, size_name=size_name, size_price=size_price)
        return redirect('information:size_view')
    else:
        return redirect('information:size_view')


# size update
@csrf_exempt
def size_update(request):
    context = {}

    size_id = request.GET['id']
    size_name = request.GET['name']
    size_price = request.GET['price']
    print(size_name)
    print(size_price)

    size = Size.objects.get(size_id=size_id)
    if size_name != "":
        size.size_name = size_name
    if size_price != "":
        size.size_price = size_price
    size.save()

    context['flag'] = '0'
    context['result_msg'] = '수정되었습니다'

    return JsonResponse(context, content_type="application/json")


# size delete
def size_delete(request):
    size_id = request.GET['size_id']
    rows = Size.objects.get(size_id=size_id).delete()

    return redirect('information:size_view')
