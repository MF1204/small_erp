from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Member, SessionMatch
from django.contrib.sessions.models import Session
from datetime import datetime
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import json


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

    rs = Member.objects.filter(member_id=member_id, member_pw=member_pw)

    if (len(rs)) == 0:
        context['flag'] = '1'
        context['result_msg'] = '등록되지 않은 사용자입니다.'

    else:
        member = Member.objects.get(member_id=member_id, member_pw=member_pw)

        sessionmatch = SessionMatch.objects.filter(member=member)
        if len(sessionmatch) != 0:
            context['flag'] = '400'
            context['result_msg'] = '다른 기기에서 로그인중입니다.\n현재 기기에서 로그인 하시겠습니까?'
            return JsonResponse(context, content_type="application/json")

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
    member_no = ''
    if request.session.has_key('member_no'):
        memberno = request.session['member_no']

    member = Member.objects.get(member_no=memberno)
    member.access_latest = datetime.now()
    member.save()
    session_delete(member.member_id)

    request.session.flush()

    return redirect('accounts:signin')


def session_match(session_key, memberno):
    member = Member.objects.get(member_no=memberno)

    try:
        confirm_session_key = SessionMatch.objects.get(member=member, session_key=session_key)
    except ObjectDoesNotExist:
        session_table = SessionMatch.objects.create(member=member, session_key=session_key)

    return


def session_delete(memberid):
    member = Member.objects.get(member_id=memberid)
    session_table = SessionMatch.objects.filter(member=member)
    session_value = session_table.values()
    sessionkey_list = set()
    for sessionlist in session_value:
        session_key = sessionlist['session_key']
        sessionkey_list.add(session_key)
    session_table.delete()
    sessionkey_list = list(sessionkey_list)
    for session_key in sessionkey_list:
        django_session = Session.objects.get(session_key=session_key)
        django_session.delete()
    return


def other_logout(request):
    context = {}
    jsondata = json.loads(request.body.decode('utf-8'))
    flag = jsondata['flag']

    if flag != 1:
        context['flag'] = False
        return JsonResponse(context, content_type="application/json")

    member_id = jsondata['member_id']
    session_delete(member_id)
    context['flag'] = True
    return JsonResponse(context, content_type="application/json")
