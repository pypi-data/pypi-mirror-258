from orbiter.objects import ImportList
from orbiter.objects.requirement import OrbiterRequirement
from orbiter.objects.task import OrbiterOperator, RenderAttributes

__mermaid__ = """
--8<-- [start:mermaid-relationships]
OrbiterOperator --|> OrbiterBashOperator
--8<-- [end:mermaid-relationships]
"""


class OrbiterBashOperator(OrbiterOperator):
    """
    An Airflow [BashOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/BashOperator)

    ```pycon
    >>> OrbiterBashOperator(task_id="my_task", bash_command="echo 'hello world'")
    my_task_task = BashOperator(task_id='my_task', bash_command="echo 'hello world'")

    ```
    """

    __mermaid__ = """
    --8<-- [start:mermaid-props]
    operator = "BashOperator"
    task_id: str
    bash_command: str
    --8<-- [end:mermaid-props]
    """

    imports: ImportList = [
        OrbiterRequirement(
            package="apache-airflow",
            module="airflow.operators.bash",
            names=["BashOperator"],
        )
    ]
    operator: str = "BashOperator"
    render_attributes: RenderAttributes = OrbiterOperator.render_attributes + [
        "bash_command"
    ]

    bash_command: str
