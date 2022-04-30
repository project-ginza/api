from django.db import models
from common.models import BaseModel


class OrderStatus(models.IntegerChoices):    
    SUCCESS = 0   #주문완료
    ARRIVE = 1    #배송완료
    REFUND = 2    #환불신청완료
    SHIPPING = 3  #배송중

class PaymentStatus(models.IntegerChoices):
    CARD = 1     #카드
    DEPOSIT = 2  #무통장입금

class Basket(BaseModel):
    product = models.ManyToManyField("product.Product", through="order.ProductBasket" ,on_delete=models.PROTECT)
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table = "basket"
        

class ProductBasket(BaseModel):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    basket = models.ForeignKey("product.Basket", on_delete=models.CASCADE)
    
    class Meta:
        db_table="product_basket"


class OrderHeader(BaseModel):
    user = models.ForeignKey("user.User", on_delete=models.PROTECT, null=True)
    order_status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.SUCCESS)
    basket = models.OneToOneField("order.Basket", on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = "order"


class ProductOrder(BaseModel):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    order = models.ForeignKey("order.OrderHeader", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "product_order"