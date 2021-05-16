# 3rd party modules.
import requests


def test_read_all():
    response = requests.get("http://0.0.0.0:5000/api/users")
    assert response.status_code == 200


def test_create():
    params = {"postalcode": "48012", "username": "Jone"}
    response = requests.post("http://0.0.0.0:5000/api/users", json=params,)
    assert response.status_code == 201


def test_read_one():
    response = requests.get("http://0.0.0.0:5000/api/users/Jone")
    assert response.status_code == 200


def test_read_one_details():
    response = requests.get("http://0.0.0.0:5000/api/users/details/Jone")
    assert response.json()["cityname"] == "Bilbao"


def test_delete():
    response = requests.delete("http://0.0.0.0:5000/api/users/Jone")
    assert response.status_code == 200
