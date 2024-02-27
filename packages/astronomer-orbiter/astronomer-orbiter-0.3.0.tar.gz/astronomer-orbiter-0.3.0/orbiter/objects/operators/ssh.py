from __future__ import annotations

from typing import Dict

from orbiter.objects import ImportList
from orbiter.objects.requirement import OrbiterRequirement
from orbiter.objects.task import OrbiterOperator, RenderAttributes

__mermaid__ = """
--8<-- [start:mermaid-relationships]
OrbiterOperator --|> OrbiterSSHOperator
--8<-- [end:mermaid-relationships]
"""


class OrbiterSSHOperator(OrbiterOperator):
    """
    An Airflow
    [SSHOperator](https://registry.astronomer.io/providers/apache-airflow-providers-ssh/versions/latest/modules/SSHOperator)

    ```pycon
    >>> OrbiterSSHOperator(task_id="my_task", ssh_conn_id="SSH", command="echo 'hello world'")
    my_task_task = SSHOperator(task_id='my_task', ssh_conn_id='SSH', command="echo 'hello world'")

    ```
    """

    __mermaid__ = """
    --8<-- [start:mermaid-props]
    operator = "SSHOperator"
    task_id: str
    ssh_conn_id: str
    command: str
    environment: Dict[str, str] | None
    --8<-- [end:mermaid-props]
    """

    imports: ImportList = [
        OrbiterRequirement(
            package="apache-airflow",
            module="airflow.providers.ssh.operators.ssh",
            names=["SSHOperator"],
        )
    ]
    operator: str = "SSHOperator"
    render_attributes: RenderAttributes = OrbiterOperator.render_attributes + [
        "ssh_conn_id",
        "command",
        "environment",
    ]

    ssh_conn_id: str
    command: str
    environment: Dict[str, str] | None = None
