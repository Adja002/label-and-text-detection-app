#Adja Gueye s2110852

import boto3

# Function to create my EC2 instance 
def create_ec2_instance(instance_name):
    try:
        # Create my EC2 client using boto3
        ec2 = boto3.client('ec2')
        
        # Run instance with parameters below
        response = ec2.run_instances(
            ImageId='ami-08e4e35cccc6189f4', # AMI ID for the instance
            InstanceType='t2.micro', # Instance type
            MaxCount=1, # Maximum number of instances to launch
            MinCount=1, # Minimum number of instances to launch
            KeyName='vockey', # Key pair name for SSH access
            TagSpecifications=[
                {
                    'ResourceType': 'instance', 
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name 
                        },
                    ]
                },
            ],
        )

        # Extract the instance ID from the response
        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 instance {instance_name} created with Instance ID: {instance_id}")

    except Exception as e:
        # Catch any exceptions that occur during the instance creation process
        print(f"An error occurred while creating the EC2 instance: {e}")

# Main execution block
if __name__ == "__main__":
    # The name of my instance with my student ID
    instance_name = "MyEC2.s2110852"
    
    # Call the function to create the EC2 instance
    create_ec2_instance(instance_name)
