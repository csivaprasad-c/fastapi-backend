from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from pydantic import EmailStr

from app.config import notification_settings
from app.utils import TEMPLATE_DIR


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR
            )
        )

    async def send_email(
        self,
        recipients: list[EmailStr],
        subject: str,
        body: str
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=[NameEmail(email, email) for email in recipients],
                subject=subject,
                body=body,
                subtype=MessageType.plain
            )
        )

    async def send_email_with_template(
        self,
        recipients: list[EmailStr],
        subject: str,
        context: dict,
        template_name: str
    ):

        print(recipients, subject, context, template_name)
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=[NameEmail(email, email) for email in recipients],
                subject=subject,
                template_body=context,
                subtype=MessageType.html
            ),
            template_name=template_name
        )
