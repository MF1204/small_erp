from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Order_type


# Order_type

# modal view
@csrf_exempt
def order_type_get(request):
    order_type_id = request.GET['order_type_id']
    order_type = Order_type.objects.get(order_type_id = order_type_id)
    data = model_to_dict(order_type)
    print(data)

    return JsonResponse(data, content_type="application/json")


# page view
def order_type_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    rsBoard = Order_type.objects.all().order_by('-order_type_id')

    if Order_type.objects.first() is not None:
        last_id = Order_type.objects.last().order_type_id + 1
    else:
        last_id = 1

    context = {"last_id": last_id, "order_type_table": rsBoard, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'order_type.html', context)


# Order_type insert
def order_type_insert(request):
    order_type_name = request.GET['order_type_name']
    if order_type_name != "":
        rows = Order_type.objects.create(order_type_name=order_type_name)
        return redirect('information:order_type_view')
    else:
        return redirect('information:order_type_view')


# Order_type update
def order_type_update(request):
    order_type_id = request.GET['order_type_id']
    order_type_name = request.GET['order_type_name']

    try:
        filling = Order_type.objects.get(order_type_id = order_type_id)
        if order_type_name != "":
            order_type.order_type_name = order_type_name
        try:
            order_type.save()
            return redirect('information:order_type_view')
        except ValueError:
            return HttpResponse({"success": False, "msg":"에러가 발생했습니다"})

    except ObjectDoesNotExist:
        return HttpResponse({"success": False, "msg": "정보가 존재하지 않습니다"})


# Order_type delete
def order_type_delete(request):
    order_type_id = request.GET['order_type_id']
    rows = Order_type.objects.get(order_type_id=order_type_id).delete()

    return redirect('information:order_type_view')