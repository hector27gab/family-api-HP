"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    try:
        get_one_member = jackson_family.get_member(id)

        if get_one_member:
            return get_one_member, "was found", 200

        else:
            return "Error: the member doesn't exist", 404

    except:
        return "An Error Ocurred", 500

@app.route('/member', methods=['POST'])
def create_new_member():

    try:
        id = request.json.get("id")
        first_name = request.json.get("first_name")
        age = request.json.get("age")
        lucky_numbers = request.json.get("lucky_members")

        new_member = {
            "id":jackson_family._generate_id(),
            "firt_name":first_name,
            "last_name":"Jackson",
            "age":age,
            "lucky_numbers":lucky_numbers,
        }
        jackson_family.add_member(new_member)

        return jsonify({"message": "member added"})
        
    except Exception as error:

        return jsonify({"Error": str(error)}), 400

@app.route('/member/<int:id>', methods=["DELETE"])
def delete_member(id):

    try: 
        update_members = jackson_family.delete_member(id)
        
        if (update_members):
            return jsonify({"message":"the member doesn't exist"}), 404
        
        else:
            return jsonify({"Done": True}), 200
    
    except Exception as error:

        return jsonify({"error": str(error)}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
