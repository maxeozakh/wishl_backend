from flask import (
    Blueprint, request, jsonify
)
from wishl.db import get_db

bp = Blueprint('wishes', __name__)


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


@bp.route('/create', methods=['POST'])
def create():
    json = request.get_json()
    uid = json.get('uid')
    secrets = json.get('secrets')

    error = None
    if not uid:
        error = 'uid is required.'
    elif not secrets:
        error = 'secrets is required.'

    if error is not None:
        print("💥💥💥💥💥")
        print(error)
        print("💥💥💥💥💥")
        resp = jsonify(success=False)
        resp.error = error
        resp.status_code = 400
        return resp
    else:
        db = get_db()
        db.execute(
            'INSERT INTO wishlists (uid, secrets)'
            ' VALUES (?, ?)',
            (uid, secrets)
        )
        db.commit()
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp


@bp.route('/wishlists/<uid>', methods=['GET'])
def wishlists_get_by_uid_api(uid):
    wish = get_wishlist_by_uid(uid)
    return wish


def get_wishlist_by_uid(uid):
    error = None
    db = get_db()
    wishlist_data = db.execute(
        'SELECT uid, secrets'
        ' FROM wishlists w'
        ' WHERE uid = ?',
        (uid,)
    ).fetchone()

    if not wishlist_data:
        error = 'uid is not found.'
        response = {
            'success': False,
            'error': error
        }
        resp = jsonify(response)
        resp.status_code = 400
        return resp

    print(wishlist_data)
    return {
        "uid": wishlist_data["uid"],
        "secrets": wishlist_data["secrets"]
    }
