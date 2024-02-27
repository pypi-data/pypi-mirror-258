from __future__ import annotations
import json
import re
from abc import ABC
from copy import deepcopy
from pathlib import Path
from typing import (
    List,
    Any,
    Collection,
    Dict,
    Type,
    Annotated,
    ClassVar,
    Callable,
    Union,
)

from loguru import logger
from pydantic import BaseModel, Field, AfterValidator, validate_call

from orbiter import FileType
from orbiter.util import import_from_qualname, load_filetype
from orbiter.objects.dag import OrbiterDAG
from orbiter.objects.project import OrbiterProject
from orbiter.objects.task import OrbiterOperator, OrbiterTaskDependency

qualname_validator_regex = r"^[\w.]+$"
qualname_validator = re.compile(qualname_validator_regex)


def validate_translate_fn(
    translate_fn: str | Callable[[dict, "TranslationRuleset"], OrbiterProject]
) -> str | Callable[[dict, "TranslationRuleset"], OrbiterProject]:
    # noinspection PyTypeChecker
    """
    ```pycon
    >>> validate_translate_fn(fake_translate) # a valid function works # doctest: +ELLIPSIS
    <function fake_translate at ...>
    >>> validate_translate_fn("orbiter.rules.fake_translate") # a valid qualified name works  # doctest: +ELLIPSIS
    <function fake_translate at ...>
    >>> validate_translate_fn(json.loads)
    Traceback (most recent call last):
    AssertionError: translate_fn=<function ...> must take two arguments
    >>> validate_translate_fn("???")
    Traceback (most recent call last):
    AssertionError:

    ```
    """
    if isinstance(translate_fn, Callable):
        # noinspection PyUnresolvedReferences
        assert (
            translate_fn.__code__.co_argcount == 2
        ), f"{translate_fn=} must take two arguments"
    if isinstance(translate_fn, str):
        validate_qualified_imports([translate_fn])
        (_, _translate_fn) = import_from_qualname(translate_fn)
        translate_fn = _translate_fn
    return translate_fn


def validate_qualified_imports(qualified_imports: List[str]) -> List[str]:
    """
    ```pycon
    >>> validate_qualified_imports(["json", "package.module.Class"])
    ['json', 'package.module.Class']

    ```
    """
    for _qualname in qualified_imports:
        assert qualname_validator.match(_qualname), (
            f"Import Qualified Name='{_qualname}' is not valid."
            f"Qualified Names must match regex {qualname_validator_regex}"
        )
    return qualified_imports


QualifiedImport = Annotated[str, AfterValidator(validate_qualified_imports)]

TranslateFn = Annotated[
    Union[QualifiedImport, Callable[[dict, "TranslationRuleset"], OrbiterProject]],
    AfterValidator(validate_translate_fn),
]


class PydanticLoadMixin:
    @classmethod
    @validate_call
    def from_file(cls, file: Path, file_type: FileType):
        """Load a TranslationRuleset from a file
        :return:TranslationRuleset
        """
        return cls.from_json(json.dumps(load_filetype(file.read_text(), file_type)))

    @classmethod
    @validate_call
    def from_json(cls, input_json: str):
        """Load a TranslationRuleset from a json file
        :return:TranslationRuleset
        """
        # noinspection PyUnresolvedReferences
        return cls.model_validate_json(input_json)


