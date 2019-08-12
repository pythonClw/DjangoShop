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
                    store = Store.objects.filter(user_id=user.id).first()
                    if store:
                        response.set_cookie("has_store",store.id)
                    else:
                        response.set_cookie("has_store","")
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
        user_id = request.COOKIES.get("user_id")
        if username and session_user and user_id:
            user = Seller.objects.filter(username=username).first()
            if user and username == session_user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/Store/login/")
    return inner
@login_valid
def index(request):
    return render(request,"store/index.html")
def base(request):
    return render(request,"store/base.html")
@login_valid
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
        response = HttpResponseRedirect("/Store/index/")
        response.set_cookie('has_store',store.id)
        return response
    return render(request, "store/register_store.html", locals())
@login_valid
def add_goods(request):
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_description = request.POST.get("goods_description")
        goods_number = request.POST.get("goods_number")
        goods_price = request.POST.get("goods_price")
        goods_date = request.POST.get("goods_date")
        goods_image = request.FILES.get("goods_image")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.COOKIES.get("has_store")
        goods_type = request.POST.get("goods_type")
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_number = goods_number
        goods.goods_price = goods_price
        goods.goods_date = goods_date
        goods.goods_image = goods_image
        goods.goods_safeDate = goods_safeDate
        goods.goods_type = GoodsType.objects.get(id=int(goods_type))
        goods.save()
        goods.store_id.add(
            Store.objects.get(id=int(goods_store))
        )
        goods.save()
        return HttpResponseRedirect("/Store/list_goods/up")
    return render(request,"store/add_goods.html",locals())
@login_valid
def list_goods(request,state):

    if state =="up":
        state_num = 1
    else:
        state_num = 0
    keywords = request.GET.get("keywords","")
    page_num = request.GET.get("page_num",1)
    store_id = request.COOKIES.get("has_store")
    store = Store.objects.get(id=int(store_id))
    if keywords:
        goods_list = store.goods_set.filter(goods_name__contains=keywords,goods_under=state_num)
    else:
        goods_list = store.goods_set.filter(goods_under=state_num)
    goods_type = GoodsType.objects.all()

    paginator = Paginator(goods_list,5)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,"store/list_goods.html",locals())
@login_valid
def goods(request,goods_id):
    goods_data = Goods.objects.filter(id=goods_id).first()
    return render(request,"store/goods.html",locals())
@login_valid
def update_goods(request,goods_id):
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_description = request.POST.get("goods_description")
        goods_number = request.POST.get("goods_number")
        goods_price = request.POST.get("goods_price")
        goods_date = request.POST.get("goods_date")
        goods_image = request.FILES.get("goods_image")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods = Goods.objects.get(id=int(goods_id))
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_number = goods_number
        goods.goods_price = goods_price
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect("/Store/goods/%s"%goods_id)
    return render(request,"store/update_goods.html",locals())
def set_goods(request,state):
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get("id")
    referer = request.META.get("HTTP_REFERER")
    if id:
        goods=Goods.objects.filter(id=id).first()
        if state == "del":
            goods.delete()
        else:
            goods.goods_under = state_num
            goods.save()
    return HttpResponseRedirect(referer)
def logout(request):
    response = HttpResponseRedirect("/Store/login")
    for key in request.COOKIES.keys():
        response.delete_cookie(key)
    return response
def add_type(request):
    if request.method == "POST":
        type_name = request.POST.get("goodsType_name")
        type_description = request.POST.get("goodsType_description")
        type_image = request.FILES.get("goodsType_image")
        goods_type = GoodsType()
        goods_type.goodsType_name = type_name
        goods_type.goodsType_description = type_description
        goods_type.goodsType_image = type_image
        goods_type.save()
        return HttpResponseRedirect("/Store/add_type/")
    return render(request,"store/goods_type.html")
from rest_framework import viewsets

from Store.serializers import *
class UserViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all().order_by("id")
    serializer_class = UserSerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer
def ajax_goods_list(request):
    return render(request,"store/ajax_goods_list.html")