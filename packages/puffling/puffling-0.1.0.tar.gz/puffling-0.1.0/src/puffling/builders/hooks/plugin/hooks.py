from __future__ import annotations

import typing

from puffling.builders.hooks.custom import CustomBuildHook
from puffling.builders.hooks.version import VersionBuildHook
from puffling.plugin import hookimpl

if typing.TYPE_CHECKING:
    from puffling.builders.hooks.plugin.interface import BuildHookInterface


@hookimpl
def puffling_register_build_hook() -> list[type[BuildHookInterface]]:
    return [CustomBuildHook, VersionBuildHook]  # type: ignore
