from abc import ABC, abstractclassmethod

from Image.Image import Image


# An abstract Image Encoder class, which encodes image
# Concrete implementations can be made according to different encodings
class ImageEncoder(ABC):
    @abstractclassmethod
    def getImageEncodings(self, image: Image) -> list:
        pass

    @abstractclassmethod
    def getStringPickle(self, image: Image):
        pass