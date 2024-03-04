import base64
import json
from datetime import datetime

from pydantic import TypeAdapter

from utils import Pipeline
from model import Event


def lambda_handler(event, context):
    print(f"Recieved event {event}")
    if 'records' in event:
        output = []
        uuid_cache = {}

        for record in event['records']:
            print(record['recordId'])
            payload = json.loads(base64.b64decode(record['data']).decode('utf-8'))

            for event in payload:
                if not uuid_cache.get(event["event_uuid"]):
                    try:
                        TypeAdapter(Event).validate_json(event)
                        
                        event["event_uuid"] = True
                        event["created_datetime"] = datetime.utcfromtimestamp(event["created_at"])
                        event["event_type"] = event["event_name"].split[":"][0]
                        event["event_subtype"] = event["event_name"].split[":"][1]
                
                        output_record = {
                            'recordId': record['recordId'],
                            'result': 'Ok',
                            'data': base64.b64encode(event.encode('utf-8')).decode('utf-8')
                        }
                        output.append(output_record)
                    except Exception as e:
                        print(f"could not transform event: {e}")


        return {'records': output}

    elif event.get("job_name") == "analytical_pipeline":
        Pipeline.run_analytical_pipeline()
    else:
        print(f"unknown event {event}")
