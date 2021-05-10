from server import app, validate_pet_data, pets
import unittest
import json

class PetTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def test_pet_post_status(self):
        test_pet = {
            "id": 2,
            "category": {
                "id": 2,
                "name": "Cat"
            },
            "name": "Butter",
            "photoUrls": [
                "https://someurl.com/of-this-pet2/",
                "https://someurl.com/of-this-pet10/"
            ],
            "tags": [
                {
                "id": 2,
                "name": "puppy"
                }
            ],
            "status": "available"
        }
        
        with app.test_client() as tc:
            result = tc.post('/pet', json=test_pet)
            self.assertEqual(result.status_code, 201)
        
        # we are removing the test pet that we added through the test client  
        pets.pop()
        
    def test_pet_post_status_400(self):
        test_pet = {
            "id": 1,
            "category": {
                "id": 2,
                "name": "Cat"
            },
            "name": "Butter",
            "photoUrls": [
                "https://someurl.com/of-this-pet2/",
                "https://someurl.com/of-this-pet10/"
            ],
            "tags": [
                {
                "id": 2,
                "name": "puppy"
                }
            ],
            "status": "available"
        }
        
        with app.test_client() as tc:
            result = tc.post('/pet', json=test_pet)
            self.assertEqual(result.status_code, 400)
        
    def test_pet_post_status_405_empty(self):
        test_pet = {}
        
        with app.test_client() as tc:
            result = tc.post('/pet', json=test_pet)
            self.assertEqual(result.status_code, 405)
            self.assertEqual(json.loads(result.data)['error'], 'Invalid input')
        
        with app.test_client() as tc:
            result = tc.post('/pet', json=test_pet)
            self.assertEqual(result.status_code, 405)
            self.assertEqual(json.loads(result.data)['error'], 'Invalid input')
            
    def test_pet_post_content(self):
        test_pet = {
            "id": 2,
            "category": {
                "id": 2,
                "name": "Cat"
            },
            "name": "Butter",
            "photoUrls": [
                "https://someurl.com/of-this-pet2/",
                "https://someurl.com/of-this-pet10/"
            ],
            "tags": [
                {
                "id": 2,
                "name": "puppy"
                }
            ],
            "status": "available"
        }
        
        with app.test_client() as tc:
            result = tc.post('/pet', json=test_pet)
            self.assertEqual(result.content_type, 'application/json')
            
        # we are removing the test pet that we added through the test client  
        pets.pop()
        
    def test_pet_post_data(self):
        test_pet = {
            "id": 2,
            "category": {
                "id": 2,
                "name": "Cat"
            },
            "name": "Butter",
            "photoUrls": [
                "https://someurl.com/of-this-pet2/",
                "https://someurl.com/of-this-pet10/"
            ],
            "tags": [
                {
                "id": 2,
                "name": "puppy"
                }
            ],
            "status": "available"
        }
        
        with app.test_client() as tc:
            response = tc.post('/pet', json=test_pet)
            data = json.loads(response.data)
            self.assertEqual(data['result'], 2)
            # self.assertEqual(data['category']['id'], 2)
            # self.assertEqual(data['category']['name'], 'Cat')
            # self.assertEqual(data['name'], 'Butter')
            # self.assertEqual(data['photoUrls'][0], 'https://someurl.com/of-this-pet2/')
            # self.assertEqual(data['photoUrls'][1], 'https://someurl.com/of-this-pet10/')
            # self.assertEqual(data['tags'][0]['id'], 2)
            # self.assertEqual(data['tags'][0]['name'], 'puppy')
            # self.assertEqual(data['status'], 'available')

        # we are removing the test pet that we added through the test client  
        pets.pop()
            
if __name__ == '__main__':
    unittest.main()