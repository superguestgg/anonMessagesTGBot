import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from functools import cache


class RoomsYDBDatabase:
    def __init__(self):
        self.storage_url = os.environ.get('YDB_STORAGE_URL')
        self.ydb_access_key_id = os.environ.get("YDB_ACCESS_KEY_ID")
        self.ydb_secret_access_key = os.environ.get("YDB_SECRET_ACCESS_KEY")

    def set_up(self):
        self.create_table()

    def get_db(self):
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=self.storage_url,
            region_name='global',
            aws_access_key_id=self.ydb_access_key_id,
            aws_secret_access_key=self.ydb_secret_access_key
        )
        return dynamodb

    def delete_table(self):
        dynamodb = self.get_db()
        table = dynamodb.Table('UserRooms')
        table.delete()
        return table

    def create_table(self):
        dynamodb = self.get_db()
        table = dynamodb.create_table(
            TableName='UserRooms',
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'room_name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'room_name',
                    'AttributeType': 'S'
                }
            ]
        )

        return table

    def create_room(self, user_id, room_name, is_public=True, password="", dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()

        table = dynamodb.Table('UserRooms')
        response = table.put_item(
            Item={
                'user_id': str(user_id),
                'room_name': str(room_name),
                'is_public': "1" if is_public else "0",
                'password': str(password)
            }
        )
        return response

    def get_rooms_by_user(self, user_id, dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()
        table = dynamodb.Table('UserRooms')
        try:
            response = table.query(
                KeyConditionExpression=Key('user_id').eq(str(user_id))
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return
        try:
            return response['Items']
        except Exception as e:
            print(e)
            return

    def get_room(self, room_name, dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()
        table = dynamodb.Table('UserRooms')
        try:
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('room_name').eq(room_name)
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return
        try:
            return response['Items']
        except:
            return

    def read_user(self, user_id, dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()
        table = dynamodb.Table('UserRooms')
        try:
            response = table.get_item(Key={'user_id': str(user_id)})
        except ClientError as e:
            print(e.response['Error']['Message'])
            return
        try:
            return response['Item']
        except:
            return

    def read_room_field(self, room_name, field_name, dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()
        table = dynamodb.Table('UserRooms')
        try:
            response = table.get_item(Key={'room_name': str(room_name)})
        except ClientError as e:
            print(e.response['Error']['Message'])
            return
        try:
            return response['Item'][field_name]
        except:
            return

    def read_all_rooms(self, dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()
        table = dynamodb.Table('UserRooms')
        try:
            print(table.item_count)
            response = table.scan()
        except ClientError as e:
            print(e.response['Error']['Message'])
            return
        try:
            return response['Items']
        except:
            return

    def read_user_field(self, user_id, field_name, dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()
        table = dynamodb.Table('UserRooms')
        try:
            response = table.get_item(Key={'user_id': str(user_id)})
        except ClientError as e:
            print(e.response['Error']['Message'])
            return
        try:
            return response['Item'][field_name]
        except:
            return

    def update_room(self, room_name, updates, dynamodb=None):
        print(room_name, updates)
        if not dynamodb:
            dynamodb = self.get_db()

        table = dynamodb.Table('UserRooms')
        response = table.update_item(
            Key={'room_name': str(room_name)},
            AttributeUpdates={update_attr: {"Value": updates[update_attr], "Action": "PUT"}
                              for update_attr in updates}
        )
        return response

    def delete_room(self, user_id, room_name, dynamodb=None):
        if not dynamodb:
            dynamodb = self.get_db()

        table = dynamodb.Table('UserRooms')
        response = table.delete_item(
            Key={
                'user_id': str(user_id),
                'room_name': str(room_name)
            }
        )
        return response

    def is_user2(self, user_id):
        user_rights = self.read_user_field(user_id, "rights")
        return user_rights in {"admin", "user2"}

    def is_admin(self, user_id):
        user_rights = self.read_user_field(user_id, "rights")
        return user_rights == "admin"

    def is_user(self, user_id):
        user = self.read_user(user_id)
        return bool(user)

    def handler(self, event, context):
        dynamodb = self.get_db()
        body = json.loads(event['body'])
        user_data = self.read_user(body['message']['chat']['id'], dynamodb)
        if user_data is None:
            self.create_user(body['message']['chat']['id'], body['message']['from']['first_name'], dynamodb)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'method': 'sendMessage',
                    'chat_id': body['message']['chat']['id'],
                    'text': 'Привет! Я тебя запомнил :)'
                }),
                'isBase64Encoded': False
            }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'method': 'sendMessage',
                'chat_id': body['message']['chat']['id'],
                'text': f'Привет, {user_data["first_name"]}!'
            }),
            'isBase64Encoded': False
        }


if __name__ == "__main__":
    print(RoomsYDBDatabase())
