import boto3

#this dictionary is used to match the hostname to the Octopus Env
def ssmsendcommand(instance):
    env = {
        'hostname prefix' : 'environment in Octopus'
    }
    for k, v in env.items():
        if k in instance:
            environment = v

    ssm = boto3.client('ssm')
    command = ssm.send_command( 
        InstanceIds=[
            # 'this instanceID will accept your runcommand command',
        ],
        DocumentName='AWS-RunPowerShellScript',
        Comment='Restarting IIS Services on {}'.format(instance),
        Parameters={
            'commands': [
                # the below powershell only works with Octopus deploy.  You must create a job in Octopus that ResetsIIS services for hosts
                #'.\Octo deploy-release --project "IISReset" --releaseNumber 0.0.1 --guidedfailure=FALSE --server "serverURLhere" --apiKey "OctopusAPI Key here" --deployto {} --specificmachines={}'.format(environment, instance) #--deploytto is the Octopus Env. 
            ],
            'workingDirectory': [
                'C:\OctopusTools', 
            ]
        },
    )
    print(command)
    return