class Rule(BaseModel, PydanticLoadMixin, frozen=True, extra="forbid"):
    # noinspection Pydantic
    """
    A Rule evaluates python code and return either one of Any or None

    ## Rule Overview
    see Rule.evaluate for more specifics

    - Rule can evaluate to `Any`
    ```pycon
    >>> Rule(rule="4").evaluate()
    4

    ```

    - or Rule can evaluate to `None`
    ```pycon
    >>> Rule(rule="None").evaluate()

    ```

    - A Rule MUST evaluate to `Any | None`. Other evaluations like assignment are invalid
    ```pycon
    >>> Rule(rule="a = 1").evaluate()
    Traceback (most recent call last):
    RuntimeError: ...

    ```

    ## Rule Object Validation

    - A `Rule` must have a rule, expressed as Rule(rule="...") or Rule(**{"rule": "..."})
    ```pycon
    >>> Rule()
    Traceback (most recent call last):
    pydantic_core._pydantic_core.ValidationError: ...

    ```

    - Extra properties cannot be passed
    ```pycon
    >>> Rule(not_a_prop="???")
    Traceback (most recent call last):
    pydantic_core._pydantic_core.ValidationError: ...
    ```
    """

    rule: str
    """Python Code to evaluate. Must evaluate to one of Any or None"""

    priority: int = Field(0, ge=0)
    """Higher priority rules are evaluated first"""

    name: str = ""
    """Optional name for the rule"""

    description: str = ""
    """Optional description for the rule"""

    qualified_imports: List[QualifiedImport] = []
    """ Qualified names to import for use in the rule, "e.g. `json` or `package.module.Class`"""

    output_type: Type | None = None
    """Optional Type representing the output of the rules,
    for post-processing validation, overrides ruleset output_type (if specified)"""

    def _import(self) -> Dict[str, Any]:
        # noinspection GrazieInspection
        """Private method - used prior to `evaluate` to import any qualified names
        Do the actual imports, returning a dict of name: imported_object
        ```pycon
        >>> Rule(rule="", qualified_imports=["json"])._import() # doctest: +ELLIPSIS
        {'json': <module 'json' from '...'>}

        ```
        """
        return dict(
            import_from_qualname(qualified_name)
            for qualified_name in self.qualified_imports
        )

    def evaluate(
        self,
        global_dict: dict | None = None,
        output_type: Type | None = None,
        **kwargs,
    ) -> Any | None:
        # noinspection PyTypeChecker
        """
        Evaluate a Rule, returning either

        - a SINGLE python primitive or object
        - or None

        The evaluation has access to any qualified name imports provided on the `Rule`
        e.g. `OrbiterDAG` if it was given `qualified_imports=["orbiter.objects.dag.OrbiterDAG"]`

        - Rule.evaluate can be applied over dict items
        ```pycon
        >>> for item in {"a": 1, "b": 2}.items():
        ...   print(Rule(rule="{key: val} if key == 'b' else None").evaluate(key=item[0], val=item[1]))
        None
        {'b': 2}

        ```

        - Simple map over a non-dict value
        ```pycon
        >>> Rule(rule="str(val) if val > 4 else None").evaluate(val=5)
        '5'

        ```

        - for usage in a filter, return a boolean
        ```pycon
        >>> for k, v in {"a": 1}.items():
        ...  Rule(rule="int(val) > 4").evaluate(val=v)
        False

        ```

        :param global_dict: optional dictionary, referenceable from the evaluation as "global", if provided
        :param output_type: optionally override the output_type of the rule
                        (such as setting it once over whole the ruleset)
        :param kwargs: any kwargs passed to evaluate are available to the evaluation as variables
        :return: Any | None
        :raises RuntimeError: if the Rule raises an exception
        """
        # Setup environment
        imports = self._import()
        copied_kwargs = deepcopy(kwargs)
        env = {**copied_kwargs, "global": global_dict or {}} | imports

        # Evaluate rule
        try:
            result = eval(self.rule, env)
        except Exception as e:
            raise RuntimeError(f"Exception in Rule({self}) on input={kwargs}") from e
        output_type = output_type or self.output_type
        if (
            result is not None
            and output_type is not None
            and not isinstance(result, output_type)
        ):
            raise RuntimeError(
                f"Rule({self}) evaluated to {result=} which is not of type {output_type}"
            )
        return result


