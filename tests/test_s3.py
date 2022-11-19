from io import BytesIO
from wishl import constants
import os
endpoints = constants.endpoints['s3']

URL = 'https://s3.amazonaws.com/wishl-bucket/test8.jpg'


class TestUpload:
    data = {}

    def fake_send_to_s3(*argv):
        global function_called, function_args
        function_args = argv
        function_called = True
        return URL

    def test_file_not_provided(self, client, monkeypatch):

        self.data['file'] = (BytesIO(b"some file data"), 'test9.jpg')

        response = client.post(
            constants.endpoints['dev'] + endpoints['upload'])

        assert response.status_code == 400
        assert response.json['error'] == 'file is required'

    def test_call_send_to_s3_if_image_presented(self, client, monkeypatch):
        global function_called, function_args
        function_called = False

        monkeypatch.setattr('wishl.s3.send_to_s3',
                            self.fake_send_to_s3)

        response = client.post(
            constants.endpoints['dev'] + endpoints['upload'], data=self.data)

        assert response.status_code == 200
        assert function_called
        assert function_args[1].filename == 'test9.jpg'
        assert function_args[2] == os.environ.get('S3_BUCKET_NAME')

    def test_throw_error_if_image_not_presented(self, client, monkeypatch):
        self.data['file'] = (BytesIO(b"some file data"), 'test9.txt')

        response = client.post(
            constants.endpoints['dev'] + endpoints['upload'], data=self.data)

        assert response.status_code == 400
        assert response.json['error'] == 'file is not an image'


# return exception if any appears
# return exception if file is not presented
# secure filename
