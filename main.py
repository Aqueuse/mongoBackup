import json
import os
import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient('localhost', 27017)
except ConnectionFailure:
    print("connection failed")
    sys.exit(1)


def mongo_to_json(my_collection, my_database, my_directory):
    try:
        os.mkdir(my_directory)
    except FileExistsError:
        print('file exist')

    database = client[my_database]
    collection = database[my_collection]

    collection_list = []

    for element in collection.find():
        # remove objectID, because it's crap
        del element['_id']
        collection_list.append(element)

    json_file = open(my_directory+'/'+collection.name, 'w+')

    json_file.write(json.dumps(collection_list))
    json_file.close()


def json_to_mongo(my_collection, my_database):
    database = client[my_database]
    collection_mongo = database[my_collection]

    json_file = open('restore/'+my_collection, 'r')
    line = json_file.readline()

    collection_dict = json.loads(line)
    json_file.close()

    cured_collection = restore_pk(collection_dict)
    print(cured_collection)

    # if collection exist, backup the old before and drop
    print("save the old data and clean the collection")
    mongo_to_json(my_collection, my_database, 'old')
    collection_mongo.drop()

    collection_mongo.insert_many(collection_dict)


# get a pk to items in the collection
def restore_pk(my_collection_dict):
    pk = 0
    for element in my_collection_dict:
        element['pk'] = pk
        pk = pk + 1
    return my_collection_dict


# mongo_to_json('articles', 'oursAgile', 'ours')
json_to_mongo('articles', 'oursAgile')
