from flask import (
    Blueprint, request, jsonify
)
from wishl.db import get_db
from wishl import constants

bp = Blueprint('wishes', __name__)
endpoints = constants.endpoints['wishlists']


@bp.route('/')
def index():
    db = get_db()
    wishlists = db.execute(
        'SELECT uid, secrets'
        ' FROM wishlists w'
        ' ORDER BY id ASC'
    ).fetchall()

    wishlists_data = []
    for wish in wishlists:
        wishlists_data.append({
            'uid': wish['uid'],
            'secrets': wish['secrets']

        })

    return jsonify(
        wishlists=wishlists_data,
    )


@bp.route(endpoints["create"], methods=['POST'])
def create():
    json = request.get_json()
    uid = json.get('uid')
    secrets = json.get('secrets')

    error = None
    if not uid:
        error = 'uid is required.'
    elif not secrets:
        error = 'secrets is required.'
    elif not json:
        error = 'json is empty.'

    if error is not None:
        response_body = {
            'success': False,
            'error': error
        }
        response = jsonify(response_body)
        response.status_code = 400
        return response

    else:
        db = get_db()
        db.execute(
            'INSERT INTO wishlists (uid, secrets)'
            ' VALUES (?, ?)',
            (uid, secrets)
        )
        db.commit()
        response = jsonify(success=True)
        response.status_code = 200
        return response


@bp.route(endpoints["get_by_uid"] + '<uid>', methods=['GET'])
def wishlists_get_by_uid_api(uid):
    wish = get_wishlist_by_uid(uid)
    return wish


def get_wishlist_by_uid(uid):
    db = get_db()
    wishlist_data = db.execute(
        'SELECT uid, secrets'
        ' FROM wishlists w'
        ' WHERE uid = ?',
        (uid,)
    ).fetchone()

    if not wishlist_data:
        response_body = {
            'success': False,
            'error': 'wishlist by uid is not found.'
        }
        response = jsonify(response_body)
        response.status_code = 400
        return response

    return {
        "uid": wishlist_data["uid"],
        "secrets": wishlist_data["secrets"]
    }
