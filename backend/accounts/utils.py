from django.conf import settings
import requests
from urllib.parse import quote_plus
import logging
import secrets
from django.core.mail import send_mail

""" 
   Send OTP to the given phone number using Kannel SMS gateway 
    Generates a random 6-digit OTP and sends it via an HTTP GET request to the Kannel SMS gateway.
    Returns the generated OTP and the status of the request.
"""


def send_otp(phone_number, otp=None):
    """
    Send OTP through Kannel SMS Gateway.
    """
    if not otp:
        otp = "".join([str(secrets.randbelow(10)) for _ in range(6)])
    send_status = {"success": False, "message": ""}

    try:
        message = f"Votre OTP est {otp}"
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
                send_status["message"] = f"OTP sent to {phone_number}"
            else:
                send_status["message"] = f"Kannel responded: {response.text}"
        else:
            send_status["message"] = f"Gateway error: {response.text}"

    except Exception as e:
        send_status["message"] = str(e)
        logging.error(f"Error sending OTP: {e}")

    return otp, send_status


def send_email(to_email, subject, message):
    """
    Send email to the given email address.
    """
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
    except Exception as e:
        logging.error(f"Error sending email: {e}")
