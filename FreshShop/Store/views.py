import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from Store.models import *
from Store.models import *
def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result
def userValid(username):
    user = Seller.objects.filter(username=username).first()
    return user
def ajax_userValid(request):
    pass
def register(request):
    result = {"content":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            if not userValid(username):
                seller = Seller()
                seller.username = username
                seller.password = set_password(password)
                seller.nickname = username
                seller.save()
                return HttpResponseRedirect("/Store/login/")
            else:
                result["content"] = "用户名已存在"
        else:
            result["content"] = "用户名或密码不可为空"
    return render(request,"store/register.html",locals())


def login(request):
    result = {"content":""}
    # response = render(request,"store/login.html",locals())
    #     # response.set_cookie("login_left","login_right")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if user:
                web_password = set_password(password)
                # cookies = request.COOKIES.get("login_left")
                if user.password == web_password :
                    response = HttpResponseRedirect("/Store/index/")
                    response.set_cookie("username",username)
                    request.session["username"] = username
                    return response
                else:
                    result["content"] = "密码输入有误"
            else:
                result["content"] = "用户名不存在"
        else:
            result["content"] = "用户名或者密码不可为空"
    return render(request,'store/login.html',locals())



def login_valid(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        session_user = request.session.get("username")
        if username and session_user:
            user = Seller.objects.filter(username=username).first()
            if user and username == session_user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/Store/login/")
    return inner
@login_valid
def index(request):
    return render(request,"store/index.html")

