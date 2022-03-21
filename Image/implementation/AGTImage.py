import datetime
import io
from typing import Union
from Image.Image import Image
from PIL import Image as PILImage
from PIL.ExifTags import TAGS


# An implementation of Image Abstract class
class AGTImage(Image):
    def __init__(self, image_contents: Union[bytes, str]) -> None:
        self.image_contents = image_contents
        

    def getMetadata(self, filename: str = "img.txt") -> dict:
        # Open image as PIL image
        pil_image = PILImage.open(io.BytesIO(self.image_contents))
        
        # Extract metadata from image
        metadata = {}
        exifdata = pil_image.getexif()
        for tagid in exifdata:
            tagname = TAGS.get(tagid)
            value = exifdata.get(tagid)
            metadata[tagname] = value
        
        # Add necessary fields to metadata
        if "Name" not in metadata:
            name = filename.split(".")[0].replace("_", " ")
            if " " in name:
                name = name.split(" ")[0] + " " + name.split(" ")[1]
            metadata["Name"] = name
        metadata["Name"] = str(metadata["Name"])
        if "Version" not in metadata:
            metadata["Version"] = str(b'0220')
        metadata["Version"] = str(metadata["Version"])
        if "DateTime" not in metadata:
            metadata["DateTime"] = datetime.datetime.now().strftime("%c")
        metadata["DateTime"] = str(metadata["DateTime"])
        if "Location" not in metadata:
            metadata["Location"] = "Not Defined"
        metadata["Location"] = str(metadata["Location"])

        return metadata