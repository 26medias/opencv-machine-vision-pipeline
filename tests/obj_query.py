import uuid
import math


def query(objects, query):
    output = []
    for object_id in objects.keys():
        obj = objects[object_id]
        is_match = True
        for qk in query.keys():
            if "$opt" in query[qk] and query[qk]["$opt"] is True and qk not in obj:
                continue
            for opk in query[qk].keys():
                if opk == "$eq":
                    is_match = is_match and qk in obj and obj[qk] == query[qk][opk]
                elif opk == "$exists":
                    if query[qk][opk] is False:
                        is_match = is_match and qk not in obj
                    elif query[qk][opk] is True:
                        is_match = is_match and qk in obj
                elif opk == "$gt":
                    is_match = is_match and qk in obj and obj[qk] > query[qk][opk]
                elif opk == "$lt":
                    is_match = is_match and qk in obj and obj[qk] < query[qk][opk]
        
        if is_match is True:
            output.append(object_id)
    return output




objects = {
    '0fe2521f-0a59-4ca2-9906-2ff473a7fa17': {'score': 0.9223633, 'label': '92.24%', 'type': 'face', 'x1': 375, 'y1': 231, 'x2': 452, 'y2': 361, 'last_seen': 0, 'active': True, 'number': 0},
    '16f5438e-db87-40bc-9b4c-f2e6376e4ea8': {'score': 0.96777344, 'label': '96.78%', 'type': 'face', 'x1': 366, 'y1': 242, 'x2': 449, 'y2': 369, 'last_seen': 0, 'active': True, 'number': 0},
    'a6af1ab9-652a-4b72-884c-858358512ce5': {'score': 0.9995117, 'label': '99.95%', 'type': 'face', 'x1': 357, 'y1': 213, 'x2': 453, 'y2': 352, 'last_seen': 0, 'active': True, 'number': 0, 'age': '(48, 53)', 'age_inference_count': 1}
}

print("Actual:")
print(query(objects, {'type': {'$eq': 'face'}, 'score': {'$gt': 0.7}, 'age_inference_count': {'$opt': True, '$lt': 20}}))

print("Test:")
print(query(objects, {
    "type": {
        "$eq": "face"
    },
    "score": {
        "$gt": 0.7
    },
    "age_inference_count": {
        "$opt": True,
        "$lt": 20
    }
}))
"""
objects = {
    "A": {
        "type":         "face",
        "gender":       "male",
        "gender_count": 30,
        "n":            5
    },
    "B": {
        "type":         "face",
        "gender":       "female",
        "gender_count": 10,
        "n":            0
    },
    "C": {
        "type":         "face",
        "gender":       "male",
        "n":            50
    }
}

print("Faces:")
print(query(objects, {
    "type": {
        "$eq":  "face"
    }
}))

print("gender_count:")
print(query(objects, {
    "type": {
        "$eq":  "face"
    },
    "gender_count": {
        "$opt": True,
        "$lt":  20
    }
}))

print("gender_count 2:")
print(query(objects, {
    "type": {
        "$eq":  "face"
    },
    "gender_count": {
        "$lt":  20
    }
}))
"""