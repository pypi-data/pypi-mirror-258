from __future__ import annotations
from typing import Callable

from orbiter.ast_helper import py_function
from orbiter.objects import ImportList
from orbiter.objects.requirement import OrbiterRequirement
from orbiter.objects.task import OrbiterOperator, RenderAttributes

__mermaid__ = """
--8<-- [start:mermaid-relationships]
OrbiterOperator --|> OrbiterPythonOperator
--8<-- [end:mermaid-relationships]
"""


class OrbiterPythonOperator(OrbiterOperator):
    """
    An Airflow [PythonOperator](https://registry.astronomer.io/providers/apache-airflow/versions/latest/modules/PythonOperator)


    ```pycon
    >>> def foo(a, b):
    ...    print(a + b)
    >>> OrbiterPythonOperator(task_id="my_task", python_callable=foo)
    def foo(a, b):
       print(a + b)
    my_task_task = PythonOperator(task_id='my_task', python_callable=foo)

    ```
    """

    __mermaid__ = """
    --8<-- [start:mermaid-props]
    operator = "PythonOperator"
    task_id: str
    python_callable: Callable
    op_args: list | None
    op_kwargs: dict | None
    --8<-- [end:mermaid-props]
    """

    imports: ImportList = [
        OrbiterRequirement(
            package="apache-airflow",
            module="airflow.operators.python",
            names=["PythonOperator"],
        )
    ]
    operator: str = "PythonOperator"
    render_attributes: RenderAttributes = OrbiterOperator.render_attributes + [
        "python_callable",
        "op_args",
        "op_kwargs",
    ]

    python_callable: Callable
    op_args: list | None = None
    op_kwargs: dict | None = None

    def _to_ast(self):
        return [py_function(self.python_callable), super()._to_ast()]
