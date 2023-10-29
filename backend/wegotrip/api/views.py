from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product, Order, Payment
from .serializers import ProductSerializer, GetOrderSerializer
from .consts import Constants


class GetProducts(generics.ListAPIView):
    """Получение списка товаров"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @staticmethod
    def get_extra_actions():
        return []

    @method_decorator(cache_page(30, cache='default'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class CreateOrder(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "products": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="ID of the product",
                            ),
                        },
                    ),
                    description="List of products to order",
                ),
            },
            required=["products"],
        ),
        responses={
            201: GetOrderSerializer,
            400: 'Bad Request',
        },
        operation_description="Create an order with a list of products.",
    )
    def post(self, request, *args, **kwargs):
        """Метод POST для создания заказа"""
        products = request.data.get("products")
        if products is None or len(products) == 0:
            return Response({"error": "Add at least one product to your order."},
                            status=status.HTTP_400_BAD_REQUEST)
        sum_price = 0
        errors = []
        for product in products:
            try:
                price = Product.objects.get(id=product["id"]).price
                sum_price += price
            except Product.DoesNotExist:
                errors.append(f"Product with ID {product["id"]} does not exist.")
            except TypeError:
                return Response({"error": "Invalid data type."},
                                status=status.HTTP_400_BAD_REQUEST)
        if errors:
            return Response({"errors": errors},
                            status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(sum_price=sum_price,
                                     status=Constants.ORDER_CREATED)
        serializer = GetOrderSerializer(order)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @staticmethod
    def get_extra_actions():
        return []


class CreatePayment(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the order for payment',
                ),
            },
            required=['order_id'],
        ),
        responses={
            202: GetOrderSerializer,
            400: 'Bad Request',
        },
    )
    def post(self, request, *args, **kwargs):
        """Метод POST для создания оплаты"""
        order_id = request.data.get('order_id')
        if order_id is None or order_id in ('', ' '):
            return Response({"error": "order_id is required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": f"Order with ID {order_id} does not exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        if order.payment is not None:
            return Response({"error": f"Order with ID {order_id} is paid"},
                            status=status.HTTP_400_BAD_REQUEST)
        sum_price = order.sum_price
        payment = Payment.objects.create(
            sum_price=sum_price,
            status=Constants.PAYMENT_PAID,
            payment_type=Constants.PAID_CARD_ONLINE)
        order.status = Constants.ORDER_PAID
        order.payment = payment
        order.save()
        serializer = GetOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def get_extra_actions():
        return []
