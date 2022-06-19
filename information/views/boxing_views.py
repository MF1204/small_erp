from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Boxing


# boxing

# modal view
@csrf_exempt
def boxing_get(request):
    boxing_id = request.GET['boxing_id']
    box = Boxing.objects.get(boxing_id = boxing_id)
    data = model_to_dict(box)
    print(data)

    return JsonResponse(data, content_type="application/json")


# page view
def boxing_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    rsBoard = Boxing.objects.all().order_by('-boxing_id')

    if Boxing.objects.first() is not None:
        last_id = Boxing.objects.last().boxing_id + 1
    else:
        last_id = 1

    context = {"last_id": last_id, "boxing_table": rsBoard, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'boxing.html', context)


# boxing insert
def boxing_insert(request):
    boxing_name = request.GET['boxing_name']
    boxing_price = request.GET['boxing_price']
    if boxing_name and boxing_price != "":
        rows = Boxing.objects.create(boxing_name=boxing_name, boxing_price=boxing_price)
        return redirect('information:boxing_view')
    else:
        return redirect('information:boxing_view')


# boxing update
def boxing_update(request):
    boxing_id = request.GET['boxing_id']
    boxing_name = request.GET['boxing_name']
    boxing_price = request.GET['boxing_price']

    try:
        box = Boxing.objects.get(boxing_id = boxing_id)
        if boxing_name != "":
            box.boxing_name = boxing_name
        if boxing_price != "":
            box.boxing_price = boxing_price

        try:
            box.save()
            return redirect('information:boxing_view')
        except ValueError:
            return HttpResponse({"success": False, "msg":"에러가 발생했습니다"})

    except ObjectDoesNotExist:
        return HttpResponse({"success": False, "msg": "정보가 존재하지 않습니다"})


# boxing delete
def boxing_delete(request):
    boxing_id = request.GET['boxing_id']
    rows = Boxing.objects.get(boxing_id=boxing_id).delete()

    return redirect('information:boxing_view')