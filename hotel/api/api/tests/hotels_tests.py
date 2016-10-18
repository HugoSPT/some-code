from api import (
    app,
    db
)
from json import loads, dumps
import unittest
from unittest.mock import patch

from api.hotels.models import (
    Hotel
)


class HotelsTests(unittest.TestCase): 

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_get_home(self):
        result = self.app.get('/api/v1.0/hotels/')

        self.assertEqual(result.status_code, 200) 

        result = loads(result.data.decode('utf-8'))
        
        self.assertEqual(type(result), dict)
        self.assertTrue('hotels' in result.keys())

    def test_get_hotel(self):
        hotel_id = loads(
            self.app.get(
                '/api/v1.0/hotels/'
            ).data.decode('utf-8')
        )['hotels'][0]['id']

        result = self.app.get('/api/v1.0/hotels/' + str(hotel_id))

        self.assertEqual(result.status_code, 200) 

        result = loads(result.data.decode('utf-8'))
        
        self.assertEqual(type(result), dict)
        self.assertTrue('hotels' in result.keys())
        self.assertEqual(len(result['hotels']), 1)

    def test_insert_hotel_invalid_json(self):

        result = self.app.post(
            '/api/v1.0/hotels/',
            data=dumps({}),
            content_type='application/json'
        )

        data = loads(result.data.decode('utf-8'))
    
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data, {"message": "Invalid JSON."})

    @patch('api.hotels.models.Hotel.insert')
    @patch('api.db.session.commit')
    def test_insert_hotel_valid_json(self, commit_mock, insert_mock):

        insert_mock.return_value = 1

        result = self.app.post(
            '/api/v1.0/hotels/',
            data=dumps({'name': 'Test Hotel', 'address': 'Test Address'}),
            content_type='application/json'
        )

        data = loads(result.data.decode('utf-8'))
        
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data, {"message": "Hotel inserted successfully.", "hotel_id": 1})

    def test_delete_hotel_not_found_id(self):

        result = self.app.delete('/api/v1.0/hotels/0')
        data = loads(result.data.decode('utf-8'))
    
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data, {'error': 'Hotel not found.'})

    @patch('api.db.session.commit')
    def test_delete_hotel_not_found_id(self, commit_mock):
        hotel_id = loads(
            self.app.get(
                '/api/v1.0/hotels/'
            ).data.decode('utf-8')
        )['hotels'][0]['id']

        result = self.app.delete('/api/v1.0/hotels/' + str(hotel_id))
        data = loads(result.data.decode('utf-8'))
    
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data, {'message': 'Hotel inserted successfully.'})

