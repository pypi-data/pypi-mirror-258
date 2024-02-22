# coding: utf-8

"""
    FINBOURNE Notifications API

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
from pydantic import BaseModel, Field, constr, validator
from lusid_notifications.models.notification_type import NotificationType

class UpdateNotificationRequest(BaseModel):
    """
    The information required to update a notification  # noqa: E501
    """
    display_name: constr(strict=True, max_length=64, min_length=0) = Field(..., alias="displayName", description="The name of the notification")
    description: Optional[constr(strict=True, max_length=512, min_length=1)] = Field(None, description="The summary of the services provided by the notification")
    notification_type: NotificationType = Field(..., alias="notificationType")
    __properties = ["displayName", "description", "notificationType"]

    @validator('display_name')
    def display_name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('description')
    def description_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

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
    def from_json(cls, json_str: str) -> UpdateNotificationRequest:
        """Create an instance of UpdateNotificationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of notification_type
        if self.notification_type:
            _dict['notificationType'] = self.notification_type.to_dict()
        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateNotificationRequest:
        """Create an instance of UpdateNotificationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateNotificationRequest.parse_obj(obj)

        _obj = UpdateNotificationRequest.parse_obj({
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "notification_type": NotificationType.from_dict(obj.get("notificationType")) if obj.get("notificationType") is not None else None
        })
        return _obj
