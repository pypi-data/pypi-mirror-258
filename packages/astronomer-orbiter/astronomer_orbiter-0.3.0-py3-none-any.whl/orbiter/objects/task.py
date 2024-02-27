from __future__ import annotations

import ast
from abc import ABC
from typing import Set, List, ClassVar, Annotated, Callable

from loguru import logger
from pydantic import AfterValidator, BaseModel

from orbiter.ast_helper import OrbiterASTBase, py_bitshift, py_function
from orbiter.ast_helper import py_assigned_object
from orbiter.objects import ImportList
from orbiter.objects import OrbiterBase
from orbiter.util import to_task_id

__mermaid__ = """
--8<-- [start:mermaid-dag-relationships]
OrbiterOperator --> "many" OrbiterTaskDependency
OrbiterOperator --> "many" OrbiterRequirement
--8<-- [end:mermaid-dag-relationships]

--8<-- [start:mermaid-task-relationships]
OrbiterOperator --|> OrbiterTask
--8<-- [end:mermaid-task-relationships]
"""

RenderAttributes = ClassVar[List[str]]
TaskId = Annotated[str, AfterValidator(lambda t: to_task_id(t))]


def task_add_downstream(
    self, task_id: str | List[str] | OrbiterTaskDependency
) -> "OrbiterOperator" | "OrbiterTaskGroup":  # noqa: F821
    """
    Add a downstream task dependency
    """
    if isinstance(task_id, OrbiterTaskDependency):
        task_dependency = task_id
        if task_dependency.task_id != self.task_id:
            raise ValueError(
                f"task_dependency={task_dependency} has a different task_id than {self.task_id}"
            )
        self.downstream.add(task_dependency)
        return self

    if not len(task_id):
        return self

    if len(task_id) == 1:
        task_id = task_id[0]
    downstream_task_id = (
        [to_task_id(t) for t in task_id]
        if isinstance(task_id, list)
        else to_task_id(task_id)
    )
    logger.debug(f"Adding downstream {downstream_task_id} to {self.task_id}")
    self.downstream.add(
        OrbiterTaskDependency(task_id=self.task_id, downstream=downstream_task_id)
    )
    return self


class OrbiterTaskDependency(OrbiterASTBase, BaseModel, frozen=True, extra="forbid"):
    """Represents a task dependency

    ```pycon
    >>> OrbiterTaskDependency(task_id="task_id", downstream="downstream")
    task_id_task >> downstream_task
    >>> OrbiterTaskDependency(task_id="task_id", downstream=["a", "b"])
    task_id_task >> [a_task, b_task]

    ```

    :param task_id: The task_id for the operator
    :param downstream: downstream tasks
    """

    # --8<-- [start:mermaid-td-props]
    task_id: TaskId
    downstream: TaskId | List[TaskId]

    # --8<-- [end:mermaid-td-props]

    def _to_ast(self):
        if isinstance(self.downstream, str):
            return py_bitshift(
                to_task_id(self.task_id, "_task"), to_task_id(self.downstream, "_task")
            )
        elif isinstance(self.downstream, list):
            return py_bitshift(
                to_task_id(self.task_id, "_task"),
                [to_task_id(t, "_task") for t in self.downstream],
            )


