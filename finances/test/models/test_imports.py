import inspect

import pytest

from recipes import models
from recipes.models.base import Model


@pytest.mark.parametrize("package", [models])
def test_flattened_models(package):
    """Get all models in a package and verify that they are also available at the top level."""
    top_level_classes = dict()
    packaged_classes = dict()
    for name, obj in inspect.getmembers(package):
        if inspect.ismodule(obj):
            for name, mod_obj in inspect.getmembers(obj, inspect.isclass):
                if issubclass(mod_obj, Model) and mod_obj is not Model:
                    packaged_classes[name] = mod_obj
        elif inspect.isclass(obj):
            top_level_classes[name] = "top-level"
        # TODO: recurse into packages

    assert top_level_classes.keys() == packaged_classes.keys(), \
        "Expected all classes in {} to also be imported at the top-level package, i.e., {}/__init__.py. " \
        "Add these lines to that file:\n{}".format(
            package.__name__,
            package.__name__.replace(".", "/"),
            "\n".join(
                ["from .{} import {}".format(
                    packaged_classes[k].__module__.lstrip(package.__name__),
                    packaged_classes[k].__name__
                ) for k in packaged_classes.keys() - top_level_classes.keys()]
            )
        )
