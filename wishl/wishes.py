from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort

from wishl.auth import login_required
from wishl.db import get_db

bp = Blueprint('wishes', __name__)


from flask import jsonify
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
    print(wishes_data)
    return jsonify(
        wishes=wishes_data,
    )

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
            return error
        else:
            db = get_db()
            db.execute(
                'INSERT INTO wishes (uid, secrets)'
                ' VALUES (?, ?)',
                (uid, secrets)
            )
            db.commit()
            return Response(status=200)