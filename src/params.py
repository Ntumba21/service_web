from pydantic import BaseModel
from typing import List

class TradParams(BaseModel):
    word: str
    dictionnary: str

class DictionnaryLineParams(BaseModel):
    letter: str
    trad: str

class DictionnaryParams(BaseModel):
    name: str
    lines: List[DictionnaryLineParams] = []
