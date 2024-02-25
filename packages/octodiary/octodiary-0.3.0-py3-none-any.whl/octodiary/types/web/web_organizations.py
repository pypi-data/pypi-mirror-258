#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from pydantic import Field

from octodiary.types.model import DT, Type


class ConstituentEntityItem(Type):
    key: str


class Entity(Type):
    signature_date: Optional[DT] = None
    global_id: Optional[int] = None
    system_object_id: Optional[str] = None
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    constituent_entity: list[ConstituentEntityItem]


class WebOrganizations(Type):
    page: Optional[int] = None
    size: Optional[int] = None
    total_size: Optional[int] = Field(None, alias="totalSize")
    parent_categories: Optional[Any] = Field(None, alias="parentCategories")
    entities: Optional[list[Entity]] = None
