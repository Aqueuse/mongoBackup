import json
import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient('localhost', 27017)
except ConnectionFailure:
    print("connection failed")
    sys.exit(1)


def mongo_to_json(my_collection, my_database, my_filename):
    database = client[my_database]
    collection = database[my_collection]

    if collection.count() == 0:
        print("... collection don't exist or empty \nfile not created\n")

    else:
        print("... collection founded in the database\n")
        collection_list = []

        # remove objectID, because it's crap
        for element in collection.find():
            del element['_id']
            collection_list.append(element)

        json_file = open(my_filename, 'w+')

        json_file.write(json.dumps(collection_list))
        json_file.close()
        print("=> "+my_filename+" writed\n")


def json_to_mongo(my_collection, my_database, my_filename):
    database = client[my_database]
    collection_mongo = database[my_collection]

    json_file = open(my_filename, 'r')
    line = json_file.readline()

    collection_dict = json.loads(line)
    json_file.close()

    cured_collection = restore_pk(collection_dict)
    print(cured_collection)
    print("\n")

    # if collection exist, backup the old before and drop
    print("=> save the old data and clean the collection\n")
    mongo_to_json(my_collection, my_database, 'old_'+my_collection)
    collection_mongo.drop()

    collection_mongo.insert_many(collection_dict)
    print("=> collection restored  \\o/\n")


# get a pk to items in the collection
def restore_pk(my_collection_dict):
    pk = 0
    for element in my_collection_dict:
        element['pk'] = pk
        pk = pk + 1
    return my_collection_dict
