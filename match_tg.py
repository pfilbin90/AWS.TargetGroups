import boto3
import find_tgs
import json, sys, time
from runcommand import ssmsendcommand

instance_names = sys.argv[1]
names = instance_names.lower

def change_name(instname):
    ec2 = boto3.client('ec2')
    response = ec2.describe_tags(
        Filters=[
        {
         'Name': 'tag:Name',
         'Values': [instname]
        }
        ]
    )
    return response

def get_instance_id(instname):
    dictionary = change_name(instname)
    if 'Tags' in dictionary:
        items = dictionary['Tags']

        for item in items:
            if "i-" in item['ResourceId']:
                instanceid = (item['ResourceId'])
    return instanceid

def get_instance_name(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_tags(
        Filters=[
        {
         'Name': 'resource-id',
         'Values': [instance_id,]
        },
        ]
        )

    for tag in response["Tags"]:
      if tag['Key'] == 'Name':
        inst_name = tag['Value']
    return inst_name

def open_arn(arn):
    client = boto3.client('elbv2')
    response = client.describe_target_health(
            TargetGroupArn=arn,
    )
    return response

def deregister_targets(x, y):
    client = boto3.client('elbv2')
    response = client.deregister_targets(
        TargetGroupArn=x,
        Targets=[
            {
                'Id': y
            },
        ]
    )
    print(response)

def register_targets(x, y):
    client = boto3.client('elbv2')
    response = client.register_targets(
        TargetGroupArn=x,
        Targets=[
            {
                'Id': y
            },
        ]
    )
    print(response)

def draining(arn):
    item = open_arn(arn)
    dump = json.dumps(item)
    data = json.loads(dump)
    if 'TargetHealthDescriptions' in data:
        items = data['TargetHealthDescriptions']

        for item in items:
            if 'TargetHealth' in item:
                state = item['TargetHealth']['State']
                if str(state) is 'draining':
                    return True
                else:
                    return False


instname_list = []
for item in names.split(','):
   instname_list.append(item)

instanceid_list = []
for instname in instname_list:
    instanceid_list.append(get_instance_id(instname))
#python3 leftover_list = instanceid_list.copy()
leftover_list = list(instanceid_list)

tg_list = find_tgs.tg_arns()
arn_list= []
id_list = []

for arn in tg_list:
    item = open_arn(arn)
    dump = json.dumps(item)
    data = json.loads(dump)

    if 'TargetHealthDescriptions' in data:
        items = data['TargetHealthDescriptions']

        for item in items:
            if 'Target' in item:
                target = item['Target']['Id']
                if target in instanceid_list:
                    leftover_list.remove(target)
                    ## uncomment below if not using Jenkins
                    # print(get_instance_name(target) + " belongs to target group:")
                    # print(arn)
                    arn_list.append(arn)
                    id_list.append(target)
for item in leftover_list:
    print(get_instance_name(item) + " does not belong to any target groups")

for x, y in zip(arn_list, id_list):
    deregister_targets(x, y)
    while draining(x) is True:
        time.sleep(10)
    time.sleep(75)
    ssmsendcommand(get_instance_name(y))
    time.sleep(75)
    register_targets(x, y)
    time.sleep(25)
