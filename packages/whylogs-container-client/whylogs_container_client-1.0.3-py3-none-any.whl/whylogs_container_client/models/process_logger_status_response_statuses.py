from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.logger_status_response import LoggerStatusResponse


T = TypeVar("T", bound="ProcessLoggerStatusResponseStatuses")


@_attrs_define
class ProcessLoggerStatusResponseStatuses:
    """ """

    additional_properties: Dict[str, "LoggerStatusResponse"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.logger_status_response import LoggerStatusResponse

        d = src_dict.copy()
        process_logger_status_response_statuses = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = LoggerStatusResponse.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        process_logger_status_response_statuses.additional_properties = additional_properties
        return process_logger_status_response_statuses

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "LoggerStatusResponse":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "LoggerStatusResponse") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
