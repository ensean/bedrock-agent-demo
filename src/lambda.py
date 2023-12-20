import json
import boto3

ec2_client = boto3.client('ec2')

def get_named_parameter(event, name):
    return next(item for item in event['parameters'] if item['name'] == name)['value']

def startEc2Instance(event):
    # Extract parameters
    instanceType = get_named_parameter(event, 'instanceType') 
    keyName = get_named_parameter(event, 'keyName')

    # Implement starting EC2 instance
    resp = ec2_client.run_instances(
                ImageId='ami-0de43e61758b7158c',    # refers to amazon linux 2 in oregon
                InstanceType=instanceType,
                KeyName=keyName,
                MaxCount=1,
                MinCount=1
            )

    # Return instance ids
    ids = [x['InstanceId'] for x in resp['Instances']]
    return {
        "instanceIds": ",".join(ids)
    }

def lambda_handler(event, context):

    print(event)

    response_code = 200
    action_group = event['actionGroup']
    api_path = event['apiPath']

    if api_path == '/startEc2Instance':
        result = startEc2Instance(event)
    else:
        response_code = 404
        result = f"Unrecognized api path: {action_group}::{api_path}"

    response_body = {
        'application/json': {
            'body': result 
        }
    }

    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': response_code,
        'responseBody': response_body
    }
    
    api_response = {'messageVersion': '1.0', 'response': action_response}
    return api_response