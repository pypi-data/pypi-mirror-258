import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.whois_response_200_usage import WhoisResponse200Usage


T = TypeVar("T", bound="WhoisResponse200")


@_attrs_define
class WhoisResponse200:
    """
    Attributes:
        email (str):
        username (str):
        is_admin (bool):
        is_super_admin (bool):
        created_at (datetime.datetime):
        operator (bool):
        disabled (bool):
        folders (List[str]):
        folders_owners (List[str]):
        groups (Union[Unset, List[str]]):
        usage (Union[Unset, WhoisResponse200Usage]):
    """

    email: str
    username: str
    is_admin: bool
    is_super_admin: bool
    created_at: datetime.datetime
    operator: bool
    disabled: bool
    folders: List[str]
    folders_owners: List[str]
    groups: Union[Unset, List[str]] = UNSET
    usage: Union[Unset, "WhoisResponse200Usage"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        username = self.username
        is_admin = self.is_admin
        is_super_admin = self.is_super_admin
        created_at = self.created_at.isoformat()

        operator = self.operator
        disabled = self.disabled
        folders = self.folders

        folders_owners = self.folders_owners

        groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        usage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "username": username,
                "is_admin": is_admin,
                "is_super_admin": is_super_admin,
                "created_at": created_at,
                "operator": operator,
                "disabled": disabled,
                "folders": folders,
                "folders_owners": folders_owners,
            }
        )
        if groups is not UNSET:
            field_dict["groups"] = groups
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.whois_response_200_usage import WhoisResponse200Usage

        d = src_dict.copy()
        email = d.pop("email")

        username = d.pop("username")

        is_admin = d.pop("is_admin")

        is_super_admin = d.pop("is_super_admin")

        created_at = isoparse(d.pop("created_at"))

        operator = d.pop("operator")

        disabled = d.pop("disabled")

        folders = cast(List[str], d.pop("folders"))

        folders_owners = cast(List[str], d.pop("folders_owners"))

        groups = cast(List[str], d.pop("groups", UNSET))

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, WhoisResponse200Usage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = WhoisResponse200Usage.from_dict(_usage)

        whois_response_200 = cls(
            email=email,
            username=username,
            is_admin=is_admin,
            is_super_admin=is_super_admin,
            created_at=created_at,
            operator=operator,
            disabled=disabled,
            folders=folders,
            folders_owners=folders_owners,
            groups=groups,
            usage=usage,
        )

        whois_response_200.additional_properties = d
        return whois_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
