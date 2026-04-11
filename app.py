from twilio.rest import Client
from app.config import notification_settings

client = Client(
    notification_settings.TWILIO_SID, notification_settings.TWILIO_AUTH_TOKEN
)

client.messages.create(
    to="+917299058008",
    body="Hello from FastShip",
    messaging_service_sid=notification_settings.TWILIO_MESSAGE_SERVICE_ID,
)

# import asyncio
#
# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
#
# from app.config import notification_settings
#
# print(notification_settings.model_dump())
#
# fastmail = FastMail(
#    ConnectionConfig(
#       **notification_settings.model_dump()
#    )
# )
#
# async def send_message():
#     await fastmail.send_message(
#         message=MessageSchema(
#             recipients=["sivaprasad@sivaprasad.co.in"],
#             subject="Your Email Delivered With FastShip",
#             body="Things are about to get interesting...",
#             subtype=MessageType.plain,
#         )
#     )
#     print("Email sent")
#
# asyncio.run(send_message())
