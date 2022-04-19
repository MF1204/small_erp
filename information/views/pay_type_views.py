from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Pay_type


# Pay_type

# modal view
@csrf_exempt
def pay_type_get(request):
    pay_type_id = request.GET['pay_type_id']
    pay_type = Pay_type.objects.get(pay_type_id = pay_type_id)
    data = model_to_dict(pay_type)
    print(data)

    return JsonResponse(data, content_type="application/json")


# page view
def pay_type_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    rsBoard = Pay_type.objects.all().order_by('-pay_type_id')

    if Pay_type.objects.first() is not None:
        last_id = Pay_type.objects.last().pay_type_id + 1
    else:
        last_id = 1

    context = {"last_id": last_id, "pay_type_table": rsBoard, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'pay_type.html', context)


# Pay_type insert
def pay_type_insert(request):
    pay_type_name = request.GET['pay_type_name']
    if pay_type_name != "":
        rows = Pay_type.objects.create(pay_type_name=pay_type_name)
        return redirect('information:pay_type_view')
    else:
        return redirect('information:pay_type_view')


# Pay_type update
def pay_type_update(request):
    pay_type_id = request.GET['pay_type_id']
    pay_type_name = request.GET['pay_type_name']

    try:
        pay_type = Pay_type.objects.get(pay_type_id = pay_type_id)
        if pay_type_name != "":
            pay_type.pay_type_name = pay_type_name
        try:
            pay_type.save()
            return redirect('information:pay_type_view')
        except ValueError:
            return HttpResponse({"success": False, "msg":"에러가 발생했습니다"})

    except ObjectDoesNotExist:
        return HttpResponse({"success": False, "msg": "정보가 존재하지 않습니다"})


# Pay_type delete
def pay_type_delete(request):
    pay_type_id = request.GET['pay_type_id']
    rows = Pay_type.objects.get(pay_type_id=pay_type_id).delete()

    return redirect('information:pay_type_view')