class OrbiterOperator(OrbiterASTBase, OrbiterBase, ABC, frozen=True, extra="forbid"):
    """
    Abstract class representing a
    [Task in Airflow](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html#operators),
    must be subclassed such as [OrbiterBashOperator](#orbiter.objects.operators.bash.OrbiterBashOperator)

    **Instantiation/inheriting:**
    ```pycon
    >>> from orbiter.objects import OrbiterRequirement
    >>> class OrbiterMyOperator(OrbiterOperator):
    ...   imports: ImportList = [OrbiterRequirement(package="apache-airflow")]
    ...   operator: str = "MyOperator"
    >>> foo = OrbiterMyOperator(task_id="task_id"); foo
    task_id_task = MyOperator(task_id='task_id')

    ```

    **Adding downstream tasks:**
    ```pycon
    >>> foo.add_downstream("downstream").downstream
    {task_id_task >> downstream_task}
    >>> sorted(list(foo.add_downstream(["a", "b"]).downstream))
    [task_id_task >> [a_task, b_task], task_id_task >> downstream_task]
    >>> foo.add_downstream(OrbiterTaskDependency(task_id="other", downstream="bar")).downstream
    Traceback (most recent call last):
    ValueError: Task dependency ... has a different task_id than task_id

    ```

    :param imports: List of requirements for the operator
    :param task_id: The task_id for the operator
    :param operator: operator name
    :param downstream: downstream tasks
    """

    imports: ImportList
    render_attributes: RenderAttributes = ["task_id"]

    operator: str
    task_id: TaskId
    downstream: Set[OrbiterTaskDependency] = set()

    __mermaid__ = """
    --8<-- [start:mermaid-op-props]
    imports: List[OrbiterRequirement]
    operator: str
    task_id: str
    downstream: Set[OrbiterTaskDependency]
    add_downstream(str | List[str] | OrbiterTaskDependency)
    --8<-- [end:mermaid-op-props]
    """

    def add_downstream(
        self, task_id: str | List[str] | OrbiterTaskDependency
    ) -> "OrbiterOperator":
        return task_add_downstream(self, task_id)

    def _to_ast(self) -> ast.stmt:
        def prop(k):
            attr = getattr(self, k)
            return ast.Name(id=attr.__name__) if isinstance(attr, Callable) else attr

        return py_assigned_object(
            to_task_id(self.task_id, "_task"),
            self.operator,
            **{k: prop(k) for k in self.render_attributes if k and getattr(self, k)},
        )


class OrbiterTask(OrbiterOperator, extra="allow"):
    """
    A Generic Airflow Operator - can either be subclassed for specific functionality or instantiated directly
    The operator that is instantiated is inferred from the `imports` field - the first `*Operator` or `*Sensor` is used.

    [View more info for specific operators at the Astronomer Registry.](https://registry.astronomer.io/)

    ```pycon
    >>> from orbiter.objects.requirement import OrbiterRequirement
    >>> OrbiterTask(task_id="my_task", bash_command="echo 'hello world'", other=1, imports=[
    ...   OrbiterRequirement(package="apache-airflow", module="airflow.operators.bash", names=["BashOperator"])
    ... ])
    my_task_task = BashOperator(task_id='my_task', bash_command="echo 'hello world'", other=1)

    >>> def foo():
    ...   pass
    >>> OrbiterTask(task_id="foo", python_callable=foo, other=1, imports=[
    ...   OrbiterRequirement(package="apache-airflow", module="airflow.sensors.python", names=["PythonSensor"])
    ... ])
    def foo():
        pass
    foo_task = PythonSensor(task_id='foo', other=1, python_callable=foo)

    ```

    :param task_id: The task_id for the operator
    :param imports: List of requirements for the operator (operator is inferred from first "XYZOperator")
    :param **kwargs: Any other keyword arguments to be passed to the operator
    """

    imports: ImportList
    task_id: str
    operator: None = None  # Not used
    __mermaid__ = """
    --8<-- [start:mermaid-task-props]
    <<OrbiterOperator>>
    imports: List[OrbiterRequirement]
    task_id: str
    **kwargs
    --8<-- [end:mermaid-task-props]
    """

    def _to_ast(self) -> ast.stmt:
        def prop(k):
            attr = getattr(self, k)
            return ast.Name(id=attr.__name__) if isinstance(attr, Callable) else attr

        # Figure out which operator we are talking about
        operator_names = [
            name
            for _import in self.imports
            for name in _import.names
            if "operator" in name.lower() or "sensor" in name.lower()
        ]
        if len(operator_names) != 1:
            raise ValueError(
                f"Expected exactly one operator name, got {operator_names}"
            )
        [operator] = operator_names

        self_as_ast = py_assigned_object(
            to_task_id(self.task_id, "_task"),
            operator,
            **{
                k: prop(k)
                for k in ["task_id"] + sorted(self.__pydantic_extra__.keys())
                if k and getattr(self, k)
            },
        )
        callable_props = [
            k
            for k in self.__pydantic_extra__.keys()
            if isinstance(getattr(self, k), Callable)
        ]
        return (
            [py_function(getattr(self, prop)) for prop in callable_props]
            + [self_as_ast]
            if len(callable_props)
            else self_as_ast
        )
