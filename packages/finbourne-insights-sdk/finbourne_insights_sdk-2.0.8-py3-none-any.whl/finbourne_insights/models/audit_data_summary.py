# coding: utf-8

"""
    FINBOURNE Insights API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, Optional
from pydantic import BaseModel, StrictInt

class AuditDataSummary(BaseModel):
    """
    AuditDataSummary
    """
    count: Optional[StrictInt] = None
    categories: Optional[Dict[str, StrictInt]] = None
    __properties = ["count", "categories"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AuditDataSummary:
        """Create an instance of AuditDataSummary from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "count",
                          },
                          exclude_none=True)
        # set to None if categories (nullable) is None
        # and __fields_set__ contains the field
        if self.categories is None and "categories" in self.__fields_set__:
            _dict['categories'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AuditDataSummary:
        """Create an instance of AuditDataSummary from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AuditDataSummary.parse_obj(obj)

        _obj = AuditDataSummary.parse_obj({
            "count": obj.get("count"),
            "categories": obj.get("categories")
        })
        return _obj
