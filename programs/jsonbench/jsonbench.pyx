import json
import sys

EMPTY = ({}, 200000)
SIMPLE = ({'key1': 0, 'key2': True, 'key3': 'value', 'key4': 'foo', 'key5': 'string'}, 100000)
NESTED = ({'key1': 0, 'key2': SIMPLE[0], 'key3': 'value', 'key4': SIMPLE[0], 'key5': SIMPLE[0], u'key': u'\u0105\u0107\u017c'}, 100000)
HUGE = ([NESTED[0]] * 1000, 100)

cases = [EMPTY, SIMPLE, NESTED, HUGE]

cdef main(int n):
    for i in range(n):
        for case in cases:
            data, count = case
            for i in range(count):
                json_data = json.dumps(data)
                json.loads(json_data)
    print('OK')

main(int(sys.argv[1]))
