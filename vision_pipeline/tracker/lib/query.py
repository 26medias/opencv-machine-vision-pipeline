import uuid
import math
import time


def obj_query(objects, query, debug=False):
    if debug is True: print("--------------")
    if debug is True: print(objects)
    if debug is True: print(query)
    output = []
    for object_id in objects.keys():
        if debug is True: print("-- ", object_id)
        obj = objects[object_id]
        is_match = True
        for qk in query.keys():
            if debug is True: print("> ", qk, "(", is_match, ")")
            if "$opt" in query[qk] and query[qk]["$opt"] is True and qk not in obj:
                if debug is True: print("# Optional & not found")
            else:
                for opk in query[qk].keys():
                    if opk == "$eq":
                        if debug is True: print("# $eq ", obj[qk], " -> ", qk in obj and obj[qk] == query[qk][opk])
                        is_match = is_match and qk in obj and obj[qk] == query[qk][opk]
                    elif opk == "$exists":
                        if query[qk][opk] is False:
                            if debug is True: print("# $exists:False ", qk not in obj)
                            is_match = is_match and qk not in obj
                        elif query[qk][opk] is True:
                            if debug is True: print("# $exists:True ", qk in obj)
                            is_match = is_match and qk in obj
                    elif opk == "$gt":
                        if debug is True: print("# $gt ", obj[qk], " -> ", qk in obj and obj[qk] > query[qk][opk])
                        is_match = is_match and qk in obj and obj[qk] > query[qk][opk]
                    elif opk == "$lt":
                        if debug is True: print("# $lt ", obj[qk], " -> ", qk in obj and obj[qk] < query[qk][opk])
                        is_match = is_match and qk in obj and obj[qk] < query[qk][opk]
                    elif opk == "$older_than":
                        is_match = is_match and qk in obj and round(time.time()*1000)-round(obj[qk]) >= query[qk][opk]
        
        if debug is True:
            print("Obj loop end: ", is_match, is_match is True, is_match == True)
        if is_match == True:
            if debug is True: print("Will return ", object_id)
            output.append(object_id)
    if debug is True: print(output)
    return output
