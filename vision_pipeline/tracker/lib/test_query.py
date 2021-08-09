
from query import obj_query

objects = {
    '66fed1e3-78b0-460d-b815-91c5dd8e34bd': {'score': 0.9995117, 'label': '99.95%', 'type': 'face', 'x1': 349, 'y1': 239, 'x2': 446, 'y2': 375, 'last_seen': 0, 'active': True, 'number': 0},
    '2e2147a6-e635-4b2d-98e9-85fb48841183': {'score': 0.42407227, 'label': '42.41%', 'type': 'face', 'x1': 60, 'y1': 168, 'x2': 98, 'y2': 210, 'last_seen': 23, 'active': True, 'number': 1}, 
    'fe52d9ca-007a-4caa-949d-e8b7bc56f0ad': {'score': 0.9868164, 'label': '98.68%', 'type': 'face', 'x1': 396, 'y1': 243, 'x2': 471, 'y2': 355, 'last_seen': 0, 'active': True, 'number': 5}
}

print("Actual:")
print(obj_query(
    objects, 
    {'type': {'$eq': 'face'}, 'score': {'$gt': 0.7}, 'age_inference_count': {'$opt': True, '$lt': 20}},
    True
))