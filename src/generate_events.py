import boto3
import json
import time
import uuid
import random

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dotenv import dotenv_values

from utils import event_types, event_subtypes

config = dotenv_values(".env")

kinesis_client = boto3.client('kinesis', 
                              aws_access_key_id=config['aws_access_key_id'], 
                              aws_secret_access_key=config['aws_secret_access_key'], 
                              region_name=config['region_name'])


def send_events_to_kinesis(num_events, sleep_time):
    for event in range(num_events):
        event_data = generate_event()
        resp = kinesis_client.put_record(StreamName='kinesis-datastreams-demo',
                                  Data=event_data,
                                  PartitionKey="partitionKey")
        print(f"send event {event}", event_data, resp)
        time.sleep(sleep_time)

def generate_event():
    event = {
        "event_uuid": str(uuid.uuid4()),
        "event_name": f"{random.choice(event_types)}:{random.choice(event_subtypes)}",
        "created_at": int(time.time()),
    }
    return json.dumps(event)

def generate_mock_data():
    events = [
        {
        "event_uuid": str(uuid.uuid4()),
        "event_name": f"{random.choice(event_types)}:{random.choice(event_subtypes)}",
        "created_at": int(time.time()),
    } for _ in range(10)
    ]
    
    with open("events_10.json", "w") as f:
        json.dump(events, f)
    
    # table = pa.Table.from_pandas(df)
    # pq.write_table(table, 'event.parquet')
    # df.to_json("events_1000000.json", orient='records', lines=True)

if __name__ == "__main__":
    events_per_hour = 1000000
    sleep_time = 3600 / events_per_hour
    while True:
        send_events_to_kinesis(events_per_hour, sleep_time)
    
    # generate_mock_data()
