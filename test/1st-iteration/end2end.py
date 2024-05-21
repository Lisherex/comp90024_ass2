import unittest
import requests
from unittest.mock import patch

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.Session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}/{path}')
    

class TestEnd2End(unittest.TestCase):
    def test_student(self):
        self.assertEqual(test_request.get('/airquality/copd').status_code, 200)

        self.assertEqual(test_request.get('/airquality/houseprice').status_code, 200)

        self.assertEqual(test_request.get('/airquality/vehicle').status_code, 200)

        self.assertEqual(test_request.get('/airquality/rsd').status_code, 200)

        self.assertEqual(test_request.get('/houseprice/copd').status_code, 200)

        self.assertEqual(test_request.get('/houseprice/vehicle').status_code, 200)


if __name__ == '__main__':

    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()
