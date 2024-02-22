from __future__ import annotations

from typing import TYPE_CHECKING

from puffling.plugin import hookimpl
from puffling.version.scheme.standard import StandardScheme

if TYPE_CHECKING:
    from puffling.version.scheme.plugin.interface import VersionSchemeInterface


@hookimpl
def puffling_register_version_scheme() -> type[VersionSchemeInterface]:
    return StandardScheme
