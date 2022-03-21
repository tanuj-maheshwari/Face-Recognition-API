from heapq import heapify, heappush, heappushpop, nsmallest
import io
import json
from multiprocessing import Pool
from typing import Union
import zipfile

from API.API import API
from Database.implementation.MySQLImageDatabase import MySQLImageDatabase
from Image.Encoder.implementation.AGTEncoder import AGTEncoder
from Image.implementation.AGTImage import AGTImage


# A concrete implementation of API class
class AGTAPI(API):
    def __init__(self, config_file_path: str) -> None:
        # Setup image database
        config_file = open("config.json")
        config_str = config_file.read()
        db_config = json.loads(config_str)
        self.db = MySQLImageDatabase(db_config)

        # Setup image encoder
        self.encoder = AGTEncoder()
    
    def insertSingleImage(self, image_contents: Union[bytes, str], filename: str = "img.txt") -> bool:
        # Get image encodings and convert to pickle of array as a string
        image = AGTImage(image_contents)

        # Convert image to string pickle
        stringPickle = self.encoder.getStringPickle(image)

        if(stringPickle == "\0"):
            return False

        # Get image metadata
        image_metadata = image.getMetadata(filename)
        
        # Insert in database
        self.db.insertImageWithMetadata(stringPickle, image_metadata)
        
        return True

    
    def insertImagesInBatch(self, zip_contents: Union[bytes, str]) -> int:
        # Unzip the file and add individual images to an array
        filebytes = io.BytesIO(zip_contents)
        zipfiles = zipfile.ZipFile(filebytes)
        images = []
        metadata = []
        temp = []
        for filename in zipfiles.namelist():
            file = zipfiles.open(filename)
            file_contents = file.read()
            temp.append(file_contents)
            images.append(AGTImage(file_contents))
            metadata.append(AGTImage(file_contents).getMetadata(filename))

        # Create a process pool and divide the array for each processes
        pickles = []
        with Pool(8) as process_pool:
            pickles = process_pool.map(self.encoder.getStringPickle, images)

        # Insert the images in database
        num_images_inserted = 0
        for i in range(len(pickles)):
            if pickles[i] != "\0":
                self.db.insertImageWithMetadata(pickles[i], metadata[i])
                num_images_inserted = num_images_inserted + 1

        return num_images_inserted

    
    def findTopKMatches(self, image_contents: Union[bytes, str], k: int, tolerance: float) -> dict:
        # Get image encodings
        image = AGTImage(image_contents)
        image_encodings_all = self.encoder.getImageEncodings(image)

        # Get all image encodings from database
        database_results_all = self.db.retrieveAllImages()

        # Repeat for all faces in image
        i = 1
        result = {}
        for image_encoding in image_encodings_all:
            parameter_list = []
            for database_result in database_results_all:
                parameter_list.append((image_encoding, database_result))

            # Get face distance values in a pool of processes
            face_distances_all = []
            with Pool(8) as process_pool:
                face_distances_all = process_pool.map(self.encoder.getFaceDistances, parameter_list)

            # Remove all faces with distance more than tolerance
            face_distances_all = [face for face in face_distances_all if not face[0] > tolerance]
            
            # Build the result for this face
            face_result = []            
            if len(face_distances_all) > k:
                face_result = [{"id":face[2], "person_name": face[1]} for face in nsmallest(k, face_distances_all)]
            else:
                face_distances_all = sorted(face_distances_all)
                face_result = [{"id":face[2], "person_name": face[1]} for face in face_distances_all]

            # Append to final result
            result[f'face{i}'] = str(face_result)
            i = i + 1

        return result

    def getFaceInfo(self, face_id_str: str) -> Union[dict, str]:
        # Convert face_id to int
        face_id = int(face_id_str)

        # Retrive the image information from database
        database_result = self.db.retriveImageInfo(face_id)
        if database_result is None:
            return "No such face id in database"
        
        # Create the result dictionary
        result = {}
        result['id'] = str(database_result[0])
        result['person_name'] = str(database_result[1])
        result['version'] = str(database_result[2])
        result['date and time'] = str(database_result[3])
        result['location'] = str(database_result[4])
        
        return result