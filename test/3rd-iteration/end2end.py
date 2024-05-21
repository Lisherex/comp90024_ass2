import unittest, requests, json, time

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}{path}')


class TestEnd2End(unittest.TestCase):
    def test_airqaulity_copd(self):
        r= test_request.get('/airquality/copd')
        o= (r.json())
        self.assertEqual(len(o), 78)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(o[0]['average_total_copd_admissions_num']), 270.391134572132)

    def test_airqaulity_houseprice(self):
        r= test_request.get('/airquality/houseprice')
        o= (r.json())
        self.assertEqual(len(o), 180)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(o[0]['site_location']['latitude']), -38.1864662)
        self.assertEqual(float(o[0]['site_location']['longitude']), 146.258331)

    def test_airqaulity_vehicle(self):
        r= test_request.get('/airquality/vehicle')
        o= (r.json())
        self.assertEqual(len(o), 76)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(o[0]['total_dwelling']), 11849)

    def test_airqaulity_rsd(self):
        r= test_request.get('/airquality/rsd')
        o= (r.json())
        self.assertEqual(len(o), 78)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(o[0]['average_total_rsd_admissions_num']), 1635.441179261734)

    def test_houseprice_copd(self):
        r= test_request.get('/houseprice/copd')
        o= (r.json())
        self.assertEqual(len(o), 14)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(o[0]['average_price']), 1165231.724870764)


    def test_houseprice_vehicle(self):
        r= test_request.get('/houseprice/vehicle')
        o= (r.json())
        self.assertEqual(len(o), 14)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o[0]['station_id'], '4afe6adc-cbac-4bf1-afbe-ff98d59564f9')

if __name__ == '__main__':
    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()
