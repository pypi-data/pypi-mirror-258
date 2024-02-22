# coding: utf-8

"""
    FINBOURNE Scheduler API

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
from pydantic import BaseModel, Field
from lusid_scheduler.models.time_trigger import TimeTrigger

class Trigger(BaseModel):
    """
    Holds different kinds of triggers  A schedule may only have one type of trigger  # noqa: E501
    """
    time_trigger: Optional[TimeTrigger] = Field(None, alias="timeTrigger")
    __properties = ["timeTrigger"]

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
    def from_json(cls, json_str: str) -> Trigger:
        """Create an instance of Trigger from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of time_trigger
        if self.time_trigger:
            _dict['timeTrigger'] = self.time_trigger.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Trigger:
        """Create an instance of Trigger from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Trigger.parse_obj(obj)

        _obj = Trigger.parse_obj({
            "time_trigger": TimeTrigger.from_dict(obj.get("timeTrigger")) if obj.get("timeTrigger") is not None else None
        })
        return _obj
