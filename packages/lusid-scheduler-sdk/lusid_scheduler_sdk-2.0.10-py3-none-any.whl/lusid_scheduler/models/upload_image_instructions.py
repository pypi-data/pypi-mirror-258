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

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictStr, constr

class UploadImageInstructions(BaseModel):
    """
      # noqa: E501
    """
    docker_login_command: constr(strict=True, min_length=1) = Field(..., alias="dockerLoginCommand")
    build_versioned_docker_image_command: constr(strict=True, min_length=1) = Field(..., alias="buildVersionedDockerImageCommand")
    tag_versioned_docker_image_command: constr(strict=True, min_length=1) = Field(..., alias="tagVersionedDockerImageCommand")
    push_versioned_docker_image_command: constr(strict=True, min_length=1) = Field(..., alias="pushVersionedDockerImageCommand")
    tag_latest_docker_image_command: Optional[StrictStr] = Field(None, alias="tagLatestDockerImageCommand")
    push_latest_docker_image_command: Optional[StrictStr] = Field(None, alias="pushLatestDockerImageCommand")
    expiry_time: Optional[datetime] = Field(None, alias="expiryTime")
    __properties = ["dockerLoginCommand", "buildVersionedDockerImageCommand", "tagVersionedDockerImageCommand", "pushVersionedDockerImageCommand", "tagLatestDockerImageCommand", "pushLatestDockerImageCommand", "expiryTime"]

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
    def from_json(cls, json_str: str) -> UploadImageInstructions:
        """Create an instance of UploadImageInstructions from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if tag_latest_docker_image_command (nullable) is None
        # and __fields_set__ contains the field
        if self.tag_latest_docker_image_command is None and "tag_latest_docker_image_command" in self.__fields_set__:
            _dict['tagLatestDockerImageCommand'] = None

        # set to None if push_latest_docker_image_command (nullable) is None
        # and __fields_set__ contains the field
        if self.push_latest_docker_image_command is None and "push_latest_docker_image_command" in self.__fields_set__:
            _dict['pushLatestDockerImageCommand'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UploadImageInstructions:
        """Create an instance of UploadImageInstructions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UploadImageInstructions.parse_obj(obj)

        _obj = UploadImageInstructions.parse_obj({
            "docker_login_command": obj.get("dockerLoginCommand"),
            "build_versioned_docker_image_command": obj.get("buildVersionedDockerImageCommand"),
            "tag_versioned_docker_image_command": obj.get("tagVersionedDockerImageCommand"),
            "push_versioned_docker_image_command": obj.get("pushVersionedDockerImageCommand"),
            "tag_latest_docker_image_command": obj.get("tagLatestDockerImageCommand"),
            "push_latest_docker_image_command": obj.get("pushLatestDockerImageCommand"),
            "expiry_time": obj.get("expiryTime")
        })
        return _obj
