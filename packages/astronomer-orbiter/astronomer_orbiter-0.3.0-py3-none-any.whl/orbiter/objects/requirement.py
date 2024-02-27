from __future__ import annotations

import ast
from typing import List

from orbiter.ast_helper import py_import, OrbiterASTBase
from pydantic import BaseModel


class OrbiterRequirement(OrbiterASTBase, BaseModel, frozen=True, extra="forbid"):
    """
    A requirement for a project. e.g. `apache-airflow-providers-google`, and it's representation in the DAG file.

    ```pycon
    >>> OrbiterRequirement(package="apache-airflow",module="airflow.operators.bash",names=["BashOperator"])
    from airflow.operators.bash import BashOperator

    ```

    :param package: e.g. `"apache-airflow-providers-google"`
    :type package: str
    :param module: e.g. `"airflow.providers.google.cloud.operators.bigquery"`, defaults to `None`
    :type module: str, optional
    :param names: e.g. `["BigQueryCreateEmptyDatasetOperator"]`, defaults to `[]`
    :type names: List[str], optional
    :param sys_package: e.g. `"mysql"` - represents a **Debian** system package
    :type sys_package: str, optional
    """

    __mermaid__ = """
    --8<-- [start:mermaid-props]
    package: str
    module: str | None
    names: List[str] | None
    sys_package: str | None
    --8<-- [end:mermaid-props]
    """

    package: str
    module: str | None = None
    names: List[str] | None = []
    sys_package: str | None = None

    def _to_ast(self) -> ast.stmt | ast.Module:
        """
        :return: ast.ImportFrom
        """
        return py_import(self.module, self.names)
