from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import Company, Payment, Queue, Service
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def desactivate_company_payment():
    """
    desactivate company if payment expired
    search for the latest payment of each company
    if the latest payment is expired, desactivate the company
    """
    try:
        with transaction.atomic():
            companies = Company.objects.all()
            for company in companies:
                payment = (
                    Payment.objects.filter(company=company)
                    .order_by("-updated_at")
                    .first()
                )
                if payment and payment.expired_at <= timezone.now():
                    payment.status = "expired"
                    payment.save()
                    company.is_active = False
                    company.save()
    except Exception as e:
        logger.error(f"Error desactivating company payment: {e}")
