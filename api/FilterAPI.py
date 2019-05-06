from flask import Blueprint, request, send_file, Response
from services.DBConn import db
import api.AuthorizationAPI
from bson.json_util import dumps
import json


filter_api = Blueprint('filter_api', __name__)
userDB = db.users
listingDB = db.listings


@filter_api.route("", methods=['GET'])
@api.AuthorizationAPI.requires_auth
def filterListings():
    condition = request.args.get('condition')  # /filter?condition=
    category = request.args.get('category')  # /filter?condition=

    try:
        if (condition is not None) and not category :
            listings = dumps(listingDB.find({'condition' : condition}))
        elif (category is not None) and not condition :
            listings = dumps(listingDB.find({'category':category }))
        elif(condition is not None) and (category is not None):
            listings = dumps(listingDB.find({'condition' : condition, 'category':category }))

        if listings is None:
            return json.dumps({'error': "Filterd item not found: "})
        else:
            return listings
    except Exception as e:
        print(e)
        return json.dumps({'error': "Server error filtering the database.", 'code': 123})