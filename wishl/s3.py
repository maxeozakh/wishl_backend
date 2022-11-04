from wishl import constants
from flask import (
    Blueprint, request, jsonify
)
import os
import boto3
from werkzeug.utils import secure_filename
from flask_cors import cross_origin

endpoints = constants.endpoints['s3']

bp = Blueprint('s3', __name__)
s3 = boto3.client('s3', aws_access_key_id=os.environ.get(
    'S3_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET'))

S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
S3_LOCATION = os.environ.get('S3_LOCATION')


def send_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
                # Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(S3_LOCATION, file.filename)


@bp.route(endpoints['upload'], methods=(['POST']))
@cross_origin()
def upload():
    # return jsonify(something=1)
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    file = request.files and request.files['file']

    if not file:
        response_body = {
            'success': False,
            'error': 'file is required'
        }
        response = jsonify(response_body)
        response.status_code = 400
        return response
    if file:
        file.filename = secure_filename(file.filename)
        output = send_to_s3(file, S3_BUCKET_NAME)
        return jsonify({"url": output})
