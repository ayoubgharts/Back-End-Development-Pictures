from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all picture URLs in the data"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a single picture URL by id"""
    # Find the picture with the matching id
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200
    
    # If not found, return a 404 error
    return jsonify({"error": "Picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry"""
    # Extract picture data from the request body
    picture = request.get_json()

    # Check if picture has an 'id' field
    if "id" not in picture:
        return jsonify({"error": "Picture must have an id"}), 400

    # Check if a picture with the same id already exists
    for existing_picture in data:
        if existing_picture.get("id") == picture["id"]:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append the new picture to the data list
    data.append(picture)

    # Optionally, save the updated data list to the JSON file
    with open(json_url, "w") as f:
        json.dump(data, f)

    # Return the created picture data, including its id, in the response
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture by id"""
    # Extract updated data from the request body
    new_data = request.get_json()

    # Find the picture with the matching id
    for picture in data:
        if picture.get("id") == id:
            # Update the picture with new data
            picture.update(new_data)
            
            # Save the updated data list to the JSON file
            with open(json_url, "w") as f:
                json.dump(data, f)
            
            return jsonify({"Message": "Picture updated successfully"}), 200

    # If the picture is not found, return a 404 error
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by id"""
    # Find the index of the picture with the matching id
    for index, picture in enumerate(data):
        if picture.get("id") == id:
            # Remove the picture from the data list
            del data[index]
            
            # Save the updated data list to the JSON file
            with open(json_url, "w") as f:
                json.dump(data, f)
            
            return '', 204  # Return 204 No Content

    # If the picture is not found, return a 404 error
    return jsonify({"message": "picture not found"}), 404
