from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify
)
from wishl.db import get_db

bp = Blueprint('wishes', __name__)
@bp.route('/')
def index():
    db = get_db()
    wishes = db.execute(
        'SELECT uid, secrets'
        ' FROM wishes w'
        ' ORDER BY id ASC'
    ).fetchall()

    wishes_data = []
    for wish in wishes:
        wishes_data.append({
            'uid': wish['uid'],
            'secrets': wish['secrets']
            
        })
    return jsonify(
        wishes=wishes_data,
    )

from flask import jsonify
from flask_cors import cross_origin

@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
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
                'INSERT INTO wishes (uid, secrets)'
                ' VALUES (?, ?)',
                (uid, secrets)
            )
            db.commit()
            resp = jsonify(success=True)
            resp.status_code = 200
            return resp


@bp.route('/wishes/<uid>', methods=['GET'])
def get_wishlist_by_uid(uid):
    error = None
    db = get_db()
    wish_list_data = db.execute(
        'SELECT uid, secrets'
        ' FROM wishes w'
        ' WHERE uid = ?',
        (uid,)
    ).fetchone()
    
    if not wish_list_data:
        error = 'uid is not found.'
        response = {
            'success': False,
            'error': error
        }
        resp = jsonify(response)
        resp.status_code = 400
        return resp

    wishes_data = {}
    wishes_data['uid'] = wish_list_data['uid']
    wishes_data['secrets'] = wish_list_data['secrets']

    return jsonify(
        wishes_data,
    )