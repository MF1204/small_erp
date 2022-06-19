from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
# ajax
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Member


# employee


# page view
def employee_view(request):

    if request.session.has_key('member_no'):
        memberno = request.session['member_no']
        membername = request.session['member_name']
        memberauth = request.session['member_auth']
        if memberauth != '관리자':
            return redirect('information:product_view')
    else:
        return redirect('accounts:signin')

    rsBoard = Member.objects.all().order_by('-member_no')

    context = {"member_table": rsBoard, "member_no": memberno, "member_name": membername, "member_auth": memberauth}

    return render(request, 'employee.html', context)


# employee update
@csrf_exempt
def emp_update(request):
    context = {}
    # 전달받은 인자
    member_no = request.GET['member_no']
    member_rank = request.GET['member_rank']
    hiredate = request.GET['hiredate']
    resignationdate = request.GET['resignationdate']
    member_auth = request.GET['member_auth']
    # DB 수정
    member = Member.objects.get(member_no=member_no)
    member.member_rank = member_rank
    member.hiredate = hiredate
    member.resignationdate = resignationdate
    member.member_auth = member_auth
    # 수정사항 저장
    member.save()

    context['flag'] = '0'
    context['result_msg'] = '수정되었습니다'
    return JsonResponse(context, content_type="application/json")


# employee delete
@csrf_exempt
def emp_delete(request):
    context = {}
    member_no = request.GET['member_no']
    rows = Member.objects.get(member_no=member_no).delete()

    context["result_msg"] = "삭제되었습니다"
    return JsonResponse(context, content_type="application/json")