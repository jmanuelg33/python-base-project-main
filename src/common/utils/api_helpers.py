from flask import jsonify


def ok_response(status_code=200, **kwargs):
    response = jsonify(status="ok", **kwargs)

    response.status_code = status_code

    return response
