from io import BytesIO
from wishl import constants
endpoints = constants.endpoints['s3']


def test_upload(client, monkeypatch):
    data = {}
    data['file'] = (BytesIO(b"some file data"), 'test9.jpg')

    response = client.post(
        constants.endpoints['dev'] + endpoints['upload'])

    assert response.status_code == 400
    assert response.json['error'] == 'file is required'

    """upload to s3 with image"""
    URL = 'https://s3.amazonaws.com/wishl-bucket/test8.jpg'
    global function_called
    function_called = False

    def fake_send_to_s3(file, bucket_name):
        global function_called
        function_called = True
        return URL

    monkeypatch.setattr('wishl.s3.send_to_s3',
                        fake_send_to_s3)

    response = client.post(
        constants.endpoints['dev'] + endpoints['upload'], data=data)

    assert response.status_code == 200
    assert response.json['url'] == URL
    assert function_called

# call s3.upload_fileobj with correct arguments
# return json with s3 bucket location and filename
# return exception if any appears


# test_upload()

# return exception if file is not presented
# secure filename
# call send_to_s3 with correct arguments
