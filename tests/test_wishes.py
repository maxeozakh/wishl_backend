from wishl import constants
from wishl.db import get_db

endpoints = constants.endpoints['wishlists']


def test_get_all_wishlists(client):
    response = client.get('/')
    wishlists = response.json["wishlists"]

    assert response.status_code == 200
    assert wishlists
    assert len(wishlists) == 3


def test_create(client, app):
    secrets = "owl are not what they seem"
    response = client.post(
        endpoints["create"], json={
            "uid": "4000",
            "secrets": secrets
        }
    )

    assert response.status_code == 200

    with app.app_context():
        user_secrets = get_db().execute(
            "SELECT * FROM wishlists WHERE uid = '4000'"
        ).fetchone()["secrets"]

        assert user_secrets == secrets


def test_create_errors(client, app):
    response = client.post(
        endpoints["create"], json={
            "uid": "4000",
        }
    )

    assert response.status_code == 400
    assert response.json['error'] == 'secrets is required.'

    response = client.post(
        endpoints["create"], json={
            "secrets": "Speak to Denel or Skaleel once the pillar has opened",
        }
    )

    assert response.status_code == 400
    assert response.json['error'] == 'uid is required.'


def test_get_wishlist_by_uid(client):
    response = client.get(endpoints["get_by_uid"] + '123')

    assert response.status_code == 200


def test_get_wishlist_by_uid_error(client):
    response = client.get(endpoints['get_by_uid'] + '00000')

    assert response.status_code == 400
    assert response.json['error'] == 'wishlist by uid is not found.'
