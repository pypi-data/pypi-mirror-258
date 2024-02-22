from __future__ import annotations

from typing import TYPE_CHECKING

from puffling.plugin import hookimpl
from puffling.version.source.code import CodeSource
from puffling.version.source.env import EnvSource
from puffling.version.source.regex import RegexSource

if TYPE_CHECKING:
    from puffling.version.source.plugin.interface import VersionSourceInterface


@hookimpl
def puffling_register_version_source() -> list[type[VersionSourceInterface]]:
    return [CodeSource, EnvSource, RegexSource]
