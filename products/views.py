from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LsCategoryes, LsProduct
from .serializear import (
    CategorySerializer,
    CouponValidateResponseSerializer,
    CouponValidateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class CategoryListAPIView(generics.ListAPIView):
    """
    List every active product category, for populating category
    filters/menus in the consuming app.

    Public endpoint: no authentication required. Not paginated, since
    the category list is expected to stay small.
    """

    serializer_class = CategorySerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return LsCategoryes.objects.filter(Status=True).order_by('Category_name')


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter by an active category's `Category_slug`. "
                        "400 if no active category matches.",
        ),
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description='Case-insensitive substring match against `Product_name`.',
        ),
    ]
)
class ProductListAPIView(generics.ListAPIView):
    """
    List active products, most recently opened for booking first.

    Public endpoint: no authentication required. Paginated per
    DEFAULT_PAGINATION_CLASS/PAGE_SIZE in settings.
    """

    serializer_class = ProductListSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = LsProduct.objects.filter(Status=True).order_by('-Ticket_booking_start')

        category_slug = self.request.query_params.get('category')
        if category_slug:
            if not LsCategoryes.objects.filter(Category_slug=category_slug, Status=True).exists():
                raise ValidationError({'category': 'No active category matches this slug.'})
            queryset = queryset.filter(Category__Category_slug=category_slug)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Product_name__icontains=search)

        return queryset


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve one active product's full detail: description, ticket
    pricing/dates, and its active gallery images.

    Public endpoint: no authentication required. 404 if no active
    product matches the given slug.
    """

    serializer_class = ProductDetailSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    queryset = LsProduct.objects.filter(Status=True)


class CouponValidateAPIView(APIView):
    """
    Validate a coupon code and, if it is currently usable (exists,
    within its active date range, under its usage limit), return its
    discount details.

    Request body: {"Coupon_code": "<code>"}

    Public endpoint: no authentication required, since a coupon may be
    checked before the app user is signed in.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=CouponValidateSerializer, responses=CouponValidateResponseSerializer)
    def post(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'valid': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        coupon = serializer.coupon
        return Response({
            'valid': True,
            'Coupon_code': coupon.Coupon_code,
            'Coupon_Title': coupon.Coupon_Title,
            'descount_range': coupon.descount_range,
        })
