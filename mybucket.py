# Adja Gueye s2110852

import boto3

# Function to create my S3 bucket with a specified name
def create_s3_bucket(bucket_name):
    try:
        # Create my S3 client using boto3
        s3 = boto3.client('s3')
        
        # Create the S3 bucket 
        response = s3.create_bucket(
            Bucket=bucket_name, 
        )

        print(f"S3 bucket {bucket_name} created")

    except Exception as e:
        # Catch any exceptions that occur during the bucket creation process
        print(f"An error occurred while creating the S3 bucket: {e}")

# Main execution block
if __name__ == "__main__":
    # The bucket name with my student number
    bucket_name = "my.s2110852.bucket"
    
    # Call the function to create the S3 bucket
    create_s3_bucket(bucket_name)
