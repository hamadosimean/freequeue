from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/core/queues/<uuid:queue_id>", consumers.QueueConsumer.as_asgi()),
    path(
        "ws/core/services/<uuid:service_id>/queues",
        consumers.ServiceQueueConsumer.as_asgi(),
    ),
]
