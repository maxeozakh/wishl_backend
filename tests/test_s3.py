from io import BytesIO
from wishl import constants
import os
endpoints = constants.endpoints['s3']

URL = 'https://s3.amazonaws.com/wishl-bucket/test8.jpg'


def fake_send_to_s3(*argv):
    global function_called, function_args
    function_args = argv
    function_called = True
    return URL


def test_upload(client, monkeypatch):
    """"rise an error if file is not provided"""
    data = {}
    data['file'] = (BytesIO(b"some file data"), 'test9.jpg')

    response = client.post(
        constants.endpoints['dev'] + endpoints['upload'])

    assert response.status_code == 400
    assert response.json['error'] == 'file is required'

    """call send_to_s3 function with correct args if image is presented"""
    global function_called, function_args
    function_called = False

    monkeypatch.setattr('wishl.s3.send_to_s3',
                        fake_send_to_s3)

    response = client.post(
        constants.endpoints['dev'] + endpoints['upload'], data=data)

    assert response.status_code == 200
    assert function_called
    assert function_args[0].filename == 'test9.jpg'
    assert function_args[1] == os.environ.get('S3_BUCKET_NAME')

    """return error if file is not an image"""
    data['file'] = (BytesIO(b"some file data"), 'test9.txt')

    response = client.post(
        constants.endpoints['dev'] + endpoints['upload'], data=data)

    assert response.status_code == 400
    assert response.json['error'] == 'file is not an image'


# return exception if any appears
# return exception if file is not presented
# secure filename
