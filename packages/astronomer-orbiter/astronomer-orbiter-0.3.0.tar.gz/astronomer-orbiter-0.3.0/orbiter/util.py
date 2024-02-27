from typing import Literal, Tuple, Any

from orbiter import FileType
import inflection
from pydantic import validate_call


@validate_call
def to_task_id(task_id: str, assignment_suffix: Literal["", "_task"] = "") -> str:
    # noinspection PyTypeChecker
    """General utiltty function - turns MyTaskId into my_task_id (or my_task_id_task suffix is `_task`)
    :param task_id:
    :param assignment_suffix: e.g. `_task` for `task_id_task = MyOperator(...)`
    >>> to_task_id("MyTaskId")
    'my_task_id'
    >>> to_task_id("MyTaskId", "_task")
    'my_task_id_task'
    >>> to_task_id("MyTaskId", "_other")
    Traceback (most recent call last):
    pydantic_core._pydantic_core.ValidationError: ...
    """
    return inflection.underscore(task_id) + assignment_suffix


def import_from_qualname(qualname) -> Tuple[str, Any]:
    """Import a function or module from a qualified name
    :param qualname: The qualified name of the function or module to import (e.g. a.b.d.MyOperator or json)
    :return Tuple[str, Any]: The name of the function or module, and the function or module itself
    >>> import_from_qualname('json.loads') # doctest: +ELLIPSIS
    ('loads', <function loads at ...>)
    >>> import_from_qualname('json') # doctest: +ELLIPSIS
    ('json', <module 'json' from '...'>)
    """
    from importlib import import_module

    [module, name] = (
        qualname.rsplit(".", 1) if "." in qualname else [qualname, qualname]
    )
    imported_module = import_module(module)
    return (
        name,
        getattr(imported_module, name) if "." in qualname else imported_module,
    )


@validate_call
def load_filetype(input_str: str, file_type: FileType) -> dict:
    if file_type == FileType.JSON:
        import json

        return json.loads(input_str)
    elif file_type == FileType.YAML:
        import yaml

        return yaml.safe_load(input_str)
    elif file_type == FileType.XML:
        import xmltodict

        return xmltodict.parse(input_str)
    else:
        raise NotImplementedError(f"Cannot load {file_type=}")


@validate_call
def to_dag_id(s: str) -> str:
    return inflection.underscore(s)
