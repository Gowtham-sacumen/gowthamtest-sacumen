import random
from datetime import datetime
import rstr
import string

DEFAULT_MIN_LENGTH = 5
DEFAULT_MAX_LENGTH = 25
DEFAULT_INT32_MIN = 100000
DEFAULT_INT32_MAX = 9000000
DEFAULT_INT64_MIN = 10000000000
DEFAULT_INT64_MAX = 500000000000

def generatestring(data):
    now = datetime.now()
    letters = string.ascii_uppercase
    minLength = data.get('minLength', DEFAULT_MIN_LENGTH)
    maxLength = data.get('maxLength', DEFAULT_MAX_LENGTH)
    
    if 'enum' in data:
        return random.choice(data['enum'])
    if 'pattern' in data:
        return rstr.xeger(data['pattern'])
    if 'format' in data:
        if data['format'] == 'date-time':
            return now.strftime(data.get('date-time-frmt', "%Y-%m-%dT%H:%M:%S"))
        if data['format'] == 'date':
            return now.strftime("%Y-%m-%d")
    return ''.join(random.choice(letters) for _ in range(minLength, maxLength))

def generatenumber(data):
    if 'enum' in data:
        return random.choice(data['enum'])
    if 'format' in data and data['format'] in ('float', 'double'):
        return random.random()
    return random.random()

def generateinteger(data):
    multipleOf = data.get('multipleOf', 1)
    int32minimum = data.get('minimum', DEFAULT_INT32_MIN) // multipleOf
    int64minimum = data.get('minimum', DEFAULT_INT64_MIN) // multipleOf
    int32maximum = data.get('maximum', DEFAULT_INT32_MAX) // multipleOf
    int64maximum = data.get('maximum', DEFAULT_INT64_MAX) // multipleOf

    if 'enum' in data:
        return random.choice(data['enum'])
    if 'format' in data:
        if data['format'] == 'int32':
            return random.randint(int32minimum, int32maximum) * multipleOf
        if data['format'] == 'int64':
            return random.randint(int64minimum, int64maximum) * multipleOf
    return random.randint(int64minimum, int64maximum) * multipleOf

def generatevalue(data, outdict, jsondata):
    for key, value in data.items():
        if 'type' in value:
            if value['type'] == 'string':
                outdict[key] = generatestring(value)
            elif value['type'] == 'boolean':
                outdict[key] = random.choice([True, False])
            elif value['type'] == 'number':
                outdict[key] = generatenumber(value)
            elif value['type'] == 'integer':
                outdict[key] = generateinteger(value)
            elif value['type'] == 'object':
                outdict[key] = generatevalue(value['properties'], {}, jsondata)
            elif value['type'] == 'array':
                minItems = value.get('minItems', 1)
                maxItems = value.get('maxItems', 3)
                arrayItems = random.randint(minItems, maxItems)
                array = [generatevalue(item['properties'], {}, jsondata) if item['type'] == 'object' else generateitem(item) for item in value['items'] for _ in range(arrayItems)]
                outdict[key] = array
        elif '$ref' in value:
            refpath = value['$ref'].split('/')
            refproperties = jsondata[refpath[2]]['properties']
            outdict[key] = generatevalue(refproperties, {}, jsondata)
    return outdict

def generateitem(item):
    if item['type'] == 'string':
        return generatestring(item)
    if item['type'] == 'integer':
        return generateinteger(item)
    if item['type'] == 'number':
        return generatenumber(item)
    return None

def gen_data(jsondata, data_key=None, meta_key=None):
    dictobj = {}
    if meta_key:
        if meta_key != "root":
            meta_jsondata = jsondata['properties'][meta_key]
            properties = meta_jsondata['properties']
        else:
            meta_jsondata = {k: v for k, v in jsondata.items() if k != 'properties' or k != data_key}
            properties = jsondata['properties']
        dictobj = generatevalue(properties, {}, meta_jsondata)
        return dictobj
    if data_key:
        jsondata = jsondata['properties'][data_key]["items"][0]
        properties = jsondata['properties']
        dictobj = generatevalue(properties, {}, jsondata)
        return dictobj