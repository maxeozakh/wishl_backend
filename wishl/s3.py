from flask import (
    Blueprint, g, redirect, request, url_for, Response, jsonify, json
)
from wishl.db import get_db
import os
import boto3, botocore
from werkzeug.utils import secure_filename
from flask_cors import cross_origin

bp = Blueprint('s3', __name__, url_prefix='/s3')
s3 = boto3.client('s3', aws_access_key_id=os.environ.get('S3_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET'))

S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
S3_LOCATION = os.environ.get('S3_LOCATION')

@bp.route('/get_sign', methods=(['GET']))
def get_info():
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': ['ETag', 'x-amz-request-id'],
            'MaxAgeSeconds': 3000
        }]
    }   

    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('S3_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET'))
    s3.put_bucket_cors(Bucket = S3_BUCKET, CORSConfiguration=cors_configuration)


    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })


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
                    "ContentType": file.content_type    #Set appropriate content type as per the file
                }
            )
        except Exception as e:
            print("Something Happened: ", e)
            return e
        return "{}{}".format(S3_LOCATION, file.filename)

@bp.route('/upload', methods=(['POST']))
@cross_origin()
def upload():
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    file = request.files['file']

    if file.filename == "":
        return "Please select a file"
    if file:
        file.filename = secure_filename(file.filename)
        output = send_to_s3(file, S3_BUCKET_NAME)
        return jsonify({"url": output})

    