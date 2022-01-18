# html 화면 렌더링 및 화면이동, 객체추출
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# 필요한 Class
from productTrade.models import Content, Member, Comment, DropoutMember
from productTrade.forms import RegisterForm, ContentForm, LoginForm, CommentForm, UserUpdateForm, PasswordUpdateForm, CheckPasswordForm

# 화면 메세지 전송
from django.contrib import messages

# django 인증(회원가입, 로그인, 로그아웃)
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash


import os # 시스템 라이브러리
from django.conf import settings

from django.core.paginator import Paginator # 페이지 분할

import pymysql # python과 mysql 연동

# 로거 사용
import logging
logger = logging.getLogger('error')

# 공통 영역
import common.common


# Create your views here.


def contentList(request):
    if request.method == 'POST':
        word = request.POST['word']
        print(word)
        
        contents = Content.objects.filter(title__icontains=word) | Content.objects.filter(text__icontains=word) | Content.objects.filter(writer_id__username__icontains=word)
        print(contents)
        paginator = Paginator(contents, 6)
        
        # 사용자에게 받은 page 파라미터에 맞는 페이지를 전달
        page = request.GET.get('page')
        items = paginator.get_page(page)
        
        preprepage = 0
        nexnexpage = 0
        
        if items.has_previous():
            preprepage = items.previous_page_number() - 1
        if items.has_next():
            nexnexpage = items.next_page_number() + 1
        
        context = {
            'contents':items,
            'prepre' : preprepage,
            'nexnex' : nexnexpage,
        }
        
        return render(request, 'productTrade/ContentList.html', context)
        
    if request.method == 'GET':
        contents = Content.objects.all().order_by('-id')
        paginator = Paginator(contents, 6)

        # 사용자에게 받은 page 파라미터에 맞는 페이지를 전달
        page = request.GET.get('page')
        items = paginator.get_page(page)
        
        preprepage = 0
        nexnexpage = 0
        
        if items.has_previous():
            preprepage = items.previous_page_number() - 1
        if items.has_next():
            nexnexpage = items.next_page_number() + 1
        
        context = {
            'contents':items,
            'prepre' : preprepage,
            'nexnex' : nexnexpage,
        }
        return render(request, 'productTrade/ContentList.html', context)
    return render(request, 'productTrade/ContentList.html')


def indicontentList(request):
    if request.method == 'POST':
        word = request.POST['word']
        print('logger = ', logger)
        logger.error('logger using test')
        
        contents = Content.objects.filter(title__icontains=word) | Content.objects.filter(text__icontains=word) | Content.objects.filter(writer_id__username__icontains=word)
        paginator = Paginator(contents, 6)
        
        # 사용자에게 받은 page 파라미터에 맞는 페이지를 전달
        page = request.GET.get('page')
        items = paginator.get_page(page)
        
        preprepage = 0
        nexnexpage = 0
        
        if items.has_previous():
            preprepage = items.previous_page_number() - 1
        if items.has_next():
            nexnexpage = items.next_page_number() + 1
        
        context = {
            'contents':items,
            'prepre' : preprepage,
            'nexnex' : nexnexpage,
        }
        
        return render(request, 'productTrade/IndiContentList.html', context)
        
    if request.method == 'GET':
        contents = Content.objects.all().order_by('-id')
        paginator = Paginator(contents, 6)
        logger.error('error log')
        
        '''
        # is_anonymous: 사용자가 로그아웃 된 상태일 때 True 반환
        if request.user.is_anonymous:
            print('aa')
        '''
        
        # 사용자에게 받은 page 파라미터에 맞는 페이지를 전달
        page = request.GET.get('page')
        items = paginator.get_page(page)
        row = items.number//5 + 1
        if (items.number%5 == 0):
            row = items.number // 5
        left = row*5-5
        right = row*5+1
        range_for = range(row*5-4, row*5+1)
        print(items.number, row)

        '''
        preprepage = 0
        nexnexpage = 0
        
        if items.has_previous():
            preprepage = items.previous_page_number() - 1
        if items.has_next():
            nexnexpage = items.next_page_number() + 1
        '''

        context = {
            'contents': items,
            #'prepre' : preprepage,
            #'nexnex' : nexnexpage,
            'row': row,
            'left': left,
            'right': right,
            'range_for': range_for,
            'total_page_num': paginator.num_pages,
            'request_page': items.number,
        }
        return render(request, 'productTrade/IndiContentList.html', context)
    

def create_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        
        # 유효성 검사
        if form.is_valid() :
            new_item = form.save()
            tmp = Content.objects.latest('id').id
            
            name = os.path.join(settings.MEDIA_ROOT,'productTrade/contentImages', str(request.FILES['image']))
            newname = os.path.join(settings.MEDIA_ROOT, 'productTrade/contentImages', 'content_id_{}.jpg'.format(tmp))
            os.rename(name, newname)
                     
            return redirect('indicontentList')
    
    item = get_object_or_404(Member, pk=request.user)
    form = ContentForm(initial={'writer_id': item})
    return render(request, 'productTrade/CreateContent.html', {'form':form})


