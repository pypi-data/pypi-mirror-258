from typing import Annotated, Union

from pydantic import Field

from .classification import ObjectPropertyValue
from .document import CADDocument, Document
from .engineering_change import EngineeringChange
from .file import File
from .part import BOMItem, Material, Part

Object = Annotated[
    Union[Document, CADDocument, Part, File, EngineeringChange, Material, BOMItem, ObjectPropertyValue],
    Field(discriminator="object_type"),
]
