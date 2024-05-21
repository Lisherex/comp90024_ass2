import unittest
import requests
import json
from unittest.mock import patch

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.Session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}/{path}')

    def post(self, path, data):
        return self.session.post(f'{self.base_url}/{path}', data)

    def put(self, path, data):
        return self.session.put(f'{self.base_url}/{path}', data)

    def delete(self, path):
        return self.session.delete(f'{self.base_url}/{path}')

class TestEnd2End(unittest.TestCase):
    #Mocking External Services
    def test_airquality_copd(self):
        self.assertEqual(test_request.get('/airquality/copd').status_code, 200)
        self.assertIsNotNone(test_request.get('/airquality/copd').json())

    def test_airquality_rsd(self):
        self.assertEqual(test_request.get('/airquality/rsd').status_code, 200)
        self.assertIsNotNone(test_request.get('/airquality/rsd').json())

    def test_airquality_vehicle(self):
        self.assertEqual(test_request.get('/airquality/vehicle').status_code, 200)
        self.assertIsNotNone(test_request.get('/airquality/vehicle').json())

    def test_airquality_houseprice(self):
        self.assertEqual(test_request.get('/airquality/houseprice').status_code, 200)
        self.assertIsNotNone(test_request.get('/airquality/houseprice').json())

    def test_houseprice_copd(self):
        self.assertEqual(test_request.get('/houseprice/copd').status_code, 200)
        self.assertIsNotNone(test_request.get('/houseprice/copd').json())

    def test_houseprice_vehicle(self):
        self.assertEqual(test_request.get('/houseprice/vehicle').status_code, 200)
        self.assertIsNotNone(test_request.get('/houseprice/vehicle').json())

    #Test content type and headers verification
    def test_content_type_for_copd(self):
        response = self.test_request.get('/airquality/copd')
        self.assertIn('application/json', response.headers['Content-Type'])

    def test_content_type_for_rsd(self):
        response = self.test_request.get('/airquality/rsd')
        self.assertIn('application/json', response.headers['Content-Type'])

    def test_content_type_for_vehicle(self):
        response = self.test_request.get('/airquality/vehicle')
        self.assertIn('application/json', response.headers['Content-Type'])

    def test_content_type_for_houseprice(self):
        response = self.test_request.get('/airquality/houseprice')
        self.assertIn('application/json', response.headers['Content-Type'])

    def test_content_type_for_houseprice_copd(self):
        response = self.test_request.get('/houseprice/copd')
        self.assertIn('application/json', response.headers['Content-Type'])

    def test_content_type_for_houseprice_vehicle(self):
        response = self.test_request.get('/houseprice/vehicle')
        self.assertIn('application/json', response.headers['Content-Type'])

if __name__ == '__main__':
    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()