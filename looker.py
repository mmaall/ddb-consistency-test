import boto3
import sys
import decimal
import threading 
from datetime import datetime, timedelta 

def main(args: list):

    max_test_duration = 60
    read_count = 3
    record_size_kb = 100
    kb_size = 1024

    if len(args) < 1:
        print("Please include the table name as the first argument")
        exit()

    table_name = args[0]

    ddb_table = boto3.resource("dynamodb").Table(table_name)

    count = 0 
    junk_text = "a" * (int(kb_size*record_size_kb/sys.getsizeof("a")))

 
    ddb_key = "key"
    start_time = datetime.now()

    current_time = datetime.now()

    max_elapsed_time = timedelta(seconds = max_test_duration)

    while current_time - start_time < max_elapsed_time:

        # Write the counter
        write_response = ddb_table.put_item(
            Item = {
                "pk" : ddb_key,
                "counter" : count,
                "junk" : junk_text
            }
        )
        
        print("{} written to {}".format(count, ddb_key))
        # Iterate and write

        count +=1 
        write_response = ddb_table.put_item(
            Item = {
                "pk" : ddb_key,
                "counter" : count,
                "junk" : junk_text
            }
        )
        print("{} written to {}".format(count, ddb_key))

        # Read 3 times

        print ("reading from ddb")

        threads = []
        for i in range(read_count):
            thread = threading.Thread(target = get_ddb_value, args = (ddb_table, ddb_key, count))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        current_time = datetime.now()

def get_ddb_value(client, key, count):
    
    read_counter = client.get_item(
        Key = {
            "pk" : key
        },
        ConsistentRead = False 
    )["Item"]["counter"]

    read_counter = replace_decimals(read_counter)

    if read_counter != count:
        print("INCONSISTENT READ!!! Read {}, counter is {}".format(read_counter, count))

# Dynamodb does not play nice with ints and python 
def replace_decimals(obj):
    if isinstance(obj, list):
        for i in xrange(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.iterkeys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


if __name__ == "__main__":
    main(sys.argv[1:])    
