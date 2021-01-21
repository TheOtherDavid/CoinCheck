import os
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key


class PriceStorageDA:

    def savePrice(self, time, product_code, price):
        dynamodb = self.getDB()

        table = dynamodb.Table("PRC")
        price_record = {
            "DTM": str(time),
            "PD_ID": product_code,
            "PRC": price
        }
        table.put_item(Item=price_record)

    def getPrices(self, product_code):
        now = datetime.now(None)
        six_hours_ago = datetime.now(None) - timedelta(hours=6)

        dynamodb = self.getDB()
        table = dynamodb.Table("PRC")
        response = table.query(
            KeyConditionExpression=Key('PD_ID').eq(product_code) & Key('DTM').between(str(six_hours_ago), str(now))
        )
        return response

    def getDB(self):
        # TODO: Make this a singleton, so we don't have to open two connections
        aws_access_key = os.environ.get("aws_access_key")
        aws_secret_key = os.environ.get("aws_secret_access_key")

        dynamodb = boto3.resource('dynamodb',
                                  aws_access_key_id=aws_access_key,
                                  aws_secret_access_key=aws_secret_key,
                                  region_name="us-east-2")
        return dynamodb
