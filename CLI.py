import sys
from pathvalidate import sanitize_filename, validate_filename, ValidationError
from mongo import mongo_to_json, json_to_mongo

help_message = "Save and restore locales MongoDB databases \n\nusage : \n \
      mongoBackup --save    -d \"database\" -c \"collection\" -f filename.json \n \
      mongoBackup --restore -d \"database\" -c \"collection\" -f filename.json \n"

# usage :
# mongoBackup --save -d "database" -c "collection" -f "filename.json"
# mongoBackup --restore -d "database" -c "collection" -f "filename.json"


def cli_parse():
    arguments = sys.argv[1:]

    if len(arguments) == 7:
        action = arguments[0]
        database_arg = arguments[1]
        database = arguments[2]
        collection_arg = arguments[3]
        collection = arguments[4]
        file_arg = arguments[5]
        filename = arguments[6]

        if (action == "--save" or action == "-s") \
                and database_arg == "-d" \
                and len(database) > 0 \
                and collection_arg == "-c" \
                and len(collection) > 0 \
                and file_arg == "-f" \
                and filename == valid_filename(filename):
            mongo_to_json(collection, database, filename)
        else:
            print(help_message)

        if (action == "--restore" or action == "-r") \
                and database_arg == "-d" \
                and len(database) > 0 \
                and collection_arg == "-c" \
                and len(collection) > 0 \
                and file_arg == "-f" \
                and filename == valid_filename(filename):
            print("pouet")
            json_to_mongo(collection, database, filename)
        else:
            print(help_message)
    else:
        print(help_message)


def valid_filename(filename):
    try:
        validate_filename(filename)
        return filename
    except ValidationError:
        return sanitize_filename(filename)


cli_parse()
