from rest_framework import serializers
from Store.models import Goods
from Store.models import GoodsType
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goods
        fields = ['goods_name','goods_price','goods_number','goods_description','id','goods_date','goods_safeDate']
class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsType
        fields = ['goodsType_name','goodsType_description']