#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from pydantic import Field

from octodiary.types.model import DT, Type


class Info(Type):
    birthdate: Optional[DT] = None
    mail: Optional[str] = None
    gender: Optional[str] = None
    trusted: Optional[bool] = None
    first_name: str = Field(..., alias="FirstName")
    mobile: Optional[str] = None
    guid: Optional[str] = None
    failed: Optional[bool] = None
    last_name: str = Field(..., alias="LastName")
    error: Optional[Any] = None
    middle_name: str = Field(..., alias="MiddleName")
    snils: Optional[str] = None


class Subsystem(Type):
    id: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    mnemonic: Optional[str] = None
    description: Optional[str] = None
    is_mobile: Optional[bool] = None
    sort_order: Optional[int] = None


class Role(Type):
    id: int
    title: str
    subsystems: list[Subsystem]


class UserInfo(Type):
    user_id: Optional[int] = Field(None, alias="userId")
    is_ad_activated: Optional[bool] = Field(None, alias="isAdActivated")
    info: Optional[Info] = None
    roles: Optional[list[Role]] = None
    saved_choice: Optional[int] = Field(None, alias="savedChoice")
    notification: Optional[bool] = None
    login: Optional[str] = None
