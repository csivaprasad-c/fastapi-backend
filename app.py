import asyncio

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import notification_settings

print(notification_settings.model_dump())

fastmail = FastMail(
   ConnectionConfig(
      **notification_settings.model_dump()
   )
)

async def send_message():
    await fastmail.send_message(
        message=MessageSchema(
            recipients=["sivaprasad@sivaprasad.co.in"],
            subject="Your Email Delivered With FastShip",
            body="Things are about to get interesting...",
            subtype=MessageType.plain,
        )
    )
    print("Email sent")

asyncio.run(send_message())