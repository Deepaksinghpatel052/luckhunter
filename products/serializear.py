from datetime import date

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from luckhunter.utils import get_absolute_media_url
from .models import LsCategoryes, LsProduct, lsProductImage, LsCoupons


class Couponerializers(serializers.ModelSerializer):
    class Meta:
        model = LsCoupons
        fields = ['id', 'Coupon_code', 'Coupon_Title', 'No_of_use', 'No_of_used', 'descount_range']


class CategorySerializer(serializers.ModelSerializer):
    """An active product category, for populating catalog filters/menus."""

    Image = serializers.SerializerMethodField()

    class Meta:
        model = LsCategoryes
        fields = ['id', 'Category_name', 'Category_slug', 'Image']

    @extend_schema_field(OpenApiTypes.URI)
    def get_Image(self, obj):
        return get_absolute_media_url(obj.Image, self.context.get('request'))


class ProductImageSerializer(serializers.ModelSerializer):
    """One gallery image belonging to a product."""

    Image = serializers.SerializerMethodField()

    class Meta:
        model = lsProductImage
        fields = ['id', 'Image']

    @extend_schema_field(OpenApiTypes.URI)
    def get_Image(self, obj):
        return get_absolute_media_url(obj.Image, self.context.get('request'))


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight product representation for list/browse views."""

    Image = serializers.SerializerMethodField()
    category = serializers.CharField(source='Category.Category_name', default=None, read_only=True)
    category_slug = serializers.CharField(source='Category.Category_slug', default=None, read_only=True)

    class Meta:
        model = LsProduct
        fields = [
            'id', 'Product_id', 'Product_name', 'Product_TagLine', 'slug',
            'category', 'category_slug', 'ReyalPrice', 'Price_pr_ticket',
            'No_of_ticket', 'Image', 'Ticket_booking_start', 'Ticket_open_date',
            'winner_status',
        ]

    @extend_schema_field(OpenApiTypes.URI)
    def get_Image(self, obj):
        return get_absolute_media_url(obj.Image, self.context.get('request'))


class ProductDetailSerializer(ProductListSerializer):
    """Full product detail: adds description and active gallery images."""

    images = serializers.SerializerMethodField()

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + [
            'description', 'product_link', 'images', 'Publich_date', 'winner_ticket', 'Max_Coins',
        ]

    @extend_schema_field(ProductImageSerializer(many=True))
    def get_images(self, obj):
        request = self.context.get('request')
        active_images = obj.lsProductImage_create_by.filter(Status=True)
        return ProductImageSerializer(active_images, many=True, context={'request': request}).data


class CouponValidateSerializer(serializers.Serializer):
    """Validates a coupon code: exists, is within its active date range,
    and hasn't exceeded its usage limit. On success, the matched
    LsCoupons instance is available as `self.coupon`."""

    Coupon_code = serializers.CharField(max_length=120)

    def validate_Coupon_code(self, value):
        try:
            coupon = LsCoupons.objects.get(Coupon_code=value)
        except LsCoupons.DoesNotExist:
            raise serializers.ValidationError("This coupon code does not exist.")

        today = date.today()
        if not (coupon.Start_date <= today <= coupon.end_date):
            raise serializers.ValidationError("This coupon is not currently active.")

        if coupon.No_of_used >= coupon.No_of_use:
            raise serializers.ValidationError("This coupon has reached its usage limit.")

        self.coupon = coupon
        return value


class CouponValidateResponseSerializer(serializers.Serializer):
    """Response shape for CouponValidateAPIView: documents both the
    success payload (valid=True + coupon fields) and the failure
    payload (valid=False + field errors) in one schema."""

    valid = serializers.BooleanField()
    Coupon_code = serializers.CharField(required=False)
    Coupon_Title = serializers.CharField(required=False)
    descount_range = serializers.IntegerField(required=False)
    errors = serializers.DictField(required=False)
