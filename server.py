from flask import Flask, jsonify, request, json
import re


app = Flask(__name__)

# in memory data of pets
pets = [
    {
    "id": 1,
    "category": {
        "id": 1,
        "name": "Dog"
    },
    "name": "Buddy",
    "photoUrls": [
        "https://someurl.com/of-this-put/"
    ],
    "tags": [
        {
        "id": 2,
        "name": "puppy"
        }
    ],
    "status": "available"
    }
]
    
# checks all attributes within pet object
def validate_pet_data(pet):
    if 'id' in pet:
        if type(pet['id']) != int:
            return False, 'id'
    else:
        return False, 'no id'

    if 'category' in pet and type(pet['category']) == dict: 
        if 'id' in pet['category'] and type(pet['category']['id']) != int:
            return False, 'category id'
        if 'name' in pet['category'] and type(pet['category']['name']) != str:
            return False, 'category name'
    elif type(pet['category']) != dict:
        return False, 'category'

    if 'name' in pet and type(pet['name']) != str:
        return False, 'name'

    if 'photoUrls' in pet and type(pet['photoUrls']) == list:
        # Used a regex here since there can be many different requirements on 
        # the type of urls allowed. I just want to make sure it starts with 
        # https://
        regex = re.compile(r'^(https://)', re.IGNORECASE)
        for url in pet['photoUrls']:
            matches = re.match(regex, url)
            if not matches:
                return False, url
    elif type(pet['photoUrls']) != list:
        return False, 'photoUrls'

    if 'tags' in pet and type(pet['tags']) == list:
        for tag in pet['tags']:
            if type(tag) != dict:
                return False, f'{tag}'
            if 'id' in tag and type(tag['id']) != int:
                return False, 'tag id'
            if 'name' in tag and type(tag['name']) != str:
                return False, 'tag name'
    elif type(pet['tags']) != list:
        return False, 'tags'

    if 'status' in pet and type(pet['status']) != str:
        return False, 'status'

    return True, 'All good!'


@app.route('/pet', methods=['POST'])
def post_pet():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid input'}), 405

    all_good, message = validate_pet_data(pet=data)
    if not all_good:
        return jsonify({'error': message}), 405
        #return jsonify({'error': 'Invalid input'}), 405
    
    ids_set = {pet['id'] for pet in pets}
    if data['id'] in ids_set:
        return jsonify({'Invalid ID supplied'}), 400
    
    pets.append(data)

    return jsonify({'result': data['id']}), 201

@app.route('/pet', methods=['PUT'])
def put_pet():
    data = request.json
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    
    all_good, message = validate_pet_data(pet=data)
    if not all_good:
        if message == 'id':
            return jsonify({'error': 'Invalid ID supplied'}), 400
        return jsonify({'error': 'Validation exception'}), 405
    
    ids_set = {pet['id'] for pet in pets}
    if data['id'] not in ids_set:
        return jsonify({'Invalid ID supplied'}), 400

    for i, pet in enumerate(pets):
        if pet['id'] == data['id']:
            pets[i] = data
            return jsonify({'result': data}), 204
    
    return jsonify({'error': 'Pet not found'}), 404

@app.route('/pet/<int:petId>', methods=['GET'])
def get_pet(petId):
    if type(petId) != int:
        return jsonify({'error': 'Invalid ID supplied'}), 400

    for i, pet in enumerate(pets):
        if pet['id'] == petId:
            result = pets[i]
            return jsonify({'result': result}), 200
    
    return jsonify({'error': 'Pet not found'}), 404

@app.route('/pet/<int:petId>', methods=['POST'])
def post_pet_form_data(petId):
    data = request.form

    if not data:
        return jsonify({'error': 'Missing data'}), 400
    
    all_good, message = validate_pet_data(pet=data)
    if not all_good:
        #return jsonify({'error': 'Invalid input'}), 405
        return jsonify({'error': message}), 405

    ids_set = {pet['id'] for pet in pets}
    if petId not in ids_set:
        return jsonify({'Invalid ID input'}), 400
    
    for i, pet in enumerate(pets):
        if pet['id'] == data['id']:
            pets[i]['name'] = data['name']
            pets[i]['status'] = data['status']
            return jsonify({'result': pet}), 204


@app.route('/pet/<int:petId>', methods=['DELETE'])
def delete_pet_form_data(petId):
    if type(petId) != int:
        return jsonify({'error': 'Invalid ID supplied'}), 400

    for i, pet in enumerate(pets):
        if pet['id'] == petId:
            deleted = pets.pop(i)
            return jsonify({'result': deleted}), 204

    return jsonify({'error': 'Pet not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

