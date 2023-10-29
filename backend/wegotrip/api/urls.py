from django.urls import path

from .views import GetProducts, CreateOrder, CreatePayment

app_name = 'api'


urlpatterns = [
    # path('', include(router.urls)),
    path('get_products/', GetProducts.as_view(), name='get_products'),
    path('create_order/', CreateOrder.as_view(), name='create_order'),
    path('create_payment/', CreatePayment.as_view(), name='create_payment'),
]
