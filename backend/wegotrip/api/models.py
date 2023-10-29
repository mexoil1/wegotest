from django.db import models

from .consts import CHOICES_STATUS_PAYMENT,\
    CHOICES_PAYMENT_TYPE, CHOICES_STATUS_ORDER


class Product(models.Model):
    """Модель для продуктов"""
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='products/',
                              null=True, blank=True, verbose_name='Картинка')
    content = models.TextField(verbose_name='Контент')
    price = models.FloatField(verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return f'{self.name} - {self.price} руб.'


class Payment(models.Model):
    """Модель для платежа"""
    sum_price = models.FloatField(verbose_name='Сумма')
    status = models.IntegerField(
        choices=CHOICES_STATUS_PAYMENT, verbose_name='Статус')
    payment_type = models.IntegerField(
        choices=CHOICES_PAYMENT_TYPE, verbose_name='Тип оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self) -> str:
        return f'Платеж на сумму {self.sum_price}'


class Order(models.Model):
    """Модель для заказов"""
    sum_price = models.FloatField(verbose_name='Итоговая сумма')
    status = models.IntegerField(
        choices=CHOICES_STATUS_ORDER, verbose_name='Статус')
    date_of_create = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    date_of_confirm = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата подтверждения')
    payment = models.OneToOneField(
        Payment, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Платеж')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f'Заказ от {self.date_of_create} на сумму {self.sum_price}'
