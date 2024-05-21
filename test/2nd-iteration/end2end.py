import unittest
import requests
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
    @classmethod
    def setUpClass(cls):
        cls.test_request = HTTPSession('http', 'localhost', 9090)

    # Mocking External Services
    def test_airquality_copd(self):
        response = self.test_request.get('/airquality/copd')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_airquality_rsd(self):
        response = self.test_request.get('/airquality/rsd')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_airquality_vehicle(self):
        response = self.test_request.get('/airquality/vehicle')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_airquality_houseprice(self):
        response = self.test_request.get('/airquality/houseprice')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_houseprice_copd(self):
        response = self.test_request.get('/houseprice/copd')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_houseprice_vehicle(self):
        response = self.test_request.get('/houseprice/vehicle')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    # Test content type and headers verification
    def test_content_type_for_copd(self):
        response = self.test_request.get('/airquality/copd')
        self.assertIn('text/html; charset=utf-8', response.headers['Content-Type'])

    def test_content_type_for_rsd(self):
        response = self.test_request.get('/airquality/rsd')
        self.assertIn('text/html; charset=utf-8', response.headers['Content-Type'])

    def test_content_type_for_vehicle(self):
        response = self.test_request.get('/airquality/vehicle')
        self.assertIn('text/html; charset=utf-8', response.headers['Content-Type'])

    def test_content_type_for_houseprice(self):
        response = self.test_request.get('/airquality/houseprice')
        self.assertIn('text/html; charset=utf-8', response.headers['Content-Type'])

    def test_content_type_for_houseprice_copd(self):
        response = self.test_request.get('/houseprice/copd')
        self.assertIn('text/html; charset=utf-8', response.headers['Content-Type'])

    def test_content_type_for_houseprice_vehicle(self):
        response = self.test_request.get('/houseprice/vehicle')
        self.assertIn('text/html; charset=utf-8', response.headers['Content-Type'])


if __name__ == '__main__':
    unittest.main()
