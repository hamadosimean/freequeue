import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Queue


def update_service_queues(*, service_id):
    """
    - Get called queue for each service
    - Get next queue for each service
    - Number of waiting queues for each service
    """
    queues = Queue.objects.filter(
        service_id=service_id, date_joined=datetime.date.today()
    )
    next_queue = queues.filter(status="waiting").first()
    called_queue = queues.filter(status="called").last()
    waiting_queues = queues.filter(status="waiting").count()

    stats = {
        "next_queue": next_queue.queue_number if next_queue else None,
        "called_queue": called_queue.queue_number if called_queue else None,
        "waiting_queues": waiting_queues,
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"service_queue_{service_id}",
        {
            "type": "service_queue_update",
            "data": stats,
        },
    )
    return stats
