from django.db import models
class Seller(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    nickname = models.CharField(max_length=32,verbose_name="昵称",null=True,blank=True)
    phone = models.CharField(max_length=32,verbose_name="电话",null=True,blank=True)
    email = models.EmailField(verbose_name="邮箱",null=True,blank=True)
    picture = models.ImageField(upload_to="store/images", verbose_name="头像",null=True,blank=True)
    address = models.CharField(max_length=32,verbose_name="地址",null=True,blank=True)
    card_id = models.CharField(max_length=32,verbose_name="身份证号",null=True,blank=True)

