from fastapi import BackgroundTasks
from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType,
    NameEmail,
)
from pydantic import EmailStr
from twilio.http.async_http_client import AsyncTwilioHttpClient
from twilio.rest import Client

from app.config import notification_settings
from app.utils import TEMPLATE_DIR


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(
                    exclude={
                        "TWILIO_AUTH_TOKEN",
                        "TWILIO_SID",
                        "TWILIO_MESSAGE_SERVICE_ID",
                    }
                ),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
            )
        )
        self._twilio_client: Client | None = None

    async def send_email(self, recipients: list[EmailStr], subject: str, body: str):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=[NameEmail(email, email) for email in recipients],
                subject=subject,
                body=body,
                subtype=MessageType.plain,
            ),
        )

    async def send_email_with_template(
        self,
        recipients: list[EmailStr],
        subject: str,
        context: dict,
        template_name: str,
    ):

        print(recipients, subject, context, template_name)
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=[NameEmail(email, email) for email in recipients],
                subject=subject,
                template_body=context,
                subtype=MessageType.html,
            ),
            template_name=template_name,
        )

    async def send_sms(self, to: str, body: str):
        if self._twilio_client is None:
            self._twilio_client = Client(
                notification_settings.TWILIO_SID,
                notification_settings.TWILIO_AUTH_TOKEN,
                http_client=AsyncTwilioHttpClient(),
            )
        await self._twilio_client.messages.create_async(
            to=to,
            messaging_service_sid=notification_settings.TWILIO_MESSAGE_SERVICE_ID,
            body=body,
        )
