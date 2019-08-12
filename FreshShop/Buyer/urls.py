from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
    path("base/",base),
    path("index/",index),
    path("register/",register),
    path("login/",login),
    path("logout/",logout),
    path('goods_list/',goods_list),
    path('goods_detail/',goods_detail),
    path('place_order/',place_order),
    path('shoppingCart/',shoppingCart),
    path('add_cart/',add_cart),
]