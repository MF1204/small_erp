from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Delivery


# delivery

# modal view
@csrf_exempt
def delivery_get(request):
    delivery_id = request.GET['delivery_id']
    delivery = Delivery.objects.get(delivery_id = delivery_id)
    data = model_to_dict(delivery)
    print(data)

    return JsonResponse(data, content_type="application/json")


# page view
def delivery_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')


    rsBoard = Delivery.objects.all().order_by('-delivery_id')

    if Delivery.objects.first() is not None:
        last_id = Delivery.objects.last().delivery_id + 1
    else:
        last_id = 1

    context = {"last_id": last_id, "delivery_table": rsBoard, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'delivery.html', context)


# delivery insert
def delivery_insert(request):
    delivery_name = request.GET['delivery_name']
    delivery_price = request.GET['delivery_price']
    if delivery_name and delivery_price != "":
        rows = Delivery.objects.create(delivery_name=delivery_name, delivery_price=delivery_price)
        return redirect('information:delivery_view')
    else:
        return redirect('information:delivery_view')


# delivery update
def delivery_update(request):
    delivery_id = request.GET['delivery_id']
    delivery_name = request.GET['delivery_name']
    delivery_price = request.GET['delivery_price']

    try:
        delivery = Delivery.objects.get(delivery_id = delivery_id)
        if delivery_name != "":
            delivery.delivery_name = delivery_name
        if delivery_price != "":
            delivery.delivery_price = delivery_price

        try:
            delivery.save()
            return redirect('information:delivery_view')
        except ValueError:
            return HttpResponse({"success": False, "msg":"에러가 발생했습니다"})

    except ObjectDoesNotExist:
        return HttpResponse({"success": False, "msg": "정보가 존재하지 않습니다"})


# delivery delete
def delivery_delete(request):
    delivery_id = request.GET['delivery_id']
    rows = Delivery.objects.get(delivery_id=delivery_id).delete()

    return redirect('information:delivery_view')