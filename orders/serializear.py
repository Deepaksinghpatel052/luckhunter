from .models import LsAddToCard,LsOrderItems,LsOrder
from rest_framework import serializers

class AddToCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = LsAddToCard
        fields = ['id', 'user', 'Product', 'Ticket_no', 'Create_date']
        depth = 2

class LsOrderItemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LsOrderItems
        fields = ['id', 'order_id', 'user', 'product_id','Product_cycle', 'Ticket_no','Book_status','Winner']
        depth = 2


class LsOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = LsOrder
        fields = ['id', 'order_id', 'user', 'No_of_item', 'payment', 'descount','descount_amount','total_payment','payment_status','order_status','payment_method','create_date','update_date']
        depth = 2