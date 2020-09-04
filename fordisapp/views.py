from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.hashers import make_password, check_password
from .models import Users, Article, Comment, Comment2
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count, Sum
from datetime import datetime
import json
import requests

# 사용자 로긴 체크 후 사용자 정보를 모두 context에 담음
def logincheck(request) :
    context = None
    if 'user' in request.session:
        user = Users.objects.get(userEmail=request.session.get('user'))

        context = {'loginyn':True,
                   'useremail':user.userEmail,
                   'nickname': user.nickName,
                   'photopath': user.photo.url,
                   'guardianName':  user.guardianName,
                   'guardianCallNum': user.guardianCallNum,
                   'guardianBasicMsg': user.guardianBasicMsg
                   }
        return context
    else:
        context = {'loginyn': False}
        return context


############################################# Users #############################################
def index(request) :
        return render(request, 'index.html', logincheck(request))


def register(request):
    if request.method =='GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        userEmail = request.POST.get('userEmail', None)
        nickName = request.POST.get('nickName', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)
        photo = request.FILES['photo']
        guardianName = request.POST.get('guardianName', None)
        guardianCallNum = request.POST.get('guardianCallNum', None)
        guardianBasicMsg = request.POST.get('guardianBasicMsg', None)
        res_data = {}
        if not (userEmail and password and re_password and nickName):
            res_data['error']='아이디 또는 패스워드를 입력해주세요.'
        elif password != re_password:
            res_data['error']='비밀번호가 다릅니다.'
        else:
            users = Users(
                userEmail=userEmail,
                nickName=nickName,
                password=make_password(password),
                photo=photo,
                guardianName=guardianName,
                guardianCallNum=guardianCallNum,
                guardianBasicMsg=guardianBasicMsg
            )
            users.save()
            user2 = Users.objects.get(userEmail=userEmail)
            request.session['user'] = user2.userEmail
            return redirect('index')
        return render(request, 'register.html', res_data)


def login(request):
    context = None
    if request.method == "POST":
        userEmail = request.POST.get('userEmail', None)
        password = request.POST.get('password', None)
        try :
            user = Users.objects.get(userEmail=userEmail)
        except Users.DoesNotExist :
            context = {'error': '계정을 확인하세요'}
        else :
            if check_password(password, user.password):
                request.session['user'] = user.userEmail
                return redirect('index')
            else :
                context = { 'error' : '패스워드를 확인하세요'}
    else :
        if 'user' in request.session:
            context = {'msg': '이미 %s 로그인 하셨습니다.' % request.session['user'] }
    return render(request, 'login.html', context)


def logout(request):
    if 'user' in request.session :
        del request.session['user']
        context = {'msg' : '로그아웃 완료'}
    else :
        context = {'msg': '로그인 상태가 아닙니다!'}
    return render(request, 'logout.html', context)

############################################# board ##################################################
def board(request):
    if logincheck(request)['loginyn']:
        page = request.GET.get('page', 1)
        # articles = Article.objects.all().order_by('-id')
        articles = Article.objects.filter(boardType="B").annotate(cmtcnt=Count("comment__id", distinct=True) + Count("comment__comment2__id", distinct=True)).all().order_by('-id')
        paginator = Paginator(articles, 10)
        nlistpage = paginator.get_page(page)
        context = {'articles': nlistpage}
        context.update(logincheck(request))
        return render(request, 'board.html', context)
    else:
        return render(request, 'login.html', logincheck(request))


def report(request):
    if logincheck(request)['loginyn']:
        page = request.GET.get('page', 1)
        # articles = Article.objects.all().order_by('-id')
        articles = Article.objects.filter(boardType="R").annotate(cmtcnt=Count("comment__id", distinct=True) + Count("comment__comment2__id", distinct=True)).all().order_by('-id')
        paginator = Paginator(articles, 6)
        nlistpage = paginator.get_page(page)
        context = {'articles': nlistpage}
        context.update(logincheck(request))
        return render(request, 'report.html', context)
    else:
        context = {'loginyn': False}
        return render(request, 'login.html', context)


def detail(request, btype, pk):
    if logincheck(request)['loginyn']:
        article = Article.objects.get(pk=pk)
        # session에 이미 본 article의 pk를 저장해서 조회수를 관리 (로그인/아웃을 해서 조회수를 올리면 정성을 인정해 줌)
        if 'viewcnt' not in request.session:    # viewcnt 없음
            request.session['viewcnt'] = str(pk) + '|'
            article.viewcnt += 1
            article.save()
        else:                                   # viewcnt 있음
            viewlist = request.session['viewcnt'].split('|')
            if str(pk) not in viewlist:
                request.session['viewcnt'] =  request.session['viewcnt'] + str(pk) + '|'
                article.viewcnt += 1
                article.save()

        article2 = Article.objects.get(pk=pk)       # 리스트용
        article3 = Article.objects.filter(id=pk).aggregate(cmtcnt=Count("comment__id", distinct=True) + Count("comment__comment2__id", distinct=True)) #댓글수용
        context = {
            'article': article2,
            'article3': article3,
            'btype': btype
        }
        context.update(logincheck(request))
        return render(request, 'detail.html', context)
    else:
        return render(request, 'login.html', logincheck(request))


