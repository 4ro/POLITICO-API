from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v1.models.my_db import Database
from app.v1.models.party_model import Party
from app.v1.utilities.validator import response, exists
from app.v1.blueprints import bp


party_list = Party.parties


@bp.route('/parties', methods=['POST', 'GET'])
def create_party():
    if request.method == 'POST':
        """ Create party end point """

        data = request.get_json()

        if not data:
            return response("No data was provided", 400)

        try:
            name = data['name']
            hq_address = data['hq_address']
            logo_url = data['logo_url']
            
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        party = Party(name, hq_address, logo_url)

        if not party.validate_object():
            return response(party.error_message, party.error_code)

        # append new party to list
        party.save()

        # return added party
        return response("Party created successfully", 201, [party.as_json()])

    elif request.method == 'GET':
        """ Get all parties end point """

        return response('Request was sent successfully', 200, party_list)


@bp.route('/parties/<int:id>', methods=['GET', 'DELETE'])
def get_party(id):

    model = Party()
    data = model.find_by_id(id)

    if not data:
        return response('Party not found', 404)

    if request.method == 'GET':
        return response('Request sent successfully', 200, [data])
    else:
        party = model.from_json(data)
        party.delete()
        return response(
            '{} deleted successfully'.format(party.name), 200, [data])


@bp.route('/parties/<int:id>/<string:name>', methods=['PATCH'])
def edit_party(id, name):

    model = Party()
    data = model.find_by_id(id)

    if not data:
        return response('Party not found', 404)

    party = model.from_json(data)
    party.name = name

    if not party.validate_object():
        return response(party.error_message, party.error_code)

    party.edit(name)

    return response(
        '{} updated successfully'.format(party.name), 200, [data])

        