from celery import shared_task
from datetime import datetime
from time import sleep
import requests
import json
import logging

from .consts import Constants
from .models import Order


logger = logging.getLogger(__name__)


@shared_task
def confirm_order(object_id):
    try:
        order = Order.objects.get(pk=object_id)
        sleep(5)
        date_of_confirm_str = order.date_of_confirm.strftime(
            "%Y-%m-%d %H:%M:%S")

        data = {
            "id": order.id,
            "amount": order.sum_price,
            "date": date_of_confirm_str,
        }
        url = "https://webhook.site/34d5323b-89f4-4fde-97e4-187db1af4e4f"
        requests.post(url, data=json.dumps(data))
        logger.info(f"Order {order.id} confirmed successfully")
    except Order.DoesNotExist:
        logger.error(f"Order with id {object_id} not found")
    except Exception as e:
        logger.error(f"Error in confirm_order: {str(e)}")