def create(request, btype):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = Users.objects.get(userEmail=request.session['user'])
        if btype == 'R':
            reportphoto = request.FILES['reportphoto']
            reportlati = request.POST['reportlati']
            reportlong = request.POST['reportlong']
            reportaddress = request.POST['reportaddress']
            reportphotoid = user.userEmail + datetime.now().isoformat()
        else:
            reportphoto = None
            reportlati = None
            reportlong = None
            reportaddress = None
            reportphotoid = None

        viewcnt = 0
        article = Article(title=title, content=content, awriter=user, viewcnt=viewcnt, reportPhotoId=reportphotoid, reportPhoto=reportphoto, reportLati=reportlati, reportLong=reportlong, reportAddress=reportaddress, boardType=btype)
        article = article.save()
        # return redirect('board')
        # return redirect('{}#move_{}'.format(resolve_url('board'), 'board'))
        #report 개발중
        #return redirect('{}#{}'.format(resolve_url('board'), 'board'))
        if btype == 'R':
            return redirect('{}#{}'.format(resolve_url('report'), 'board'))
        else:
            return redirect('{}#{}'.format(resolve_url('board'), 'board'))
    else:
        if logincheck(request)['loginyn']:
            context = {'btype': btype}
            context.update(logincheck(request))
            return render(request, 'create.html', context)
            # return render(request, '{}#{}'.format(resolve_url('create'), 'board'), context)
        else:
            return render(request, 'login.html', logincheck(request))


def comment_create(request, btype, pk):
    article = Article.objects.get(pk=pk)
    content = request.POST['content']
    user = Users.objects.get(userEmail=request.session['user'])
    comment = Comment(content=content, cwriter = user, article=article)
    comment.save()
    # return redirect('detail', pk)
    return redirect('{}#movec_{}'.format(resolve_url('detail', btype, pk), comment.pk))
    #return redirect('{}#{}'.format(resolve_url('detail', btype, pk), 'board'))


def comment2_create(request, btype, ppk, pk):
    comment = Comment.objects.get(pk=pk)
    content = request.POST['content']
    user = Users.objects.get(userEmail=request.session['user'])
    comment2 = Comment2(content=content, c2writer = user, comment=comment)
    comment2.save()
    # return redirect('detail', ppk)
    return redirect('{}#movec_{}'.format(resolve_url('detail', btype, ppk), comment.pk))
    #return redirect('{}#{}'.format(resolve_url('detail', btype, ppk), 'board'))


def update(request, btype, pk):
        if logincheck(request)['loginyn']:
            article = Article.objects.get(pk=pk)
            if request.method == 'POST':
                title = request.POST['title']
                content = request.POST['content']
                photochanged = request.POST['photochangedid']
                article.title = title
                article.content = content
                if btype == 'R':
                    if photochanged == 'Y':
                        article.reportPhoto = request.FILES['reportphoto']
                        article.reportPhotoId = logincheck(request)['useremail'] + datetime.now().isoformat()
                        article.reportAddress = request.POST['reportaddress']
                    else:
                        article.reportAddress = request.POST['reportaddress']


                article.save()

                # return redirect('detail', article.pk)
                return redirect('{}#{}'.format(resolve_url('detail', btype, article.pk), 'board'))
            else:
                article3 = Article.objects.filter(id=pk).aggregate(
                    cmtcnt=Count("comment__id", distinct=True) + Count("comment__comment2__id", distinct=True))  # 댓글수용
                context = {
                    'article': article,
                    'btype': btype,
                    'article3':article3
                }
                context.update(logincheck(request))
                return render(request, 'update.html', context)
        else:
            return render(request, 'login.html', logincheck(request))


def comment_update(request, btype, article_pk, comment_pk):
    if logincheck(request)['loginyn']:
        comment = Comment.objects.get(pk=comment_pk)
        if request.method == 'POST':
            content = request.POST['content']
            comment.content = content
            comment.save()
            # return redirect('detail', article.pk)
            return redirect('{}#{}'.format(resolve_url('detail', btype, article_pk), 'board'))
        else:
            context = {
                'article': comment,
                'btype': btype
            }
            context.update(logincheck(request))
            return render(request, 'update.html', context)
    else:
        return render(request, 'login.html', logincheck(request))


