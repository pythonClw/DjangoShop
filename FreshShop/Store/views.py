import hashlib
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
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
                    response.set_cookie("user_id",user.id)
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
    user_id = request.COOKIES.get("user_id")
    if user_id:
        user_id = int(user_id)
    else:
        user_id = 0
    store = Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request,"store/index.html",{"is_store":is_store})
def base(request):
    return render(request,"store/base.html")
def register_store(request):
    type_list = StoreType.objects.all()
    if request.method =="POST":
        store_name = request.POST.get("store_name")
        store_description = request.POST.get("store_description")
        store_phone = request.POST.get("store_phone")
        store_money = request.POST.get("store_money")
        store_address = request.POST.get("store_address")
        user_id = int(request.COOKIES.get("user_id"))  # 通过cookie来得到user_id
        type_list = request.POST.get("type")  # 通过request.post得到类型，但是是一个列表

        store_logo = request.FILES.get("store_logo")  # 通过request.FILES得到

        # 保存非多对多数据
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo  # django1.8之后图片可以直接保存
        store.save()  # 保存，生成了数据库当中的一条数据
        # 在生成的数据当中添加多对多字段。
        for i in type_list:  # 循环type列表，得到类型id
            store_type = StoreType.objects.get(id=i)  # 查询类型数据
            store.type.add(store_type)  # 添加到类型字段，多对多的映射表
        store.save()

    return render(request, "store/register_store.html", locals())
def add_goods(request):
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_description = request.POST.get("goods_description")
        goods_number = request.POST.get("goods_number")
        goods_price = request.POST.get("goods_price")
        goods_date = request.POST.get("goods_date")
        goods_image = request.FILES.get("goods_image")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.POST.get("goods_store")
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_number = goods_number
        goods.goods_price = goods_price
        goods.goods_date = goods_date
        goods.goods_image = goods_image
        goods.goods_safeDate = goods_safeDate
        goods.save()
        goods.store_id.add(
            Store.objects.get(id=int(goods_store))
        )
        goods.save()
        return HttpResponseRedirect("/Store/list_goods/")
    return render(request,"store/add_goods.html")
def list_goods(request):
    keywords = request.GET.get("keywords","")
    page_num = request.GET.get("page_num",1)
    if keywords:
        goods_list = Goods.objects.filter(goods_name__contains=keywords)
    else:
        goods_list = Goods.objects.all()
    paginator = Paginator(goods_list,5)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,"store/list_goods.html",locals())



