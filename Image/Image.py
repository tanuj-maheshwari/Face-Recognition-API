from abc import ABC, abstractclassmethod
from typing import Union


# An abstract Image class, which can be implemented to concreate implementations
# Eg, there might be multiple ways to get image metadata
class Image(ABC):
    @abstractclassmethod
    def __init__(self, image_contents: Union[bytes, str]) -> None:
        pass


    @abstractclassmethod
    def getMetadata(self, filename: str = "img.txt") -> dict:
        pass