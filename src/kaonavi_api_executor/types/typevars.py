from typing import TypeVar
from pydantic import BaseModel

TResponse = TypeVar("TResponse", bound=BaseModel)