class Ruleset(BaseModel, frozen=True, extra="forbid"):
    # noinspection PyTypeChecker
    """
    A list of rules, which are evaluated to generate different types of output

    - You can pass either `Rule | dict` (with the schema of a Rule)
    ```pycon
    >>> Ruleset(ruleset=[Rule(rule="None"), {"rule": "None"}]) # doctest: +ELLIPSIS
    Ruleset(ruleset=[Rule(...), Rule(...)])

    ```
    - But you can't pass non-Rules
    ```pycon
    >>> Ruleset(ruleset=[None])
    Traceback (most recent call last):
    pydantic_core._pydantic_core.ValidationError: ...

    ```
    """
    output_type: ClassVar[Type | None] = None
    """Type representing the output of the ruleset, for post-processing validation"""

    ruleset: List[Rule]
    """Rules to apply"""

    def apply_many(
        self,
        input_val: Collection[Any],
        global_dict: dict | None = None,
        take_first: bool = False,
    ) -> List[List[Any]] | List[Any]:
        """
        Apply a ruleset to each item in collection (such as dict.items())
        returning any items that evaluate to Any

        - you can turn the output back into a dict
        ```pycon
        >>> ruleset = Ruleset(ruleset=[
        ...    Rule(rule="(key, val) if key != 'Defaults' and val.get('Type') == 'Folder' else None")
        ... ])
        >>> input_dict = {
        ...    "Defaults": {"Type": "Folder"},
        ...    "a": {"Type": "Folder"},
        ...    "b": {"Type": "File"},
        ...    "c": {"Type": "Folder"},
        ... }
        >>> from itertools import chain
        >>> dict(chain(*chain(ruleset.apply_many(input_dict.items()))))
        {'a': {'Type': 'Folder'}, 'c': {'Type': 'Folder'}}
        >>> dict(ruleset.apply_many(input_dict.items(), take_first=True))
        {'a': {'Type': 'Folder'}, 'c': {'Type': 'Folder'}}

        ```

        ```pycon
        >>> ruleset.apply_many({})
        Traceback (most recent call last):
        RuntimeError: Input is not Collection[Any] with length!

        ```
        :param input_val: Collection[Any] to evaluate ruleset over
            key and val are supplied if it's a tuple (dict.items())
            key and val are both the item if it's not a tuple (e.g. list)
        :param global_dict: dictionary of globals, reference-able from the evaluated fn as "global"
        :param take_first: only take the first (if any) result from each ruleset application
        :returns: List[List[Any]] of items with all non-null evaluations
                  or List[Any] of items and the first non-null evaluation if take_first=True
        :raises RuntimeError: if the Ruleset or input_vals are empty
        :raises RuntimeError: if the Rule raises an exception
        """
        # Validate Input
        if not input_val or not len(input_val):
            raise RuntimeError("Input is not Collection[Any] with length!")

        return [
            results[0] if take_first else results
            for item in input_val
            if (
                results := self.apply(
                    global_dict=global_dict,
                    take_first=False,
                    key=item[0] if isinstance(item, tuple) else item,
                    val=item[1] if isinstance(item, tuple) else item,
                )
            )
            is not None
            and len(results)
        ]

    def _sorted(self) -> List[Rule]:
        """Return a copy of the ruleset, sorted by priority
        ```pycon
        >>> sorted_rules = Ruleset(ruleset=[Rule(rule="1", priority=1), Rule(rule="99", priority=99)])._sorted()
        >>> sorted_rules[0].priority
        99
        >>> sorted_rules[-1].priority
        1

        ```
        """
        return sorted(self.ruleset, key=lambda r: r.priority, reverse=True)

    @validate_call
    def apply(
        self, global_dict: dict | None = None, take_first: bool = False, **kwargs
    ) -> List[Any] | Any:
        """
        Apply all rules in ruleset **to a single item** in priority order, removing any None results.

        - one rule, one match
        ```pycon
        >>> Ruleset(ruleset=[Rule(rule="str(val) if val > 4 else None")]).apply(val=5)
        ['5']

        ```

        - many rules, many matches
        ```pycon
        >>> Ruleset(ruleset=[
        ...   Rule(rule="str(val) if val > 4 else None"),
        ...   Rule(rule="str(val) if val > 3 else None")
        ... ]).apply(val=5)
        ['5', '5']

        ```

        - `take_first` returns first match
        ```pycon
        >>> Ruleset(ruleset=[
        ...   Rule(rule="str(val) if val > 4 else None"),
        ...   Rule(rule="str(val) if val > 3 else None")
        ... ]).apply(val=5, take_first=True)
        '5'

        ```

        - if nothing matched, returns empty list
        ```pycon
        >>> Ruleset(ruleset=[
        ...   Rule(rule="None"),
        ...   Rule(rule="None")
        ...  ]).apply(val=5)
        []

        ```

        - Returns None, nothing matched and take_first=True
        ```pycon
        >>> Ruleset(ruleset=[
        ...   Rule(rule="None"),
        ...   Rule(rule="None")
        ... ]).apply(val=5, take_first=True)

        ```

        - error if no input
        ```pycon
        >>> Ruleset(ruleset=[Rule(rule="None")]).apply(None)
        Traceback (most recent call last):
        RuntimeError: No values provided! Supply at least one key=val pair as kwargs!

        ```
        :param global_dict: dictionary of globals to pass to rule evaluation
        :param take_first: only take the first (if any) result from the ruleset application
        :param kwargs: key=val pairs to pass to the evaluated fn
        :returns: List[Any] in order of priority of rules that evaluated to Any,
                    or an empty list,
                    or Any if take_first=True
        :raises RuntimeError: if the Ruleset is empty or input_val is None
        :raises RuntimeError: if the Rule raises an exception
        """
        if not len(kwargs):
            raise RuntimeError(
                "No values provided! Supply at least one key=val pair as kwargs!"
            )
        results = [
            result
            for rule in self._sorted()
            if (result := rule.evaluate(global_dict=global_dict, **kwargs)) is not None
        ]
        return (results[0] if len(results) else None) if take_first else results


