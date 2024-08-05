import pytest, os
from borgweb.testsuite import app, client

# def test_import_repo(client):
#     response = client.post("/repos/import", data={
#         "name": "FlaskImported",
#         "location": "/temp/flask",
#         "description": "A micro web framework for Python"
#     })
#     assert response.status_code == 200

def test_create_repo_no_encrytion(client):
    response = client.post("/repos/create", data={
        "name": "FlaskCreated",
        "location": "/tmp/flask",
        "encryption": "none",
        "description": "A micro web framework for Python"
    })
    
    assert response.status_code == 200