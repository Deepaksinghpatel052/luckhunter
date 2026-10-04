import os
import shutil
import tempfile
from datetime import date, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import LsCategoryes, LsCoupons, LsProduct, lsProductImage

# Isolate uploaded test files from the real MEDIA_ROOT.
TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix='luckhunter_test_media_')


def make_image(name='test.jpg'):
    return SimpleUploadedFile(name, b'fake-image-bytes', content_type='image/jpeg')


def make_category(**overrides):
    defaults = {
        'Category_name': 'Electronics',
        'Image': make_image('category.jpg'),
        'Status': True,
    }
    defaults.update(overrides)
    return LsCategoryes.objects.create(**defaults)


def make_product(**overrides):
    today = date.today()
    defaults = {
        'Product_name': 'Test Product',
        'ReyalPrice': 1000,
        'description': 'A product used in tests.',
        'product_link': 'https://example.com/product',
        'No_of_ticket': 100,
        'Price_pr_ticket': 10,
        'Image': make_image('product.jpg'),
        'Status': True,
        'Publich_date': today,
        'Ticket_booking_start': today,
        'Ticket_open_date': today + timedelta(days=7),
    }
    defaults.update(overrides)
    return LsProduct.objects.create(**defaults)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductsAPITestCase(APITestCase):
    """Shared setup/teardown for products API tests: isolates uploaded
    test files under a temporary MEDIA_ROOT instead of the real media/
    directory."""

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)


class CategoryListAPITests(ProductsAPITestCase):
    def test_lists_only_active_categories(self):
        make_category(Category_name='Active Category', Status=True)
        make_category(Category_name='Inactive Category', Status=False)

        response = self.client.get(reverse('api:products_api:category-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item['Category_name'] for item in response.data]
        self.assertIn('Active Category', names)
        self.assertNotIn('Inactive Category', names)

    def test_image_falls_back_to_placeholder_when_file_missing(self):
        category = make_category()
        # Simulate the DB pointing at a file that no longer exists on disk.
        os.remove(category.Image.path)

        response = self.client.get(reverse('api:products_api:category-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        image_url = response.data[0]['Image']
        self.assertIn('product_placeholder', image_url)


class ProductListAPITests(ProductsAPITestCase):
    def test_lists_only_active_products(self):
        make_product(Product_name='Active Product', Status=True)
        make_product(Product_name='Inactive Product', Status=False)

        response = self.client.get(reverse('api:products_api:product-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item['Product_name'] for item in response.data['results']]
        self.assertIn('Active Product', names)
        self.assertNotIn('Inactive Product', names)

    def test_filter_by_category_slug(self):
        category = make_category()
        make_product(Product_name='In Category', Category=category)
        make_product(Product_name='No Category')

        response = self.client.get(
            reverse('api:products_api:product-list'), {'category': category.Category_slug}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item['Product_name'] for item in response.data['results']]
        self.assertEqual(names, ['In Category'])

    def test_filter_by_unknown_category_returns_400(self):
        response = self.client.get(reverse('api:products_api:product-list'), {'category': 'does-not-exist'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_by_name(self):
        make_product(Product_name='Findable Widget')
        make_product(Product_name='Other Thing')

        response = self.client.get(reverse('api:products_api:product-list'), {'search': 'findable'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item['Product_name'] for item in response.data['results']]
        self.assertEqual(names, ['Findable Widget'])


class ProductDetailAPITests(ProductsAPITestCase):
    def test_retrieve_active_product_includes_only_active_images(self):
        product = make_product()
        lsProductImage.objects.create(Product=product, Image=make_image('active.jpg'), Status=True)
        lsProductImage.objects.create(Product=product, Image=make_image('inactive.jpg'), Status=False)

        response = self.client.get(reverse('api:products_api:product-detail', args=[product.slug]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['images']), 1)

    def test_unknown_slug_returns_404(self):
        response = self.client.get(reverse('api:products_api:product-detail', args=['no-such-product']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_inactive_product_returns_404(self):
        product = make_product(Status=False)
        response = self.client.get(reverse('api:products_api:product-detail', args=[product.slug]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CouponValidateAPITests(ProductsAPITestCase):
    def make_coupon(self, **overrides):
        today = date.today()
        defaults = {
            'Coupon_code': 'SAVE10',
            'Coupon_Title': 'Save 10',
            'No_of_use': 5,
            'No_of_used': 0,
            'descount_range': 10,
            'Start_date': today - timedelta(days=1),
            'end_date': today + timedelta(days=1),
        }
        defaults.update(overrides)
        return LsCoupons.objects.create(**defaults)

    def test_valid_coupon(self):
        self.make_coupon()
        response = self.client.post(reverse('api:products_api:coupon-validate'), {'Coupon_code': 'SAVE10'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        self.assertEqual(response.data['descount_range'], 10)

    def test_missing_code_returns_400(self):
        response = self.client.post(reverse('api:products_api:coupon-validate'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['valid'])

    def test_unknown_code_returns_400(self):
        response = self.client.post(reverse('api:products_api:coupon-validate'), {'Coupon_code': 'NOPE'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_coupon_returns_400(self):
        today = date.today()
        self.make_coupon(Start_date=today - timedelta(days=10), end_date=today - timedelta(days=1))

        response = self.client.post(reverse('api:products_api:coupon-validate'), {'Coupon_code': 'SAVE10'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exhausted_coupon_returns_400(self):
        self.make_coupon(No_of_use=5, No_of_used=5)

        response = self.client.post(reverse('api:products_api:coupon-validate'), {'Coupon_code': 'SAVE10'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
