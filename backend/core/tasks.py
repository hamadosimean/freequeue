from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import Branch, Payment
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Queue, Service

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def desactivate_branch_payment():
    """
    desactivate branch if payment expired
    search for the latest payment of each branch
    if the latest payment is expired, desactivate the branch
    """
    try:
        with transaction.atomic():
            branches = Branch.objects.all()
            for branch in branches:
                payment = (
                    Payment.objects.filter(branch=branch)
                    .order_by("-updated_at")
                    .first()
                )
                if payment and payment.expired_at <= timezone.now():
                    payment.status = "expired"
                    payment.save()
                    branch.is_active = False
                    branch.save()
    except Exception as e:
        logger.error(f"Error desactivating branch payment: {e}")
