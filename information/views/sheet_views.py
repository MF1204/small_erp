from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ..models import Sheet


# sheet


# page view
def sheet_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
    else:
        return redirect('accounts:signin')

    rsBoard = Sheet.objects.all().order_by('-sheet_id')

    if Sheet.objects.first() is not None:
        last_id = Sheet.objects.last().sheet_id + 1
    else:
        last_id = 1

    context = {"last_id": last_id, "sheet_table": rsBoard, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'sheets.html', context)


# sheet insert
def sheet_insert(request):
    sheet_name = request.GET['sheet_name']
    sheet_price = request.GET['sheet_price']
    if sheet_name and sheet_price != "":
        rows = Sheet.objects.create(sheet_name=sheet_name, sheet_price=sheet_price)
        return redirect('information:sheet_view')
    else:
        return redirect('information:sheet_view')


# sheet update
@csrf_exempt
def sheet_update(request):
    context = {}

    sheet_id = request.GET['id']
    sheet_name = request.GET['name']
    sheet_price = request.GET['price']

    sheet = Sheet.objects.get(sheet_id=sheet_id)
    if sheet_name != "":
        sheet.sheet_name = sheet_name
    if sheet_price != "":
        sheet.sheet_price = sheet_price
    sheet.save()

    context['flag'] = '0'
    context['result_msg'] = '수정되었습니다'

    return JsonResponse(context, content_type="application/json")


# sheet delete
def sheet_delete(request):
    sheet_id = request.GET['sheet_id']
    rows = Sheet.objects.get(sheet_id=sheet_id).delete()

    return redirect('information:sheet_view')
