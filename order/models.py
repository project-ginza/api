from django.db import models
from common.models import BaseModel

'''
orderstatus enum으로 바꾸기
'''
class OrderStatus(models.IntegerChoices):    
    SUCCESS = 0   #주문완료
    ARRIVE = 1    #배송완료
    REFUND = 2    #환불신청완료
    SHIPPING = 3  #배송중
       

class Basket(BaseModel):
    product = models.ForeignKey("product.ProductDetails", on_delete=models.PROTECT)
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table = "basket"

class Order(BaseModel):
    product = models.ForeignKey("product.ProductDetails", on_delete=models.PROTECT, null=True)
    user = models.ForeignKey("user.User", on_delete=models.PROTECT, null=True)
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.SUCCESS)
    basket = models.ForeignKey("order.Basket", on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    
    class Meta:
        db_table = "order"

