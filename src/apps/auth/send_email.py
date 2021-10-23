from src.config import settings
from pathlib import Path
from src.apps.base.email import send_email


def send_test_email(email_to:str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test EMAIL "
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": project_name, "email": email_to},
    )


def send_account_activate(email_to: str, username: str, password: str, uuid: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = f"{settings.SERVER_HOST}/api/v1/users/verify?token={uuid}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
