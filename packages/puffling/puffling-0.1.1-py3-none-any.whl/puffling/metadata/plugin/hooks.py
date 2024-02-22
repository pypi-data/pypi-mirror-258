from __future__ import annotations

from typing import TYPE_CHECKING

from puffling.metadata.custom import CustomMetadataHook
from puffling.plugin import hookimpl

if TYPE_CHECKING:
    from puffling.metadata.plugin.interface import MetadataHookInterface


@hookimpl
def puffling_register_metadata_hook() -> type[MetadataHookInterface]:
    return CustomMetadataHook  # type: ignore
