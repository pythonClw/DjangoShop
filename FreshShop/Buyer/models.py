from django.db import models
class Buyer(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    email = models.EmailField(verbose_name="用户邮箱")
    phone = models.CharField(max_length=32,verbose_name="联系电话")
    connect_address = models.TextField(verbose_name="联系地址")
class Address(models.Model):
    address = models.TextField(verbose_name="收货地址")
    receiver = models.CharField(max_length=32,verbose_name="收件人")
    re_phone = models.CharField(max_length=32,verbose_name="收件人电话")
    post_num = models.CharField(max_length=32,verbose_name="邮编")
    buyer_id = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name="用户id")
class Order(models.Model):
    order_id = models.CharField(max_length=32,verbose_name="订单号")
    goods_count= models.IntegerField(verbose_name="商品数量")
    order_user = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name="订单用户")
    order_address = models.ForeignKey(to=Address,on_delete=models.CASCADE,verbose_name="订单地址",blank=True,null=True)
    order_price = models.FloatField(verbose_name="订单总价")
class OrderDetail(models.Model):
    order_id = models.ForeignKey(to=Order,on_delete=models.CASCADE,verbose_name="订单编号（多对一）")
    goods_id = models.IntegerField(verbose_name="商品id")
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_number = models.IntegerField(verbose_name="商品数量")
class ShoppingCart(models.Model):
    goods_name = models.CharField(max_length=32,verbose_name='商品名称')
    goods_price = models.FloatField(verbose_name='商品价格')
    goods_total = models.FloatField(verbose_name='商品总价')
    goods_number =models.IntegerField(verbose_name='商品数量')
    goods_picture = models.ImageField(upload_to= 'buyer/images',verbose_name='商品图片')
    goods_id = models.IntegerField(verbose_name='商品id')
    goods_store = models.IntegerField(verbose_name="商品店铺")
    user_id = models.IntegerField(verbose_name='用户id')