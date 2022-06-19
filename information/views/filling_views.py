from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Filling


# filling

# modal view
@csrf_exempt
def filling_get(request):
    filling_id = request.GET['filling_id']
    filling = Filling.objects.get(filling_id = filling_id)
    data = model_to_dict(filling)
    print(data)

    return JsonResponse(data, content_type="application/json")


# page view
def filling_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    rsBoard = Filling.objects.all().order_by('-filling_id')

    if Filling.objects.first() is not None:
        last_id = Filling.objects.last().filling_id + 1
    else:
        last_id = 1

    context = {"last_id": last_id, "filling_table": rsBoard, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'filling.html', context)


# filling insert
def filling_insert(request):
    filling_name = request.GET['filling_name']
    filling_price = request.GET['filling_price']
    if filling_name and filling_price != "":
        rows = Filling.objects.create(filling_name=filling_name, filling_price=filling_price)
        return redirect('information:filling_view')
    else:
        return redirect('information:filling_view')


# filling update
def filling_update(request):
    filling_id = request.GET['filling_id']
    filling_name = request.GET['filling_name']
    filling_price = request.GET['filling_price']

    try:
        filling = Filling.objects.get(filling_id = filling_id)
        if filling_name != "":
            filling.filling_name = filling_name
        if filling_price != "":
            filling.filling_price = filling_price

        try:
            filling.save()
            return redirect('information:filling_view')
        except ValueError:
            return HttpResponse({"success": False, "msg":"에러가 발생했습니다"})

    except ObjectDoesNotExist:
        return HttpResponse({"success": False, "msg": "정보가 존재하지 않습니다"})


# filling delete
def filling_delete(request):
    filling_id = request.GET['filling_id']
    rows = Filling.objects.get(filling_id=filling_id).delete()

    return redirect('information:filling_view')