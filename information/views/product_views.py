from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Category, Product


# product

# page view
def product_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    category = Category.objects.all().order_by('category_big')
    category_big = category.values("category_big").distinct()

    product = Product.objects.all().order_by('category_id__category_big')
    context = {"category_big": category_big, "category_table": category,
               "product_table": product, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'product.html', context)


@csrf_exempt
def category_mid_insert(request):
    context = {}
    category_big = request.GET['category_big']
    category_mid = request.GET['category_mid']

    if Category.objects.filter(category_mid=category_mid).exists():
        context["flag"] = "1"
        context["result_msg"] = "이미 존재하는 분류입니다"
        return JsonResponse(context, content_type="application/json")

    Category.objects.create(category_big=category_big, category_mid=category_mid)
    context["flag"] = "0"
    context["result_msg"] = "저장되었습니다"
    return JsonResponse(context, content_type="application/json")


# category update
@csrf_exempt
def category_update(request):
    context = {}
    category_id = request.GET['category_id']
    mid_category = request.GET['mid_category']

    midCategory = Category.objects.get(category_id=category_id)
    midCategory.category_mid = mid_category
    midCategory.save()

    context["flag"] = "0"
    context["result_msg"] = "수정되었습니다"
    return JsonResponse(context, content_type="application/json")


# category delete
@csrf_exempt
def category_delete(request):
    context = {}
    category_id = request.GET['category_id']

    midCategory = Category.objects.get(category_id=category_id).delete()

    context["result_msg"] = "삭제되었습니다"
    return JsonResponse(context, content_type="application/json")


# product insert
@csrf_exempt
def product_insert(request):
    context = {}
    category_id = request.GET['category_id']
    product_name = request.GET['product_name']
    product_price = request.GET['product_price']

    if Product.objects.filter(product_name=product_name).exists():
        context["flag"] = "1"
        context["result_msg"] = "이미 존재하는 상품입니다"
        return JsonResponse(context, content_type="application/json")

    Product.objects.create(category_id_id=category_id, product_name=product_name, product_price=product_price)
    context["flag"] = "0"
    context["result_msg"] = "저장되었습니다"
    return JsonResponse(context, content_type="application/json")


# product update
@csrf_exempt
def product_update(request):
    context = {}
    product_id = request.GET['product_id']
    category_id = request.GET['category_id']
    product_name = request.GET['product_name']
    product_price = request.GET['product_price']

    product = Product.objects.get(product_id=product_id)
    product.category_id_id = category_id
    product.product_name = product_name
    product.product_price = product_price
    product.save()

    context["flag"] = "0"
    context["result_msg"] = "수정되었습니다"
    return JsonResponse(context, content_type="application/json")


# product delete
@csrf_exempt
def product_delete(request):
    context = {}
    product_id = request.GET['product_id']

    Product.objects.get(product_id=product_id).delete()

    context["result_msg"] = "삭제되었습니다"
    return JsonResponse(context, content_type="application/json")
