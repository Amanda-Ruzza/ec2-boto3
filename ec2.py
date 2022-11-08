import boto3

DRYRUN=False #set this to 'true' if you just want to do a dry run and not actually even launch and terminate the instance
ec2_client = boto3.client('ec2')
# this command searches for the AMI id inside AWS
images = ec2_client.describe_images(
    Filters=[
        {
            'Name': 'name',
            'Values':[
                'amzn-ami-hvm*',
            ]
        },
        {'Name': 'owner-alias',
        'Values': [
            'amazon',
            ]
        },
    ],
)
ec2_image = boto3.resource('ec2')
AMI = ec2_image.Image(images['Images'][0]['ImageId']) # this command will find the 1st image on the list of available current EC2 image ID's 

if AMI.state == 'available':
    print(AMI.image_id) 
    instance = ec2_client.run_instances(    # this command will create the ec2 instance based on the image ID printed on the previous command
        ImageId=AMI.image_id,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN
    )
    ec2_instance = boto3.resource('ec2')
    ec2 = ec2_instance.Instance(instance['Instances'][0]['InstanceId'])
    print(ec2.instance_id)
    ec2.wait_until_running()
    print(f"Instance is {ec2.state['Name']}") # the 'state' attribute that lets you know if the EC2 is running or not
    ec2.terminate() # this will trigger the termination of the instance
    ec2.wait_until_terminated()
    print(f"Instance is {ec2.state['Name']}")
else:
    print("The AMI was not available")