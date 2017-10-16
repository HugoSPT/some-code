from api import app
from api.hotels.models import (
    Hotel,
    Accommodation,
    StarsRating
)

from json import dumps
from flask import request


expected = ['name', 'address']

"""
    Gets all the hotels stored in the DB

    Method: GET

    Returns:
        200: Dictionary containing all the hotels
"""
@app.route("/api/v1.0/hotels/", methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return dumps({
            'hotels' : [hotel.to_json() for hotel in hotels],
            'size':len(hotels)
        }), 200

"""
    Creates a new hotel

    Method: POST

    Returns:
        400: Dictionary containing error message
        200: Dictionary containing the new hotel id and a successful message
"""
@app.route("/api/v1.0/hotels/", methods=['POST'])
def create_hotel():
    if not request.json or not is_valid(request.json):
        return dumps({'message' : 'Invalid JSON.'}), 400

    hotel = Hotel(request.json['name'], request.json['address'])
    hotel.parse(request.json)
    hotel_id = hotel.insert()

    return dumps({'message': 'Hotel inserted successfully.', 'hotel_id': hotel_id}), 200

"""
    Gets a specific hotel

    Method: GET

    Args:
        hotel_id: the identification of the hotel to be retrieved

    Returns:
        400: Dictionary containing error message
        200: Dictionary containing the hotel and number of results
"""
@app.route("/api/v1.0/hotels/<int:hotel_id>", methods=['GET'])
def get_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if hotel:
        return dumps({
                'hotels': [hotel.to_json()],
                'size': 1
            }), 200
    
    return dumps({'message': 'Hotel not found.'}), 404

"""
    Updates a specific hotel

    Method: PUT

    Args:
        hotel_id: the identification of the hotel to be updated

    Returns:
        400: Dictionary containing error message
        200: Dictionary containing successful message
"""
@app.route("/api/v1.0/hotels/<int:hotel_id>", methods=['PUT'])
def update_hotel(hotel_id):
    if not request.json:
        return dumps({'message' : 'Invalid JSON.'}), 400

    hotel = Hotel.query.get(hotel_id)
    hotel.parse(request.json)
    hotel.update()

    return dumps({'message': 'Hotel updated successfully.'}), 200

"""
    Deletes a specific hotel

    Method: DELETE

    Args:
        hotel_id: the identification of the hotel to be deleted

    Returns:
        404: If hotel to be deleted was not founded
        200: Dictionary containing successful message
"""
@app.route("/api/v1.0/hotels/<int:hotel_id>", methods=['DELETE'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if hotel:
        hotel.delete()
        return dumps({'message': 'Hotel inserted successfully.'}), 200

    return dumps({'error': 'Hotel not found.'}), 404

"""
    All available accommodations

    Method: GET

    Returns:
        200: Dictionary with all available accommodations
"""
@app.route("/api/v1.0/accommodations/", methods=['GET'])
def get_accommodations():
    accommodations = Accommodation.query.all()
    return dumps({
            'accommodations' : [accommodation.to_json() for accommodation in accommodations],
            'size':len(accommodations)
        }), 200

"""
    All available ratings

    Method: GET

    Returns:
        200: Dictionary with all available ratings
"""
@app.route("/api/v1.0/stars_rating/", methods=['GET'])
def get_stars_rating():
    stars_rating = StarsRating.query.all()
    return dumps({
            'stars_rating' : [star_rating.to_json() for star_rating in stars_rating],
            'size':len(stars_rating)
        }), 200

"""
    Hotel suggestions based on a string to be searched in hotel's name and address

    Method: POST

    Returns:
        404: When there is no matched hotels
        200: Dictionary with all matched hotels
"""
@app.route("/api/v1.0/suggestions/", methods=['POST'])
def suggestions():
    if not request.json:
        return dumps({'message' : 'Invalid JSON.'}), 400

    results = Hotel.search(request.json['term'])
    
    if results:
        return dumps({'suggestions': results}), 200
    
    return dumps({'suggestions': []}), 404


"""
    Checks if a given json if valid (i.e. has the basic required keys)

    Args:
        json: the json to be checked

    Returns:
        True if all expected keys are present otherwise False
"""
def is_valid(json):
    return all(key in json.keys() for key in expected)
