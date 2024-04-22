try:
    import requests
    import csv
    import json
    import logging
    import pytest
    import os
    from datetime import datetime
    import unittest
    from dazn_assignment import call_astros_api , data_insert , process_data, main
except Exception as e:
    print ('some modules are missing {}'.format(e))

url = "http://api.open-notify.org/astros.json"
url1 = "http://api.open-notify.org/astrs.json"

class api_test(unittest.TestCase):
    resp = ''
    def test_status_code(self):
        lst1 = call_astros_api(url)
        self.assertEqual(lst1[0],200)

        lst1 = call_astros_api('')
        self.assertNotEqual(lst1[0],200)


    # check if content is application/json
    def test_response_content(self):
        lst1 = call_astros_api(url)
        self.resp = json.loads(lst1[1])
        self.assertEqual(type(json.loads(lst1[1])) , dict)
        self.assertTrue(b'message' in lst1[1])

        lst1 = call_astros_api(url1)
        self.assertTrue(b'message' not in lst1[1])

        lst1 = call_astros_api('test')
        self.assertEqual(lst1[0], False)


    def test_process_data_case(self):
        dict1 = {"message": "success", "people":
            [{"name": "Sergey Prokopyev", "craft": "ISS"},
             {"name": "Dmitry Petelin", "craft": "ISS"}]}
        t1 = process_data(dict1)
        self.assertEqual(type(t1),list)

        dict1 = {"message": "success", "people": []}
        t1 = process_data(dict1)
        self.assertEqual(len(t1[0]), 0)

        dict1 = {"message": " "}
        t1 = process_data(dict1)
        self.assertEqual(len(t1[0]), 0)

        dict1 = 'test'
        t1 = process_data(dict1)
        self.assertEqual(type(t1), str)

        lst1 = call_astros_api(url1)
        t1 = process_data(lst1[1])
        self.assertEqual(type(t1), str)


    def test_insert_data(self):
        header = ['people','craft']
        data = [['Sergey Prokopyev', 'ISS'],['Dmitry Petelin', 'ISS']]
        resp = data_insert(header=header,data=data,path=os.getcwd())
        self.assertEqual(resp,'Success')

        header = ['people', 'craft']
        data = [['Sergey Prokopyev', 'ISS'], ['Dmitry Petelin', 'ISS']]
        resp = data_insert(header=header, data=data,path='')
        self.assertEqual(resp, 'Success')


    def test_main(self):
        main(url)
        main(url1)


if __name__ == '__main__':
    unittest.main()