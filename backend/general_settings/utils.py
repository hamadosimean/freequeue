from django.db import models
from django.conf import settings
import requests
from urllib.parse import quote_plus
import logging


# Create your models here.


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)  # CreatedAt
    updated_at = models.DateTimeField(auto_now=True)  # UpdatedAt

    class Meta:
        abstract = True
        ordering = ["-created_at"]


""" 
   Send OTP to the given phone number using Kannel SMS gateway 
    Generates a random 6-digit OTP and sends it via an HTTP GET request to the Kannel SMS gateway.
    Returns the generated OTP and the status of the request.
"""


def send_sms(phone_number, message):
    """
    Send SMS through Kannel SMS Gateway.
    """
    send_status = {"success": False, "message": ""}

    try:
        message_encoded = quote_plus(message)

        username = settings.KANNEL_USERNAME
        password = settings.KANNEL_PASSWORD
        port = settings.KANNEL_PORT
        url = (
            f"http://smsbox:{port}/cgi-bin/sendsms?"
            f"username={username}&password={password}"
            f"&to={phone_number}&text={message_encoded}"
            f"&smsc=primary-provider"
        )

        response = requests.get(url, timeout=10)

        if response.status_code in (200, 202):
            if "0:" in response.text.lower():
                send_status["success"] = True
                send_status["message"] = f"SMS sent to {phone_number}"
            else:
                send_status["message"] = f"Kannel responded: {response.text}"
        else:
            send_status["message"] = f"Gateway error: {response.text}"

    except Exception as e:
        send_status["message"] = str(e)
        logging.error(f"Error sending SMS: {e}")

    return send_status
