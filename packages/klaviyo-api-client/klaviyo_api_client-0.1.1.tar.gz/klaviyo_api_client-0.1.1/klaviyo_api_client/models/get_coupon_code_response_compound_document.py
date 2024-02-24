from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.coupon_response_object_resource import CouponResponseObjectResource
    from ..models.get_coupon_code_response_compound_document_data import GetCouponCodeResponseCompoundDocumentData


T = TypeVar("T", bound="GetCouponCodeResponseCompoundDocument")


@_attrs_define
class GetCouponCodeResponseCompoundDocument:
    """
    Attributes:
        data (GetCouponCodeResponseCompoundDocumentData):
        included (Union[Unset, List['CouponResponseObjectResource']]):
    """

    data: "GetCouponCodeResponseCompoundDocumentData"
    included: Union[Unset, List["CouponResponseObjectResource"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        included: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.included, Unset):
            included = []
            for included_item_data in self.included:
                included_item = included_item_data.to_dict()
                included.append(included_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if included is not UNSET:
            field_dict["included"] = included

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.coupon_response_object_resource import CouponResponseObjectResource
        from ..models.get_coupon_code_response_compound_document_data import GetCouponCodeResponseCompoundDocumentData

        d = src_dict.copy()
        data = GetCouponCodeResponseCompoundDocumentData.from_dict(d.pop("data"))

        included = []
        _included = d.pop("included", UNSET)
        for included_item_data in _included or []:
            included_item = CouponResponseObjectResource.from_dict(included_item_data)

            included.append(included_item)

        get_coupon_code_response_compound_document = cls(
            data=data,
            included=included,
        )

        get_coupon_code_response_compound_document.additional_properties = d
        return get_coupon_code_response_compound_document

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