def comment2_update(request, btype, article_pk, comment_pk, comment2_pk):
    if logincheck(request)['loginyn']:
        comment2 = Comment2.objects.get(pk=comment2_pk)
        if request.method == 'POST':
            comment = request.POST['content']
            comment2.content = comment
            comment2.save()
            # return redirect('detail', article.pk)
            return redirect('{}#{}'.format(resolve_url('detail', btype, article_pk), 'board'))
        else:
            context = {
                'article': comment2,
                'btype': btype
            }
            context.update(logincheck(request))
            return render(request, 'update.html', context)
    else:
        return render(request, 'login.html', logincheck(request))


def delete(request, btype, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    # return redirect('board')
    if btype == 'R':
        return redirect('{}#{}'.format(resolve_url('report'), 'board'))
    else:
        return redirect('{}#{}'.format(resolve_url('board'), 'board'))


def comment_delete(request, btype, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    # return redirect('detail', article_pk)
    return redirect('{}#{}'.format(resolve_url('detail', btype, article_pk), 'board'))


def comment2_delete(request, btype, article_pk, comment_pk, comment2_pk):
    comment = Comment2.objects.get(pk=comment2_pk)
    comment.delete()
    # return redirect('detail', article_pk)
    return redirect('{}#{}'.format(resolve_url('detail', btype, article_pk), 'board'))


def search1(request, btype, nickname):
    page = request.GET.get('page', 1)
    articles = Article.objects.filter(boardType=btype, awriter__nickName=nickname).annotate(cmtcnt=Count("comment__id", distinct=True) + Count("comment__comment2__id", distinct=True)).all().order_by('-id')
    paginator = Paginator(articles, 10)
    nlistpage = paginator.get_page(page)
    context = {'articles': nlistpage,
               'btype': btype
               }
    context.update(logincheck(request))

    if btype == 'R':
        return render(request, 'report.html', context)
    else:
        return render(request, 'board.html', context)


def search2(request, btype, content):
    page = request.GET.get('page', 1)
    articles = Article.objects.filter(boardType=btype, content__contains=content).annotate(cmtcnt=Count("comment__id", distinct=True) + Count("comment__comment2__id", distinct=True)).all().order_by('-id')
    paginator = Paginator(articles, 3)
    nlistpage = paginator.get_page(page)
    context = {'articles': nlistpage,
               'btype': btype
               }
    context.update(logincheck(request))
    if btype == 'R':
        return render(request, 'report.html', context)
    else:
        return render(request, 'board.html', context)

def checknick(request):
        nickname = request.GET.get("nickname")
        try :
            user = Users.objects.get(nickName=nickname)
        except Users.DoesNotExist :
            userable = True
        else :
            userable = False

        jsonContent = {"userable" : userable}
        return JsonResponse( jsonContent, json_dumps_params={'ensure_ascii': False})


def checkuseremail(request):
    useremail = request.GET.get("useremail")
    try:
        user = Users.objects.get(userEmail=useremail)
    except Users.DoesNotExist:
        userable = True
    else:
        userable = False

    jsonContent = {"userable": userable}
    return JsonResponse(jsonContent, json_dumps_params={'ensure_ascii': False})

def getaccesstoken(request):
    url = "https://kauth.kakao.com/oauth/token"         # 수정 X
    dataString = "grant_type=authorization_code"        # 수정 X
    dataString += "&client_id=" + "1af4a3b899028e9720c99fc752d7986c"       # 수정 O  API Key
    dataString += "&redirect_uri=http://localhost:8000/fordisapp/&code="   # 수정 O  redirect_url
    dataString += "rqtjpaPM8iMz3TvfqKHGuD8eduHGwWu8C-NynGMHX47RwgHaxshrGUvQRbCxIP0Z0tbFcwo9cxgAAAF0Tfq3Hg"     # 수정 O  code값
    headers = {
        'Content-Type' : "application/x-www-form-urlencoded",
        'Cache-Control' : "no-cache",
    }
    reponse = requests.request("POST",url,data=dataString, headers=headers)
    access_token = json.loads(((reponse.text).encode('utf-8')))

    # access_token = dataString
    context = {'access_token': access_token}
    return render(request, 'getaccesstoken.html', context)


def getaddresstest(request):
    result = getLatLng('서울 강남구 압구정동 101-7')
    match_first = result['documents'][0]['address']
    context = {'x': float(match_first['x']), 'y': float(match_first['y'])}
    return render(request, 'getaccesstoken.html', context)


def getLatLng(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
    headers = {"Authorization": "KakaoAK 961e75bf4e70089fb39e1d8bf3e1e1ac"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    return result