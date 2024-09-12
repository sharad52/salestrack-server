import typing
from importlib import import_module
from pathlib import Path


def resolve_component_module_locations(
    components: typing.List[str], module_name: str
) -> typing.List[Path]:
    """resolve component module locations for defined components"""
    locations = []
    for modname in components:
        mod = import_module(modname)
        locations.append(Path(mod.__file__).parent.joinpath(module_name))
    return locations