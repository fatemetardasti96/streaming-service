from io import BytesIO
import pytz
from datetime import datetime, timedelta
import boto3
import json
from uuid import uuid4

import pandas as pd
from dotenv import dotenv_values
import pandas as pd

event_types = ['lesson', 'account', 'session', 'payment', 'purchase', 'login', 'logout', 'signup', 'comment', 'review']
event_subtypes = ['created', 'started', 'done', 'canceled', 'failed']
config = dotenv_values(".env")
  

class Pipeline:
    def __init__(self) -> None:
        self.s3_client = boto3.client('s3', aws_access_key_id=config['aws_access_key_id'], 
                                            aws_secret_access_key=config['aws_secret_access_key'], 
                                            region_name=config['region_name'])
    
    def upload_parquet_to_s3(self, df: pd.DataFrame, filepath: str):
        out_buffer = BytesIO()
        df.to_parquet(out_buffer, index=False)
        self.s3_client.put_object(Bucket='babbel-analytical-bucket-76549876', Key=filepath, Body=out_buffer.getvalue())
    
      
    def run_analytical_pipeline(self):
        date = (datetime.today() - timedelta(1))

        prefix = f"events/year={date.strftime('%Y')}/month={date.strftime('%m')}/day={date.strftime('%d')}/"

        result = self.s3_client.list_objects(Bucket='babbel-events-bucket-76549876', Prefix=prefix)
        df = pd.DataFrame()
        
        for content in result['Contents']:
            response = self.s3_client.get_object(Bucket='babbel-events-bucket-76549876', Key=content['Key'])
        
            json_event = json.loads(response['Body'].read().decode('utf-8'))
            
            if len(df) < 1000000:
                df = pd.concat([df, pd.DataFrame(json_event)], ignore_index=True)
            else:
                self.upload_parquet_to_s3(df=df, filepath=f"{prefix}{uuid4()}.parquet")        
                df = pd.DataFrame()      
            