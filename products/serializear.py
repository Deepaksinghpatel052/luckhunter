from .models import LsCoupons
from rest_framework import serializers

class Couponerializers(serializers.ModelSerializer):
    class Meta:
        model = LsCoupons
        fields = ['id', 'Coupon_code', 'Coupon_Title', 'No_of_use', 'No_of_used','descount_range']