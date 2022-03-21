from abc import ABC, abstractclassmethod
from typing import Union


# An abstract class for API functions, so that different logic may be implemented
class API(ABC):
    @abstractclassmethod
    def __init__(self, config_file_path: str) -> None:
        pass

    @abstractclassmethod
    def insertSingleImage(self, image_contents: Union[bytes, str], filename: str = "img.txt") -> bool:
        pass

    @abstractclassmethod
    def insertImagesInBatch(self, zip_contents: Union[bytes, str]) -> int:
        pass

    @abstractclassmethod
    def findTopKMatches(self, image_contents: Union[bytes, str]) -> dict:
        pass

    @abstractclassmethod
    def getFaceInfo(self, face_id:str) -> dict:
        pass