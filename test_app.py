import json
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_add_faces_in_bulk():
    url = "http://127.0.0.1:8000/add_faces_in_bulk/"
    files = {'file': open("./test_images/AmericanPresidents.zip", 'rb')}
    res = client.post(url, files=files)
    # files = {'file': open("./test_images/lfw.zip", 'rb')}
    # res = client.post(url, files=files)
    assert str(res.json()).replace("\'", "\"") == json.dumps({"status": "OK", "body": "Inserted 2 images in database."}).replace("\'", "\"")
    # assert str(res.json()).replace("\'", "\"") == json.dumps({"status": "OK", "body": "Inserted 13176 images in database."}).replace("\'", "\"")


def test_add_face():
    url = "http://127.0.0.1:8000/add_face/"
    files = {'file': open("./test_images/Donald_Trump_official_portrait.jpg", 'rb')}
    res = client.post(url, files=files)
    assert str(res.json()).replace("\'", "\"") == json.dumps({"status": "OK", "body": "Successfully inserted the image in database."}).replace("\'", "\"")


def test_get_face_info():
    url = "http://127.0.0.1:8000/get_face_info/"
    form_data = {"api_key": "key", "face_id": "1"}
    res = client.post(url, data=form_data)
    assert str(res.json()).replace("\'", "\"") == json.dumps({'status': 'OK', 'body': {'id': '1', 'person_name': 'Donald Trump', 'version': "b'0220'", 'date and time': '2017:10:19 07:50:26', 'location': 'Not Defined'}}).replace("\'", "\"")


def test_search_faces():
    url = "http://127.0.0.1:8000/search_faces/?k=5&tolerance=0.6"
    files = {'file': open("./test_images/Joe_Biden_presidential_portrait.jpg", 'rb')}
    # files = {'file': open("./test_images/GongLi.jpg", 'rb')}
    res = client.post(url, files=files)
    assert "Joe Biden" in str(res.json())
    # assert "Gong Li" in str(res.json())