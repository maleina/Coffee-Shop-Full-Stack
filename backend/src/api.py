import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE Uncomment the following line to initialize the database.
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


# db_drop_and_create_all()

# ROUTES

# Temporary route for testing authorization.
# @app.route('/headers')
# @requires_auth('post:drinks')
# def headers(payload):
#     print(payload)
#     return 'Access Granted'


'''
@DONE Implement endpoint
    GET /drinks
        It should be a public endpoint.
        It should contain only the drink.short() data representation.
    Returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure.
'''


@app.route('/drinks')
def retrieve_drinks():
    # Retrieve drinks and format them correctly.
    selection = Drink.query.all()
    drinks = [drink.short() for drink in selection]
    # Abort if there are no drinks in the database,
    # otherwise, return all drinks in short form.
    if len(drinks) == 0:
        abort(404)
    return jsonify({'success': True, "drinks": drinks})


'''
@DONE Implement endpoint
    GET /drinks-detail
        It should require the 'get:drinks-detail' permission.
        It should contain the drink.long() data representation.
    Returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure.
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drink_detail(payload):
    # Retrieve drinks and format them correctly.
    selection = Drink.query.all()
    drinks = [drink.long() for drink in selection]

    # Abort if there are no drinks in the database,
    # otherwise, return all drinks in long form.
    if len(drinks) == 0:
        abort(404)
    return jsonify({"success": True, "drinks": drinks})


'''
@DONE Implement endpoint
    POST /drinks
        It should create a new row in the drinks table.
        It should require the 'post:drinks' permission.
        It should contain the drink.long() data representation.
    Returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure.
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        # Get new drink data from request.
        body = request.get_json()
        req_title = body.get('title', None)
        req_recipe = body.get('recipe', None)

        # Validate that title and recipe are both present,
        # if not, abort.
        if (req_title is None) or (req_recipe is None):
            return abort(422)

        # If the recipe has not been input as a list,
        # format it correctly and create the drink object.
        if type(req_recipe) is not list:
            req_recipe = [req_recipe]
        drink = Drink(title=req_title, recipe=json.dumps(req_recipe))

        # Abort if the drink is already present in the database.
        if drink.is_duplicate():
            abort(422)

        # Otherwise, create a row in the database for the drink.
        drink.insert()
        return jsonify({'success': True, "drinks": [drink.long()]})
    except AuthError:
        abort(422)


'''
@DONE Implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        It should respond with a 404 error if <id> is not found.
        It should update the corresponding row for <id>.
        It should require the 'patch:drinks' permission.
        It should contain the drink.long() data representation.
    Returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure.
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        # Find the drink with the given id,
        # if it doesn't exist abort.
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)

        # Retrieve the updated drink data.
        body = request.get_json()
        req_title = body.get('title', None)
        req_recipe = body.get('recipe', None)

        # Update the drink with the new values.
        if req_title is not None:
            drink.title = req_title
        if req_recipe is not None:
            if type(req_recipe) is not list:
                req_recipe = [req_recipe]
            drink.recipe = json.dumps(req_recipe)
        drink.update()
        return jsonify({"success": True, "drinks": [drink.long()]})
    except AuthError:
        abort(422)


'''
@DONE Implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id.
        It should respond with a 404 error if <id> is not found.
        It should delete the corresponding row for <id>.
        It should require the 'delete:drinks' permission.
    Returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure.
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        # Find the drink with the given id,
        # if it doesn't exist abort.
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)

        drink.delete()
        return jsonify({"success": True, "delete": id})
    except AuthError:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity:
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE Implement error handlers using the @app.errorhandler(error) decorator.
    Each error handler should return (with appropriate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
@DONE Implement error handler for 404.
    Error handler should conform to general task above.
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@DONE Implement error handler for AuthError.
    Error handler should conform to general task above.
'''


@app.errorhandler(AuthError)
def handle_invalid_usage(error):
    return jsonify({
        "success": False,
        "error": error.error,
        "message": error.status_code
    }), error.error