class DAGFilterRuleset(Ruleset):
    """DAG Filter Rulesets are a list of Rules that take a dict and filter it to dag-like-entries"""

    output_type = dict


class DAGRuleset(Ruleset):
    """A DAG Ruleset is a list of Rules that evaluate to an OrbiterDAG"""

    output_type = OrbiterDAG


class TaskRuleset(Ruleset):
    """A Task Ruleset is a list of Rules that evaluate to an OrbiterTask"""

    output_type = OrbiterOperator


class TaskDependencyRuleset(Ruleset):
    """A Task Dependency Ruleset is a list of Rules that evaluate OrbiterTaskDependency"""

    output_type = OrbiterTaskDependency


class TranslationRuleset(BaseModel, PydanticLoadMixin, ABC, extra="forbid"):
    """A container for rulesets, which applies to a given type of translation

    - Can be initialized with a dict, or as a python object
    ```pycon
    >>> translation_ruleset = {
    ...   "file_type": FileType.JSON,                       # And a file type
    ...   "translate_fn": "orbiter.rules.fake_translate",   # and can have a callable or a qualified name to a function
    ...   "dag_filter_ruleset": {"ruleset": [{"rule": 'None'}]},  # Rulesets can be dict within dicts
    ...   "dag_ruleset": DAGRuleset(ruleset=[Rule(rule="None")]), # or python objects within python objects, or a mix
    ...   "task_ruleset": EMPTY_RULESET,                    # Omitted for brevity
    ...   "task_dependency_ruleset": EMPTY_RULESET,
    ... }
    >>> TranslationRuleset(**translation_ruleset) # doctest: +ELLIPSIS
    TranslationRuleset(...)

    ```
    """

    file_type: FileType
    """FileType to translate - e.g. .json"""

    dag_filter_ruleset: DAGFilterRuleset
    """Ruleset which filters a dict to dag-like-entries"""

    dag_ruleset: DAGRuleset
    """Ruleset which evaluates to an OrbiterDAG"""

    task_ruleset: TaskRuleset
    """Ruleset which evaluates to an OrbiterTask"""

    task_dependency_ruleset: TaskDependencyRuleset
    """Ruleset which evaluates to an OrbiterTaskDependency"""

    translate_fn: TranslateFn
    """Either a qualified name to a function or a callable
    which takes a dict and this TranslationRuleset and returns an OrbiterProject"""

    @validate_call
    def _translate_folder(self, input_dir: Path) -> OrbiterProject:
        """Translate all files in a folder, recursively
        :param input_dir: the directory to translate_fn
        :raises RuntimeError: if output of translate_file is not an OrbiterProject
        """

        def translate_file(_file: Path) -> OrbiterProject:
            """Translate a single file using project_ruleset"""
            logger.info(f"Translating file={_file.resolve()}")
            _project = self.translate_fn(
                load_filetype(_file.read_text(), self.file_type), self
            )
            if not isinstance(_project, OrbiterProject):
                raise RuntimeError(
                    f"{self}.translate_fn produced {type(_project)} not OrbiterProject"
                )
            return _project

        project = OrbiterProject()
        for file in input_dir.iterdir():
            if file.is_dir():
                project += self._translate_folder(input_dir=file)
            elif self.file_type.value.lower() in file.suffix:
                project += translate_file(file)
            else:
                logger.debug(
                    f"WARN: Skipping file={file.resolve()} because it "
                    f"is not a {self.file_type.value.lower()} or directory"
                )
        return project


