import boto3
import json

client = boto3.client('dynamodb')

def put(email, body):
  new = ""
  i = 1
  while i < len(body) - 1:
    if body[i] == "\\":
      print(body[i:i+5])
      if body[i+1] == "n":
        print("here")
        i += 1
    else:
      new += body[i]
    i += 1
  data = client.put_item(
    TableName='individualTrees',
    Item={
        'email': {
          'S': email
        },
        'tree': {
          'S': new
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
  
def getDefaultTree():
  return {'Item': {'email': {'S': 'ai974@nyu.edu'}, 'tree': {'S': '{ "class": "",  "nodeDataArray": [{"key":1,"name":"Stella Payne Diaz","title":"CEO"},{"name":"(new person)","title":"","comments":"","parent":1,"key":2},{"name":"(new person)","title":"","comments":"","parent":2,"key":3},{"name":"(new person)","title":"","comments":"","parent":2,"key":4}],  "linkDataArray": [{"from":1,"to":2},{"from":1,"to":3},{"from":2,"to":4}]}'}}, 'ResponseMetadata': {'RequestId': 'T8SSG3LCNS2KGAVFV1GNNEK9QRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 17 Jul 2022 03:17:15 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '528', 'connection': 'keep-alive', 'x-amzn-requestid': 'T8SSG3LCNS2KGAVFV1GNNEK9QRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '1270102284'}, 'RetryAttempts': 0}}
  
def get(email):
  data = client.get_item(
    TableName='individualTrees',
    Key={
      'email': {
        'S': email
      }
    }
  )
  print(f"data:{data}")
  if "Item" not in data:
    data = getDefaultTree()

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
      body = event["body"]
      response = put(email, body)
      print(f"put: {response}")
      return response
    else:
      print("error: neither put nor get")
