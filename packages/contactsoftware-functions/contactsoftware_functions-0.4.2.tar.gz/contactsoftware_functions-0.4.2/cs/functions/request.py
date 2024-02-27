from cs.functions.event import Event
from cs.functions.metadata import MetaData
from pydantic import BaseModel, Field


class Request(BaseModel):
    metadata: MetaData = Field(..., description="General information.")
    event: Event