def translate(
    input_dict: Dict[str, Any],
    translation_ruleset: TranslationRuleset,
) -> OrbiterProject:
    """Default translation function, which applies each ruleset in order.
    Expects a structure like:
    ```json
    {"dag_id": { ...dag_props, "task_id": { ...task_props} }}
    ```
    """
    project = OrbiterProject()

    # DAG FILTER Ruleset
    for dag_id, dag_dict in dict(
        translation_ruleset.dag_filter_ruleset.apply_many(
            input_dict.items(), global_dict=input_dict, take_first=True
        )
    ).items():
        # DAG Ruleset - one -> one
        dag: OrbiterDAG | None = translation_ruleset.dag_ruleset.apply(
            key=dag_id,
            val=dag_dict,
            global_dict=input_dict,
            take_first=True,
        )
        if dag is None:
            logger.debug(
                f"WARN: Couldn't extract DAG from dag_dict={dag_dict} "
                f"with dag_ruleset={translation_ruleset.dag_ruleset}"
            )
            continue

        # TASK Ruleset many -> many
        tasks: List[OrbiterOperator] = translation_ruleset.task_ruleset.apply_many(
            [(k, v) for k, v in dag_dict.items() if isinstance(v, dict)],
            global_dict=input_dict,
            take_first=True,
        )
        if not len(tasks):
            logger.debug(
                f"WARN: Couldn't extract any tasks from "
                f"dag_dict={dag_dict} with dag_ruleset={translation_ruleset.dag_ruleset}"
            )
            continue
        # reshape for quick lookup
        tasks: Dict[str, OrbiterOperator] = {task.task_id: task for task in tasks}

        # TASK DEPENDENCY Ruleset
        task_dependencies: List[
            List[OrbiterTaskDependency]
        ] = translation_ruleset.task_dependency_ruleset.apply_many(
            dag_dict.items(), global_dict=input_dict, take_first=True
        )
        if len(task_dependencies) == 1:
            [task_dependencies] = task_dependencies
        elif len(task_dependencies) > 1:
            logger.debug(
                f"WARN: Extracted more than one list of task dependencies from dag_dict={dag_dict} "
                f"with task_dependency_ruleset={translation_ruleset.task_dependency_ruleset}. "
                "Possible error? Using first list."
            )
        for task_dep in task_dependencies:
            task_dep: OrbiterTaskDependency
            if task_dep.task_id not in tasks:
                logger.debug(
                    f"WARN: Couldn't find task_id={task_dep.task_id} in tasks={tasks} for dag_id={dag_id}"
                )
                continue
            else:
                tasks[task_dep.task_id].add_downstream(task_dep)

        project.add_dag(dag.add_tasks(tasks.values()))
    return project


# Empty / Fake items for testing
def fake_translate(
    input_dict: dict, translation_ruleset: TranslationRuleset
) -> OrbiterProject:
    """Fake translate function for testing"""
    _ = (input_dict, translation_ruleset)
    return OrbiterProject()


EMPTY_RULE = Rule(
    rule="None", priority=0, name="Default rule", description="Nothing matched"
)
EMPTY_RULESET = {"ruleset": [EMPTY_RULE]}
