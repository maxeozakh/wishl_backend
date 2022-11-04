# test_send_to_s3()
from io import BytesIO
from wishl import constants
endpoints = constants.endpoints['s3']


def test_upload(client):
    response = client.post(endpoints['upload'], files={
        'file': (BytesIO(b"some initial binary data: \x00\x01"),
                 'test.jpg')
    })

    assert response == 1


# call s3.upload_fileobj with correct arguments
# return json with s3 bucket location and filename
# return exception if any appears


# test_upload()

# return exception if file is not presented
# secure filename
# call send_to_s3 with correct arguments
