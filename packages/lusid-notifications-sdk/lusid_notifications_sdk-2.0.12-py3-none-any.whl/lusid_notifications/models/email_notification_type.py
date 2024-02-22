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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, constr, validator

class EmailNotificationType(BaseModel):
    """
    The information required to create or update an Email notification  # noqa: E501
    """
    type: constr(strict=True, min_length=1) = Field(..., description="The type of delivery mechanism for this notification")
    subject: constr(strict=True, max_length=1024, min_length=1) = Field(..., description="The subject of the email")
    plain_text_body: constr(strict=True, max_length=2147483647, min_length=1) = Field(..., alias="plainTextBody", description="The plain text body of the email")
    html_body: Optional[constr(strict=True)] = Field(None, alias="htmlBody", description="The HTML body of the email (if any)")
    email_address_to: conlist(StrictStr, max_items=10, min_items=1) = Field(..., alias="emailAddressTo", description="'To' recipients of the email")
    email_address_cc: Optional[conlist(StrictStr, max_items=10, min_items=0)] = Field(None, alias="emailAddressCc", description="'Cc' recipients of the email")
    email_address_bcc: Optional[conlist(StrictStr, max_items=10, min_items=0)] = Field(None, alias="emailAddressBcc", description="'Bcc' recipients of the email")
    __properties = ["type", "subject", "plainTextBody", "htmlBody", "emailAddressTo", "emailAddressCc", "emailAddressBcc"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Email'):
            raise ValueError("must be one of enum values ('Email')")
        return value

    @validator('subject')
    def subject_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('plain_text_body')
    def plain_text_body_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('html_body')
    def html_body_validate_regular_expression(cls, value):
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
    def from_json(cls, json_str: str) -> EmailNotificationType:
        """Create an instance of EmailNotificationType from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if html_body (nullable) is None
        # and __fields_set__ contains the field
        if self.html_body is None and "html_body" in self.__fields_set__:
            _dict['htmlBody'] = None

        # set to None if email_address_cc (nullable) is None
        # and __fields_set__ contains the field
        if self.email_address_cc is None and "email_address_cc" in self.__fields_set__:
            _dict['emailAddressCc'] = None

        # set to None if email_address_bcc (nullable) is None
        # and __fields_set__ contains the field
        if self.email_address_bcc is None and "email_address_bcc" in self.__fields_set__:
            _dict['emailAddressBcc'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> EmailNotificationType:
        """Create an instance of EmailNotificationType from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return EmailNotificationType.parse_obj(obj)

        _obj = EmailNotificationType.parse_obj({
            "type": obj.get("type"),
            "subject": obj.get("subject"),
            "plain_text_body": obj.get("plainTextBody"),
            "html_body": obj.get("htmlBody"),
            "email_address_to": obj.get("emailAddressTo"),
            "email_address_cc": obj.get("emailAddressCc"),
            "email_address_bcc": obj.get("emailAddressBcc")
        })
        return _obj
