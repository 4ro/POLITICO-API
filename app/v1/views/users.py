from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v1.utilities.validator import response, exists
from app.v1.models.user_model import User
from app.v1.blueprints import bp


users_list = User.users




@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):

    model = User()
    data = model.find_by_id(id)

    if not data:
        return response('User not found', 404)

    return response('Request sent successfully', 200, [data])



