from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Member
from datetime import datetime
from django.shortcuts import redirect


# Create your views here.


def member_register(request):
    return render(request, "signup.html")


@csrf_exempt
def member_idcheck(request):
    context = {}
    mid = request.GET['member_id']

    rs = Member.objects.filter(member_id=mid)
    if (len(rs)) > 0:
        context['flag'] = 1
        context['result_msg'] = '중복된 아이디입니다.'
    else:
        context['flag'] = 0
        context['result_msg'] = '사용 가능한 아이디입니다.'

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def member_insert(request):
    context = {}
    member_id = request.GET['member_id']
    member_pw = request.GET['member_pw']
    member_name = request.GET['member_name']
    member_rank = request.GET['rank']
    member_auth = request.GET['auth']
    if member_auth != '0812':
        member_auth = '사원'
    else:
        member_auth = '관리자'
    hiredate = request.GET['hiredate']

    rs = Member.objects.create(member_id=member_id,
                               member_pw=member_pw,
                               member_name=member_name,
                               member_rank=member_rank,
                               member_auth=member_auth,
                               hiredate=hiredate,
                               access_latest=hiredate,
                               register_date=datetime.now()
                               )

    context['result_msg'] = '회원가입이 완료되었습니다.'

    return JsonResponse(context, content_type="application/json")


# 로그인 뷰
def signin_view(request):
    return render(request, "login.html")


@csrf_exempt
def member_login(request):
    context = {}
    member_id = request.GET['member_id']
    member_pw = request.GET['member_pw']

    if 'member_no' in request.session:
        context['flag'] = '1'
        context['result_msg'] = '로그인 중복 에러'

    else:
        rs = Member.objects.filter(member_id=member_id, member_pw=member_pw)

        if (len(rs)) == 0:
            context['flag'] = '1'
            context['result_msg'] = '등록되지 않은 사용자입니다.'

        else:
            member = Member.objects.get(member_id=member_id, member_pw=member_pw)
            member_no = member.member_no
            member_name = member.member_name
            member_auth = member.member_auth
            member.access_latest = datetime.now()
            member.save()

            request.session['member_no'] = member_no
            request.session['member_name'] = member_name
            request.session['member_auth'] = member_auth

            context['flag'] = '0'
            context['result_msg'] = '로그인 되었습니다.'

    return JsonResponse(context, content_type="application/json")


def member_logout(request):
    # 로그아웃하는 시간 저장
    member_no = ''
    if request.session.has_key('member_no'):
        memberno = request.session['member_no']

    member = Member.objects.get(member_no=memberno)
    member.access_latest = datetime.now()
    member.save()

    # 세션 만료
    request.session.flush()

    return redirect('accounts:signin')
