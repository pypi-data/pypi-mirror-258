from __future__ import annotations

from orbiter.objects import OrbiterRequirement, ImportList
from orbiter.objects.task import OrbiterOperator, RenderAttributes

__mermaid__ = """
--8<-- [start:mermaid-relationships]
OrbiterOperator --|> OrbiterEmailOperator
--8<-- [end:mermaid-relationships]
"""


class OrbiterEmailOperator(OrbiterOperator):
    # noinspection GrazieInspection
    """
    An Airflow [EmailOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/EmailOperator)

    ```pycon
    >>> OrbiterEmailOperator(
    ...   task_id="foo", to="humans@astronomer.io", subject="Hello", html_content="World!"
    ... )
    foo_task = EmailOperator(task_id='foo', to='humans@astronomer.io', subject='Hello', html_content='World!')

    ```
    """
    __mermaid__ = """
    --8<-- [start:mermaid-props]
    operator = "EmailOperator"
    task_id: str
    to: str | list[str]
    subject: str
    html_content: str
    files: list | None
    --8<-- [end:mermaid-props]
    """

    imports: ImportList = [
        OrbiterRequirement(
            package="apache-airflow-providers-smtp",
            module="airflow.providers.smtp.operators.smtp",
            names=["EmailOperator"],
        )
    ]
    operator: str = "EmailOperator"
    render_attributes: RenderAttributes = OrbiterOperator.render_attributes + [
        "to",
        "subject",
        "html_content",
        "files",
    ]
    to: str | list[str]
    subject: str
    html_content: str
    files: list | None = []