def show_content(request, contentid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # 유효성 검사
        if form.is_valid() :
            new_item = form.save()
            return redirect('show_content', contentid=contentid)
    
    
    content = get_object_or_404(Content, pk=contentid)
    form = ContentForm(instance=content)
    commentForm = CommentForm(initial={'content_id': contentid ,'commenter_id': request.user })
    commentAll = Comment.objects.filter(content_id=content).all()
    # imgpath = '/media/로 시작'
    imgpath = '/media/productTrade/contentImages/content_id_{}.jpg'.format(contentid)
    
    context = {'item':content, 'form':form, 'commentform':commentForm, 'contentid':contentid, 'comments':commentAll, 'imgpath':imgpath}
    
    return render(request, 'productTrade/Content.html', context)


def show_Nologin_content(request, contentid):
    if request.method == 'GET':
        content = get_object_or_404(Content, pk=contentid)
        commentAll = Comment.objects.filter(content_id=content).all()
        # imgpath = '/media/로 시작'
        imgpath = '/media/productTrade/contentImages/content_id_{}.jpg'.format(contentid)

        context = {'item':content, 'contentid':contentid, 'comments':commentAll, 'imgpath':imgpath}

        return render(request, 'productTrade/noLogin_Content.html', context)


def register(request):
    # 사용자가 회원가입을 위해 정보를 전달
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # 유효성 검사
        if form.is_valid() :
            user = form.save()
            auth.login(request, user)
            return redirect('indicontentList')
        return redirect('register')
    else: #GET
        form = RegisterForm()
        return render(request, 'productTrade/Register.html', {'form':form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, data=request.POST)
        # 유효성 검사
        if form.is_valid() :
            user_id = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = auth.authenticate(
                request=request,
                username=user_id,
                password=password
            )
            
            if user is not None:
                auth.login(request, user)
                return redirect('indicontentList')
            else:
                return render(request, "productTrade/Login.html", {
                    'error': 'Username or Password is incorrect.',
                })
        return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'productTrade/Login.html', {'form':form})
    
    
def logout(request):
    auth.logout(request)
    return redirect('contentList')


def mypage(request):
    if request.method == 'POST':
        pass
    
    item1 = get_object_or_404(Member, pk=request.user)
    item2 = Content.objects.filter(writer_id=request.user).all()
    item3 = Comment.objects.filter(commenter_id=request.user).all()
    
    # Queryset에 하나씩 접근하기 위해
    tmp = []
    for comment in item3:
        tmp.append(comment.content_id_id)
    
    # map함수 사용
    def get_content(n):
        return get_object_or_404(Content, pk=n)
    item4 = list(map(get_content,tmp))
    user_comment_tbl = dict(zip(item3, item4))
    
    context = {
        'user': item1,
        'contents': item2,
        'user_comment_tbl':user_comment_tbl,
    }
    return render(request, 'productTrade/Mypage.html', context)


def update_comment(request, contentid, commentid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # 유효성 검사
        if form.is_valid() :
            text = form.cleaned_data.get('text')
            
            # MySQL Connection 연결
            conn = pymysql.connect(host='localhost', user='root', password='ingo75348668', db='hyein_market', charset='utf8')

            # Connection으로부터 Cursor 생성
            curs = conn.cursor()
            
            # SQL문 실행
            sql = "update hyein_market.producttrade_comment set text = '" + text + "' where id = " + str(commentid) + ";"
            print(curs.execute(sql))

            # 데이터 저장
            conn.commit()
            
            '''
            
            # 데이터 Fetch
            rows = curs.fetchall()
            print (rows)
            '''
            
            # Connection 닫기
            conn.close()
            
            return redirect('show_content', contentid=contentid)
            
    else: # GET
        content = get_object_or_404(Content, pk=contentid)
        form = ContentForm(instance=content)
        commentForm = CommentForm(initial={'content_id': contentid ,'commenter_id': request.user })
        commentAll = Comment.objects.filter(content_id=content).all()
        # imgpath = '/media/로 시작'
        imgpath = '/media/productTrade/contentImages/content_id_{}.jpg'.format(contentid)
    
        context = {'item':content, 'form':form, 'commentform':commentForm,  'contentid':contentid, 'commentid':commentid, 'comments':commentAll, 'imgpath':imgpath}
        
        return render(request, 'productTrade/Content_comment_update.html', context)
    
    
def delete_comment(request, contentid, commentid):
    if request.method == 'POST':
        # MySQL Connection 연결
        conn = pymysql.connect(host='localhost', user='root', password='ingo75348668', db='hyein_market', charset='utf8')

        # Connection으로부터 Cursor 생성
        curs = conn.cursor()

        # SQL문 실행
        sql = "delete from hyein_market.producttrade_comment where id = " + str(commentid) + ";"
        curs.execute(sql)

        # 데이터 저장
        conn.commit()

        # Connection 닫기
        conn.close()

        return redirect('show_content', contentid=contentid)
            
    else: # GET
        content = get_object_or_404(Content, pk=contentid)
        form = ContentForm(instance=content)
        commentForm = CommentForm(initial={'content_id': contentid ,'commenter_id': request.user })
        commentAll = Comment.objects.filter(content_id=content).all()
        # imgpath = '/media/로 시작'
        imgpath = '/media/productTrade/contentImages/content_id_{}.jpg'.format(contentid)
    
        context = {'item':content, 'form':form, 'commentform':commentForm,  'contentid':contentid, 'commentid':commentid, 'comments':commentAll, 'imgpath':imgpath}
        
        return render(request, 'productTrade/Content_comment_delete.html', context)
    
    
def update_content(request, contentid):
    if request.method == 'POST':
        item = Content.objects.get(pk=contentid)
        form = ContentForm(request.POST, request.FILES, instance=item)
              
        if form.is_valid():
            try:
                if request.FILES['image'] != None:
                    # 기존에 저장된 contentid에 해당하는 이미지 삭제
                    os.remove(os.path.join(settings.MEDIA_ROOT, 'productTrade/contentImages', 'content_id_{}.jpg'.format(contentid)))

                    # 수정된 내용 저장
                    form.save()

                    # 이미지 이름 변경
                    name = os.path.join(settings.MEDIA_ROOT,'productTrade/contentImages', str(request.FILES['image']))
                    newname = os.path.join(settings.MEDIA_ROOT, 'productTrade/contentImages', 'content_id_{}.jpg'.format(contentid))
                    os.rename(name, newname)
            except :
                # 수정된 내용 저장
                form.save()
                
            return redirect('show_content', contentid=contentid)
            
    else: # GET
        content = get_object_or_404(Content, pk=contentid)
        form = ContentForm(instance=content)
        commentForm = CommentForm(initial={'content_id': contentid ,'commenter_id': request.user })
        commentAll = Comment.objects.filter(content_id=content).all()
        # imgpath = '/media/로 시작'
        imgpath = '/media/productTrade/contentImages/content_id_{}.jpg'.format(contentid)
    
        context = {'item':content, 'form':form, 'commentform':commentForm,  'contentid':contentid, 'comments':commentAll, 'imgpath':imgpath}
        
        return render(request, 'productTrade/Content_content_update.html', context)

    
def delete_content(request, contentid):
    if request.method == 'POST':
        # MySQL Connection 연결
        conn = pymysql.connect(host='localhost', user='root', password='ingo75348668', db='hyein_market', charset='utf8')

        # Connection으로부터 Cursor 생성
        curs = conn.cursor()

        # SQL문 실행
        sql = "delete from hyein_market.producttrade_content where id = " + str(contentid) + ";"
        curs.execute(sql)

        # 데이터 저장
        conn.commit()

        # Connection 닫기
        conn.close()

        return redirect('indicontentList')
            
    else: # GET
        content = Content.objects.filter(id=contentid)[0]
        
        
        context = {
            'contentid': contentid,
            'content': content,
            
        }
        return render(request, 'productTrade/Content_content_delete.html', context)    
    
    
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mypage')
        
    else : # GET
        form =  UserUpdateForm(instance=request.user)
        context = {
            'form':form,
        }
            
        return render(request, 'productTrade/User_update.html', context)
    
    
def update_pw(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 사용자는 비밀번호를 변경하더라도 request로 session에 비밀번호를 자동으로 업데이트 해주는 update_session_auth_hash 덕분에 세션 유지가 가능
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('indicontentList')
            
        
    else : # GET
        form =  PasswordUpdateForm(request.user)
        context = {
            'form':form,
        }
            
        return render(request, 'productTrade/Password_update.html', context)
    
    
    
def delete_user(request):
    if request.method == 'POST':
        form = CheckPasswordForm(request.user, request.POST)
        if form.is_valid():
            
            drop = DropoutMember.objects.create(user_id=request.user.username, name=request.user.name, mobile=request.user.mobile, created_at=request.user.created_at)
            drop.save()
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('contentList')
            
        
    else : # GET
        form =  CheckPasswordForm(request.user)
        context = {
            'form':form,
        }
            
        return render(request, 'productTrade/User_delete.html', context)
    
    
def usertest(request):
    if request.method == 'GET':
        us = get_object_or_404(Member, pk=request.user)
        
        context = {
            'member': us,
        }
        return render(request, 'productTrade/usertest.html', context)
    
    
    
    