from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status

from .models import Product, Order, Payment
from .consts import Constants


class CreateOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_order(self):
        """Создание заказа"""
        Product.objects.create(name="test", content="test", price=1)
        products = [{"id": 1}]
        data = {"products": products}
        response = self.client.post(
            f"{settings.API_URL}create_order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.status, Constants.ORDER_CREATED)

    def test_create_order_invalid_data(self):
        """Создание заказа с неправильными данными"""
        data = {}
        response = self.client.post(
            f"{settings.API_URL}create_order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_nonexistent_product(self):
        """Создание заказа с несуществующим id товара"""
        products = [{"id": 999}]
        data = {"products": products}
        response = self.client.post(
            f"{settings.API_URL}create_order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreatePaymentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_payment(self):
        """Создание оплаты"""
        order = Order.objects.create(
            sum_price=100, status=Constants.ORDER_CREATED)
        data = {"order_id": order.id}
        response = self.client.post(
            f"{settings.API_URL}create_payment/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        order.refresh_from_db()
        self.assertEqual(order.status, Constants.ORDER_PAID)

    def test_create_payment_missing_order_id(self):
        """Создание оплаты с неправильными данными"""
        data = {}
        response = self.client.post(
            f"{settings.API_URL}create_payment/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_nonexistent_order(self):
        """Создание оплаты на несуществующий id"""
        data = {"order_id": 999}
        response = self.client.post(
            f"{settings.API_URL}create_payment/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_paid_order(self):
        """Создание оплаты на уже оплаченный заказ"""
        payment = Payment.objects.create(
            sum_price=100, status=Constants.PAYMENT_PAID, payment_type=Constants.PAID_CARD_COURIER)
        order = Order.objects.create(
            sum_price=100, status=Constants.ORDER_PAID, payment=payment)
        data = {"order_id": order.id}
        response = self.client.post(
            f"{settings.API_URL}create_payment/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
