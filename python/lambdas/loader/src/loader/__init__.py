from data_core import process_data

def handler(event, context):
    print("Loader lambda invoked")
    return {
        "statusCode": 200,
        "body": process_data("event data")
    }
