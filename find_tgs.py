import boto3
import os, sys, json

client = boto3.client('elbv2')
response = client.describe_target_groups()

with open('data.json', 'a') as f:
    json.dump(response, f)

def tg_arns():
    tgarn_list = []
    with open("data.json", "r") as y:
        data = json.load(y)
        if 'TargetGroups' in data:
            items = data['TargetGroups']

            for item in items:
                if 'TargetGroupArn' in item:
                    tgarn_list.append(item['TargetGroupArn'])
    y.close()
    os.remove("data.json")

    return tgarn_list