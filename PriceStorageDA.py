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
        alert_target_time = float(os.environ.get("alert_target_time"))
        target_time = datetime.now(None) - timedelta(hours=alert_target_time)

        dynamodb = self.getDB()
        table = dynamodb.Table("PRC")
        response = table.query(
            KeyConditionExpression=Key('PD_ID').eq(product_code) & Key('DTM').between(str(target_time), str(now)),
            ScanIndexForward=False
        )
        return response

    def saveBalance(self, balance_record):
        dynamodb = self.getDB()

        table = dynamodb.Table("PRTFL")

        db_balance_record = {
            "DTM": str(balance_record["time"]),
            "PD_ID": balance_record["currency"],
            "QTY": str(balance_record["balance"]),
            "PRC": str(balance_record["price"]),
            "USD_VAL": str(float(balance_record["balance"]) * float(balance_record["price"])),
            "AVG_PRC": str(balance_record["average_price"])
        }

        table.put_item(Item=db_balance_record)

    def getBalances(self):
        dynamodb = self.getDB()
        table = dynamodb.Table("PRTFL")
        dynamo_response = table.scan()["Items"]
        response = []
        for orig_dict in dynamo_response:
            new_dict = {
                # Leave DTM as a string. May be a bad idea
                "DTM": orig_dict["DTM"],
                "PD_ID": orig_dict["PD_ID"],
                "PRC": float(orig_dict["PRC"]),
                "QTY": float(orig_dict["QTY"]),
                "USD_VAL": float(orig_dict["USD_VAL"])
            }
            response.append(new_dict)

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
