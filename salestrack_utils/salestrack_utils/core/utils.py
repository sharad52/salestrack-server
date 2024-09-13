import typing
from importlib import import_module
from pathlib import Path


def resolve_component_module_location(
    component: str, module_name: str
) -> Path:
    """resolve component module locations for defined component"""
    module = import_module(component)
    return Path(module.__file__).parent.joinpath(module_name)