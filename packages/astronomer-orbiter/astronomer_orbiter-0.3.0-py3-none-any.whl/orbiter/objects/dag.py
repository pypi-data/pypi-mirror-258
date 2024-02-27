from __future__ import annotations
import ast
from datetime import datetime
from typing import List, Dict, Any, Iterable, Annotated

from pydantic import AfterValidator

from orbiter.util import to_dag_id
from orbiter.ast_helper import py_object, OrbiterASTBase, py_with
from pendulum import DateTime

from orbiter.objects import OrbiterBase, ImportList
from orbiter.objects.requirement import OrbiterRequirement
from orbiter.objects.task import OrbiterOperator
from orbiter.objects.task_group import OrbiterTaskGroup

__mermaid__ = """
--8<-- [start:mermaid-project-relationships]
OrbiterDAG --> "many" OrbiterRequirement
--8<-- [end:mermaid-project-relationships]

--8<-- [start:mermaid-dag-relationships]
OrbiterDAG --> "many" OrbiterOperator
OrbiterDAG --> "many" OrbiterTaskGroup
OrbiterDAG --> "many" OrbiterRequirement
--8<-- [end:mermaid-dag-relationships]
"""


DagId = Annotated[str, AfterValidator(lambda d: to_dag_id(d))]


def _get_imports_recursively(
    tasks: Iterable[OrbiterOperator | OrbiterTaskGroup],
) -> List[OrbiterRequirement]:
    imports = []
    for task in tasks:
        imports.extend(
            task.imports + _get_imports_recursively(task.tasks)
            if isinstance(task, OrbiterTaskGroup)
            else task.imports
        )
    return imports


class OrbiterDAG(OrbiterASTBase, OrbiterBase, frozen=True, extra="forbid"):
    """Represents an Airflow DAG, with its tasks and dependencies

    ```pycon
    >>> from orbiter.objects.operators.bash import OrbiterBashOperator
    >>> OrbiterDAG(dag_id="dag_id").add_task(
    ...   OrbiterBashOperator(task_id="task_id", bash_command="echo 'hello world'")
    ... )
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from pendulum import DateTime, Timezone
    with DAG(dag_id='dag_id', schedule=None, start_date=DateTime(1970, 1, 1, 0, 0, 0), catchup=False):
        task_id_task = BashOperator(task_id='task_id', bash_command="echo 'hello world'")

    >>> from orbiter.objects.task_group import OrbiterTaskGroup
    >>> OrbiterDAG(dag_id="dag_id").add_task(OrbiterTaskGroup(
    ...  task_group_id="foo", tasks=[OrbiterBashOperator(task_id="bar", bash_command="bar")]
    ... ))
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from airflow.utils.task_group import TaskGroup
    from pendulum import DateTime, Timezone
    with DAG(dag_id='dag_id', schedule=None, start_date=DateTime(1970, 1, 1, 0, 0, 0), catchup=False):
        with TaskGroup(group_id='foo') as foo:
            bar_task = BashOperator(task_id='bar', bash_command='bar')

    ```

    :param dag_id: The DAG ID
    :param schedule: The schedule interval for the DAG
    :param catchup: Whether to catch up on missed intervals
    :param start_date: The start date for the DAG
    :param default_args: Default arguments for the DAG
    :param doc_md: Markdown documentation for the DAG
    """

    __mermaid__ = """
    --8<-- [start:mermaid-props]
    imports: List[OrbiterRequirement]
    dag_id: str
    schedule: str | None
    catchup: bool
    start_date: DateTime
    default_args: Dict[str, Any]
    doc_md: str | None
    tasks: Dict[str, OrbiterOperator]
    add_task(OrbiterOperator)
    add_tasks(Iterable[OrbiterOperator])
    --8<-- [end:mermaid-props]
    """

    imports: ImportList = [
        OrbiterRequirement(package="apache-airflow", module="airflow", names=["DAG"]),
        OrbiterRequirement(
            package="pendulum", module="pendulum", names=["DateTime", "Timezone"]
        ),
    ]

    dag_id: DagId
    schedule: str | None = None
    catchup: bool = False
    start_date: DateTime | datetime = DateTime(1970, 1, 1)
    default_args: Dict[str, Any] = dict()
    doc_md: str | None = None

    tasks: Dict[str, OrbiterOperator | OrbiterTaskGroup] = dict()

    nullable_attributes: List[str] = ["schedule", "catchup"]
    render_attributes: List[str] = [
        "dag_id",
        "schedule",
        "start_date",
        "catchup",
        "default_args",
        "doc_md",
    ]

    def _dag_to_ast(self) -> ast.Expr:
        """
        Returns the `DAG(...)` object.
        OrbiterDAG._to_ast will handle the rest (like imports, the context manager, tasks, and task dependencies)

        ```pycon
        >>> from orbiter.ast_helper import render_ast
        >>> render_ast(OrbiterDAG(dag_id="dag_id")._dag_to_ast())
        "DAG(dag_id='dag_id', schedule=None, start_date=DateTime(1970, 1, 1, 0, 0, 0), catchup=False)"

        ```

        ```pycon
        >>> render_ast(OrbiterDAG(
        ...     dag_id="dag_id", default_args={}, schedule="@hourly", start_date=datetime(2000, 1, 1)
        ... )._dag_to_ast())
        "DAG(dag_id='dag_id', schedule='@hourly', start_date=datetime.datetime(2000, 1, 1, 0, 0), catchup=False)"

        ```
        :return: `DAG(...)` as an ast.Expr
        """
        return py_object(
            name="DAG",
            **{
                k: getattr(self, k)
                for k in self.render_attributes
                if getattr(self, k) or k in self.nullable_attributes
            },
        )

    def add_task(self, task: OrbiterOperator | OrbiterTaskGroup) -> "OrbiterDAG":
        """Add a task to the DAG"""
        try:
            task_id = getattr(task, "task_id", None) or getattr(task, "task_group_id")
        except AttributeError:
            raise AttributeError(
                f"Task {task} does not have a task_id or task_group_id attribute"
            )
        self.tasks[task_id] = task
        return self

    def add_tasks(
        self, tasks: Iterable[OrbiterOperator | OrbiterTaskGroup]
    ) -> "OrbiterDAG":
        """Add tasks to the DAG"""
        for task in tasks:
            self.add_task(task)
        return self

    # noinspection PyProtectedMember
    def _to_ast(self) -> List[ast.stmt]:
        # DAG Imports, e.g. `from airflow import DAG`
        # Task/TaskGroup Imports, e.g. `from airflow.operators.bash import BashOperator`
        imports = [
            i._to_ast()
            for i in sorted(
                list(set(self.imports + _get_imports_recursively(self.tasks.values())))
            )
        ]

        # foo = BashOperator(...)
        task_definitions = [task._to_ast() for task in self.tasks.values()]

        # foo >> bar
        task_dependencies = [
            downstream._to_ast()
            for task in self.tasks.values()
            for downstream in task.downstream
        ]

        # with DAG(...) as dag:
        with_dag = py_with(
            self._dag_to_ast().value, body=task_definitions + task_dependencies
        )
        return [
            *imports,
            with_dag,
        ]
