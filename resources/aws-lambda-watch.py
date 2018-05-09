# This script is incomplete - needs a proper notification method such as email

import boto3

def lambda_handler(event, context):
    
    cloudwatch = boto3.client('cloudwatch')
    
    paginator = cloudwatch.get_paginator('list_metrics')
    for response in paginator.paginate(Dimensions=[{'Name': 'LogGroupName'}],
                                   MetricName='IncomingLogEvents',
                                   Namespace='AWS/Logs'):
        print(response['Metrics'])

        # TODO: Metrics may indicate a rapid daily increase. Sound alarm if there is one.
        