from abc import ABC, abstractclassmethod


# An abstract class for image related operations on Database
# The methods accept generic Image objects (not specific implemntations of Image abstract class)
# This abstract class can be implemented to create concrete image database implementations
class ImageDatabase(ABC):
    @abstractclassmethod
    def insertImageWithMetadata(self, imageStringPickle, image_metadata: dict) -> None:
        pass

    @abstractclassmethod
    def retrieveAllImages(self) -> list:
        pass

    @abstractclassmethod
    def retriveImageInfo(self, image_id: int) -> dict:
        pass