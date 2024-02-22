from __future__ import annotations

import typing

from puffling.builders.app import AppBuilder
from puffling.builders.custom import CustomBuilder
from puffling.builders.sdist import SdistBuilder
from puffling.builders.wheel import WheelBuilder
from puffling.plugin import hookimpl

if typing.TYPE_CHECKING:
    from puffling.builders.plugin.interface import BuilderInterface


@hookimpl
def puffling_register_builder() -> list[type[BuilderInterface]]:
    return [AppBuilder, CustomBuilder, SdistBuilder, WheelBuilder]  # type: ignore
