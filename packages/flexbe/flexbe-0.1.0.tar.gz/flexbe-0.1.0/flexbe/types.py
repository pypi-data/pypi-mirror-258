from enum import IntEnum
import typing as t


class LeadStatus(IntEnum):
    NEW = 0
    IN_WORK = 1
    DONE = 2
    CANCELLED = 10
    DELETED = 11

class _Status(t.TypedDict):
    code: LeadStatus
    name: str

class _Client(t.TypedDict):
    name: str
    phone: str
    email: str

class _Page(t.TypedDict):
    url: str
    name: str


class Lead(t.TypedDict):
    id: int
    num: int
    time: int
    status: _Status
    client: _Client
    note: str
    form_name: str
    form_data: dict[str, t.Any]
    page: _Page
    utm: dict[str, t.Any]
    pay: dict[str, t.Any] | None
    custom: str

