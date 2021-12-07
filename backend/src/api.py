import os
from flask import Flask, request, jsonify, abort, Response
# from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS, cross_origin

#from .database.models import db_drop_and_create_all, setup_db, Drink
from .database.models import setup_db, Drink, db_drop_and_create_all
from .auth.authnew import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)




'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
#db_drop_and_create_all()

# ROUTES

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET' ])
def getDrink():
    drinks = Drink.query.all()
    drink = [drink.short() for drink in drinks]
  
    return jsonify({      
           "success": True,
         "drinks": drink
        })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    """
     Method handles GET requests for getting drinks-detail
     :param jwt:
    :return:
    """

    # get all drinks
    drinks = Drink.query.all()

    # return data view
    return jsonify({
        # list interpolation
        'drinks': [drink.long() for drink in drinks],
        'success': True
    }), 200



'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    req = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        req_title = req.get('title')
        req_recipe = req.get('recipe')
        if req_title:
            drink.title = req_title

        if req_recipe:
            drink.recipe = json.dumps(req['recipe'])

        drink.update()
    except BaseException:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]}), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    """
    Method handles DELETE request to delete drinks
    :param payload:
    :param drink_id:
    :return:
    """

    try:
        # get drink by id
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        # abort if no drink was found
        if drink is None:
            abort(404)

        # delete drink
        drink.delete()

        # return data to view
        return jsonify({
            'deleted': drink_id,
            'success': True
        }), 200
    except:
        abort(422)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404



'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''



@app.errorhandler(AuthError)
def autherror(error):
        return jsonify({
            "success":False,
            "error":error.status_code,
            "message":error.error
        }),error.status_code

if __name__ == "__main__":
    app.debug = True
    app.run()
