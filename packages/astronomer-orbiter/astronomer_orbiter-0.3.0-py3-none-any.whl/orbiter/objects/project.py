from pathlib import Path
from typing import Set, Dict, Iterable

from orbiter.objects.dag import OrbiterDAG
from orbiter.objects.requirement import OrbiterRequirement
from loguru import logger

__mermaid__ = """
--8<-- [start:mermaid-relationships]
OrbiterProject --> "many" OrbiterDAG
OrbiterProject --o "many" OrbiterRequirement
--8<-- [end:mermaid-relationships]
"""


class OrbiterProject:
    """An orbiter project holds all intermediate objects needs to assemble the final output of translation

    They can be added together
    ```pycon
    >>> OrbiterProject() + OrbiterProject()
    OrbiterProject(dags=[], requirements=set())

    ```

    And compared
    ```
    >>> OrbiterProject() == OrbiterProject()
    True

    ```
    """

    __mermaid__ = """
    --8<-- [start:mermaid-props]
    dags: Dict[str, OrbiterDAG]
    requirements: Set[OrbiterRequirement]
    add_dag(OrbiterDAG)
    add_dags(Iterable[OrbiterDAG])
    add_requirement(OrbiterRequirement)
    add_requirements(Iterable[OrbiterRequirement])
    --8<-- [end:mermaid-props]
    """

    def __init__(self):
        self.dags: Dict[str, OrbiterDAG] = dict()
        self.requirements: Set[OrbiterRequirement] = set()

    def __add__(self, other) -> "OrbiterProject":
        if not other:
            return self
        if not isinstance(other, OrbiterProject):
            raise TypeError(f"Expected OrbiterProject, got {type(other)}")
        self.add_dags(other.dags.values())
        self.add_requirements(other.requirements)
        return self

    def __eq__(self, other) -> bool:
        return all(
            [str(self.dags[d]) == str(other.dags[d]) for d in self.dags]
            + [str(self.dags[d]) == str(other.dags[d]) for d in other.dags]
            + [self.requirements == other.requirements]
        )

    def __repr__(self):
        return f"OrbiterProject(dags=[{','.join(self.dags.keys())}], requirements={self.requirements})"

    def add_dag(self, dag: OrbiterDAG) -> "OrbiterProject":
        """Add DAG File (and its Requirements) to the Project"""
        if not isinstance(dag, OrbiterDAG):
            raise TypeError(f"Expected OrbiterDAG, got {type(dag)}")
        dag_id = dag.dag_id
        self.dags[dag_id] = dag
        self.add_requirements(dag.imports)
        for task in (dag.tasks or {}).values():
            self.add_requirements(task.imports)
        return self

    def add_dags(self, dags: Iterable[OrbiterDAG]) -> "OrbiterProject":
        """Add DAG Files (and their Requirements) to the Project"""
        if not isinstance(dags, Iterable):
            raise TypeError(f"Expected List[OrbiterDAG], got {type(dags)}")
        for dag in dags:
            self.add_dag(dag)
        return self

    def add_requirement(self, requirement: OrbiterRequirement) -> "OrbiterProject":
        """Add Requirement to the Project"""
        if not isinstance(requirement, OrbiterRequirement):
            raise TypeError(f"Expected OrbiterRequirement, got {type(requirement)}")
        self.requirements.add(requirement)
        return self

    def add_requirements(
        self, requirements: Iterable[OrbiterRequirement]
    ) -> "OrbiterProject":
        """Add Requirements to the Project"""
        if not isinstance(requirements, Iterable):
            raise TypeError(
                f"Expected List[OrbiterRequirement], got {type(requirements)}"
            )
        for requirement in requirements:
            self.add_requirement(requirement)
        return self

    def render(self, output_dir: Path) -> None:
        if not len(self.dags):
            raise RuntimeError("No DAGs to render!")

        dags = output_dir / "dags"
        logger.info(f"Writing {dags}")
        dags.mkdir(exist_ok=True)

        for dag_id, dag in self.dags.items():
            dag_file = dags / f"{dag_id}.py"
            logger.debug(f"Writing {dag_file}\n{dag}")
            dag_file.write_text(str(dag))

        requirements = output_dir / "requirements.txt"
        logger.info(f"Writing {requirements}")
        requirements.write_text(
            "\n".join(sorted(list({r.package for r in self.requirements if r.package})))
        )

        packages = output_dir / "packages.txt"
        logger.info(f"Writing {packages}")
        packages.write_text(
            "\n".join(
                sorted(
                    list({r.sys_package for r in self.requirements if r.sys_package})
                )
            )
        )
