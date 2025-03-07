import unittest
from datetime import datetime
import random
import string
import rstr
import copy
from dataGenerator import generatestring, generatenumber, generateinteger, generatevalue, gen_data

class TestDataGen(unittest.TestCase):

    def test_generatestring(self):
        data = {
            'minLength': 5,
            'maxLength': 10,
            'enum': ['A', 'B', 'C']
        }
        result = generatestring(data)
        self.assertIn(result, data['enum'])

        data = {
            'pattern': r'[A-Z]{5}'
        }
        result = generatestring(data)
        self.assertTrue(rstr.xeger(data['pattern']), result)

        data = {
            'format': 'date-time',
            'date-time-frmt': '%Y-%m-%dT%H:%M:%S'
        }
        result = generatestring(data)
        self.assertEqual(result, datetime.now().strftime(data['date-time-frmt']))

    def test_generatenumber(self):
        data = {
            'enum': [1.1, 2.2, 3.3]
        }
        result = generatenumber(data)
        self.assertIn(result, data['enum'])

        data = {
            'format': 'float'
        }
        result = generatenumber(data)
        self.assertIsInstance(result, float)

    def test_generateinteger(self):
        data = {
            'enum': [1, 2, 3]
        }
        result = generateinteger(data)
        self.assertIn(result, data['enum'])

        data = {
            'format': 'int32',
            'minimum': 10,
            'maximum': 20
        }
        result = generateinteger(data)
        self.assertTrue(10 <= result <= 20)

    def test_generatevalue(self):
        data = {
            'string_field': {'type': 'string', 'minLength': 5, 'maxLength': 10},
            'number_field': {'type': 'number', 'enum': [1.1, 2.2, 3.3]},
            'integer_field': {'type': 'integer', 'minimum': 10, 'maximum': 20}
        }
        outdict = {}
        jsondata = {}
        result = generatevalue(data, outdict, jsondata)
        self.assertIn('string_field', result)
        self.assertIn('number_field', result)
        self.assertIn('integer_field', result)

    def test_gen_data(self):
        jsondata = {
            'properties': {
                'data_key': {
                    'items': [{
                        'properties': {
                            'string_field': {'type': 'string', 'minLength': 5, 'maxLength': 10},
                            'number_field': {'type': 'number', 'enum': [1.1, 2.2, 3.3]},
                            'integer_field': {'type': 'integer', 'minimum': 10, 'maximum': 20}
                        }
                    }]
                }
            }
        }
        result = gen_data(jsondata, data_key='data_key')
        self.assertIn('string_field', result)
        self.assertIn('number_field', result)
        self.assertIn('integer_field', result)

if __name__ == '__main__':
    unittest.main()