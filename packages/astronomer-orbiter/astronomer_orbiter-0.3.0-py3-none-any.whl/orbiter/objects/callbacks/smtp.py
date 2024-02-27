from orbiter.objects import OrbiterRequirement, ImportList
from orbiter.objects.callback import OrbiterCallback
from orbiter.objects.task import RenderAttributes


class SmtpNotifierCallback(OrbiterCallback, extra="allow"):
    """
    [https://airflow.apache.org/docs/apache-airflow-providers-smtp/stable/_api/airflow/providers/smtp/notifications/smtp/index.html](https://airflow.apache.org/docs/apache-airflow-providers-smtp/stable/_api/airflow/providers/smtp/notifications/smtp/index.html)
    """

    imports: ImportList = [
        OrbiterRequirement(
            package="apache-airflow-providers-smtp",
            module="airflow.providers.smtp.notifications.smtp",
            names=["send_smtp_notification"],
        )
    ]
    function: str = "send_smtp_notification"
    render_attributes: RenderAttributes = [
        "to",
        "from_email",
        "subject",
        "html_content",
        "files",
        "cc",
        "bcc",
        "mime_subtype",
        "mime_charset",
        "custom_headers",
    ]
