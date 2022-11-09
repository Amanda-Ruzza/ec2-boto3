import boto3

#Create a variable for the Subnet Name

subnet_name = 'SecurityVPC-subnet-private1-us-east-1a'

ec2_client = boto3.client('ec2')
print('Subnets:')
print('-------')
sn_all = ec2_client.describe_subnets() #this collects all the subnets

for sn in sn_all['Subnets'] :
    try:
        print(sn['Tags'])
        for tag in sn['Tags']:
            if tag['Key']== 'Name': 
                if tag['Value'] == subnet_name:
                    subnet_id = sn['SubnetId']
    except:
        print("No Tags")

print(subnet_name + ":" + subnet_id)


DRYRUN=False #set this to 'true' if you just want to do a dry run and not actually even launch and terminate the instance
ec2_client = boto3.client('ec2')

def Get_Image(ec2_client):
    images = ec2_client.describe_images(    # this command searches for the AMI id inside AWS
        Filters=[
            {
                'Name': 'name',
                'Values':[
                    'ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*',
                ]
            },
            # {'Name': 'owner-alias',
            # 'Values': [
            #     'amazon',
            #     ]
            # },   
        ],
        Owners=['099720109477']
    )
    ec2_image = boto3.resource('ec2')
    AMI = ec2_image.Image(images['Images'][0]['ImageId']) # this command will find the 1st image on the list of available current EC2 image ID's 
    return AMI

def Start_Ec2(AMI, ec2_client):
    if AMI.state == 'available':
        print(AMI.image_id) 
        instance = ec2_client.run_instances(    # this command will create the ec2 instance based on the image ID printed on the previous command
            ImageId=AMI.image_id,
            InstanceType='t2.small',
            MaxCount=1,
            MinCount=1,
            SubnetId=subnet_id,
            DryRun=DRYRUN
        )
        ec2_instance = boto3.resource('ec2')
        ec2 = ec2_instance.Instance(instance['Instances'][0]['InstanceId'])
        return ec2
    else:
        print("The AMI was not available")
        return None

if __name__ == '__main__':
  ec2_client = boto3.client('ec2')
  AMI = Get_Image(ec2_client)
  ec2 = Start_Ec2(AMI=AMI, ec2_client=ec2_client)
  print(ec2.instance_id)
  ec2.wait_until_running()
  print(f"Instance is {ec2.state['Name']}") # the 'state' attribute that lets you know if the EC2 is running or not
  ec2.terminate() # this will trigger the termination of the instance
  ec2.wait_until_terminated()
  print(f"Instance is {ec2.state['Name']}")        
