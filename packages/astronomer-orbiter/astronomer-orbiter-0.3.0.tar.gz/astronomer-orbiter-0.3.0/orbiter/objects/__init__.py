from abc import ABC
from typing import List, Annotated

from pydantic import BaseModel, AfterValidator

from orbiter.objects.requirement import OrbiterRequirement


def validate_imports(v):
    assert len(v)
    for i in v:
        assert isinstance(i, OrbiterRequirement)
    return v


ImportList = Annotated[List[OrbiterRequirement], AfterValidator(validate_imports)]


class OrbiterBase(BaseModel, ABC, arbitrary_types_allowed=True):
    imports: ImportList


class OrbiterPool:
    """An Airflow Pool

    :param name: The name of the pool
    :type name: str
    :param description: The description of the pool
    :type description: str
    :param slots: The number of slots in the pool
    :type slots: int
    """

    name: str
    description: str
    slots: int

    def __hash__(self):
        return hash(f"{self.name}{self.description}{self.slots}")


class OrbiterConnection:
    """An Airflow Connection"""

    pass


class OrbiterEnvVar:
    """An Env Var - renders to a line in .env

    :param key: The key of the environment variable
    :type key: str
    :param value: The value of the environment variable
    :type value: str
    """

    key: str
    value: str


class OrbiterVariable:
    """An Airflow Variable

    :param key: The key of the variable
    :type key: str
    :param value: The value of the variable
    :type value: str
    """

    key: str
    value: str
