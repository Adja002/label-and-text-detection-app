#Adja Gueye s2110852

import boto3
import time
import os

def upload_images_to_s3(bucket_name, image_files, queue_url):
    region_name = 'us-east-1'  
    s3 = boto3.client('s3', region_name=region_name)
    sqs = boto3.client('sqs', region_name=region_name)
    
    for image_file in image_files:
        try:
            s3.upload_file(image_file, bucket_name, os.path.basename(image_file))  
            print("Uploaded {} to {}".format(image_file, bucket_name))
            
            # Send a message to the SQS queue
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=os.path.basename(image_file)
            )
            print("Sent message to SQS queue for {}".format(image_file))
            
        except Exception as e:
            print("Error uploading {} or sending message to SQS: {}".format(image_file, e))
        
        time.sleep(30) # Wait for 30 seconds before uploading the next image

if __name__ == "__main__":
    # Specify the arguments
    bucket_name = "my.s2110852.bucket"
    image_files = [
        "/home/ec2-user/IMG_20240212_125129.jpg",
        "/home/ec2-user/IMG_20240212_151946.jpg",
        "/home/ec2-user/IMG_20240212_151830.jpg",
        "/home/ec2-user/IMG_20240212_152041.jpg"
    ]  # Images path
    queue_url = "https://sqs.us-east-1.amazonaws.com/938556099999/my-queue-s2110852" 
    
    upload_images_to_s3(bucket_name, image_files, queue_url)
