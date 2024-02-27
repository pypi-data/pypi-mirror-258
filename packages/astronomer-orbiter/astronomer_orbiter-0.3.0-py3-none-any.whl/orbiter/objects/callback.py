import ast
from abc import ABC

from orbiter.objects import OrbiterBase, OrbiterRequirement, ImportList
from orbiter.ast_helper import py_object, OrbiterASTBase
from orbiter.objects.task import RenderAttributes


class OrbiterCallback(OrbiterASTBase, OrbiterBase, ABC, frozen=True, extra="forbid"):
    """
    >>> class OrbiterMyCallback(OrbiterCallback):
    ...   function: str = "my_callback"
    ...   foo: str
    ...   bar: str
    ...   render_attributes: RenderAttributes = ["foo", "bar"]
    >>> OrbiterMyCallback(foo="fop", bar="bop")
    my_callback(foo='fop', bar='bop')
    """

    imports: ImportList = [OrbiterRequirement(package="apache-airflow")]
    function: str
    render_attributes: RenderAttributes = []

    def _to_ast(self) -> ast.Expr:
        return py_object(
            name=self.function,
            **{
                k: getattr(self, k)
                for k in self.render_attributes
                if k and getattr(self, k)
            },
        )
