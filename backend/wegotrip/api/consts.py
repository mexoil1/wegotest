class Constants:
    ORDER_CREATED = 0
    ORDER_PAID = 1
    ORDER_CONFIRMED = 2
    PAYMENT_NOT_PAID = 0
    PAYMENT_PAID = 1
    PAID_CARD_ONLINE = 0
    PAID_CARD_COURIER = 1
    PAID_CASH_COURIER = 2


CHOICES_STATUS_ORDER = (
    (Constants.ORDER_CREATED, 'Создан'),
    (Constants.ORDER_PAID, 'Оплачен'),
    (Constants.ORDER_CONFIRMED, 'Подтвержден'),
)
CHOICES_STATUS_PAYMENT = (
    (Constants.PAYMENT_NOT_PAID, 'Не оплачено'),
    (Constants.PAYMENT_PAID, 'Оплачено'),
)
CHOICES_PAYMENT_TYPE = (
    (Constants.PAID_CARD_ONLINE, 'Картой онлайн'),
    (Constants.PAID_CARD_COURIER, 'Картой курьеру'),
    (Constants.PAID_CASH_COURIER, 'Наличными курьеру'),
)
