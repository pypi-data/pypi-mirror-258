""" " A basic SIMOS Attribute"""
from __future__ import annotations
from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .blueprint import Blueprint

class BlueprintAttribute:
    """ " A basic SIMOS Attribute"""

    def __init__(self, content: Dict, parent_blueprint: Blueprint) -> None:
        self.content = content
        if "description" not in content:
            content["description"] = ""
        name = content["name"]
        if not name:
            raise ValueError("Attribute has no name")
        self.name = name
        self.description = content["description"].replace('"',"'")
        self.__is_many= "dimensions" in content
        self.__contained = content.get("contained",True)
        atype = content["attributeType"]

        package = parent_blueprint.parent
        self.__type = package.resolve_type(atype)
        primitive_types =  ['boolean', 'number', 'string', 'integer']
        self.__is_primitive = atype in primitive_types
        self.is_enum = self.content.get("enumType",None) is not None

    @property
    def name(self) -> str:
        """Entity id"""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Set name"""
        self.__name = str(value)

    @property
    def type(self) -> str:
        """Attribute type"""
        return self.__type

    @property
    def description(self) -> str:
        """Entity id"""
        return self.__description

    @property
    def contained(self) -> bool:
        """Is contained"""
        return self.__contained

    @property
    def is_primitive(self) -> bool:
        """Is this a primitive attribute"""
        return self.__is_primitive

    @property
    def is_many(self) -> bool:
        """Is this a many relation"""
        return self.__is_many

    @property
    def optional(self) -> bool:
        """Is this a many relation"""
        return self.content.get("optional",True)

    @description.setter
    def description(self, value: str):
        """Set description"""
        self.__description = str(value)

    def get(self, key, default=None):
        """Return the content value or an optional default"""
        return self.content.get(key,default)

    def as_dict(self) -> Dict:
        """Return the attribute as a dictionary"""
        return dict(self.content)
