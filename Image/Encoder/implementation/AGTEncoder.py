import io
import pickle
import face_recognition
from numpy import ndarray

from Image.Encoder.ImageEncoder import ImageEncoder
from Image.Image import Image


# A concrete implementation of ImageEncoder, which encodes the image using ageitgey's face_ecnodings API
class AGTEncoder(ImageEncoder):
    def getImageEncodings(self, image: Image) -> list:
        loaded_image = face_recognition.load_image_file(io.BytesIO(image.image_contents))
        return face_recognition.face_encodings(loaded_image)

    def getStringPickle(self, image: Image):
        encodings = self.getImageEncodings(image)
        if len(encodings) == 0:
            return "\0"
        return ndarray.dumps(encodings[0])
    
    def getFaceDistances(self, param: tuple) -> tuple:
        image_encodings = param[0]
        database_result = param[1]
        known_encodings = pickle.loads(database_result[0])
        distance = face_recognition.face_distance([known_encodings], image_encodings)
        return (distance, database_result[1], database_result[2])