from typing import List, Union

from pydantic import BaseModel


class DiapasonValidator(BaseModel):
    points: List[Union[float, int]]
