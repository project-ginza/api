from django.db import models
from common.models import BaseModel

# 사용자 상태 enum
class OrderStatus(models.IntegerChoices):
    SUCCESS = 0   #주문완료
    ARRIVE = 1  #배송완료
    REFUND = 2  #환불신청완료
    SHIPPING = 3 #배송중

class Order(BaseModel):
    product = models.ForeignKey("product.ProductDetails", on_delete=models.PROTECT)
    user = models.ForeignKey("user.User", on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.SUCCESS
    )

