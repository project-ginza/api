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

class BasketHeader(BaseModel):
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    price_sum = models.PositiveIntegerField()
        
    class Meta:
        db_table = "basket_header"
        

class BasketLine(BaseModel):
    header = models.ForeignKey("order.BasketHeader", on_delete=models.CASCADE)
    product = models.ManyToManyField("product.Product", through="order.ProductBasketLine" ,on_delete=models.PROTECT)
    
    class Meta:
        db_table = "basket_line"


class ProductBasketLine(BaseModel):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    basket = models.ForeignKey("product.BasketLine", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table="product_basket_line"


class OrderHeader(BaseModel):
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    order_status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.SUCCESS)
    basket = models.OneToOneField("order.BasketHeader", on_delete=models.CASCADE, null=True)
    price_sum = models.PositiveIntegerField()
    
    class Meta:
        db_table = "order_header"


class OrderLine(BaseModel):
    header = models.ForeignKey("OrderHeader", on_delete=models.CASCADE)
    product = models.ManyToManyField("product.Product", on_delete=models.PROTECT,through="order.ProductOrderLine")
    
    class Meta:
        db_table = "order_line"


class ProductOrderLine(BaseModel):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    order = models.ForeignKey("order.OrderLine", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    class Meta:
        db_table = "product_order_line"