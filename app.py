from fastapi import FastAPI, File, Form, UploadFile
from API.implementation.AGTAPI import AGTAPI


app = FastAPI()


@app.post("/search_faces/")
async def search_faces(k: int = 1, tolerance: float = 0.6, file: UploadFile = File(..., description="An image file, possible containing multiple human faces.")):
    image_contents = await file.read()
    matches = api.findTopKMatches(image_contents, k, tolerance)

    return {"status": "OK", "body": {"matches": matches}}


@app.post("/add_face/")
async def add_face(file: UploadFile = File(..., description="An image file having a single human face.")):
    image_contents = await file.read()
    insertion = api.insertSingleImage(image_contents, file.filename)

    if insertion is True:
        return {"status": "OK", "body": "Successfully inserted the image in database."}
    else:
        return {"status": "ERROR", "body": "Image doesn't contain a face in database."}


@app.post("/add_faces_in_bulk/")
async def add_faces_in_bulk(file: UploadFile = File(..., description="A ZIP file containing multiple face images.")):
    zip_contents = await file.read()
    num_images_inserted = api.insertImagesInBatch(zip_contents)
    
    return {"status": "OK", "body": f"Inserted {num_images_inserted} images in database."}


@app.post("/get_face_info/")
async def get_face_info(api_key: str = Form(...), face_id: str = Form(...)):
    metadata = api.getFaceInfo(face_id)

    if type(metadata) == dict:
        return {"status": "OK", "body": metadata}
    else:
        return {"status": "ERROR", "body": metadata}


api = AGTAPI("config.json")