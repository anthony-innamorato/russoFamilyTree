import boto3
import json

client = boto3.client('dynamodb')

def put():
  data = client.put_item(
    TableName='individualTrees',
    Item={
        'email': {
          'S': 'test2@gmail.com'
        },
        'tree': {
          'S': '{"class": "go.TreeModel", "nodeDataArray": [{"key":1, "name":"Stella Payne Diaz", "title":"CEO"}, {"key":2, "name":"Luke Warm", "title":"VP Marketing/Sales", "parent":1}, {"key":3, "name":"Meg Meehan Hoffa", "title":"Sales", "parent":2}, {"key":4, "name":"Peggy Flaming", "title":"VP Engineering", "parent":1, "comments":"test comment"}]}'
        }
    }
  )

  response = {
    'statusCode': 200,
    'body': 'successfully created item!',
    'headers': {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
  }
  return response
  
def get(email):
  data = client.get_item(
    TableName='individualTrees',
    Key={
      'email': {
        'S': email
      }
    }
  )

  response = {
      'statusCode': 200,
      'body': json.dumps(data),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
  }
  
  return response

def lambda_handler(event, context):
    
    email = event["queryStringParameters"]["email"]
    print(f"event: {event}")
    print(f"email: {email}")
    
    if event["httpMethod"] == "GET":
      item = get(email)
      print(f"item: {item}")
      return item
    elif event["httpMethod"] == "PUT":
      print(f"put: {put()}")
    else:
      print("error: neither put nor get")
