# Label and Text Detection Application on AWS

This project demonstrates the implementation of a Label and Text Detection system using AWS Rekognition for image analysis. 

## Features

- **Resource Creation with Boto3 and CloudFormation**
  - Python (Boto3) scripts are used to provision an EC2 instance and an S3 bucket.
  - SQS queue and DynamoDB table are created using CloudFormation templates.

- **Image File Upload to S3 and Lambda Trigger from SQS**
  - Image files are uploaded to S3 from the EC2 instance at regular intervals.
  - Uploads trigger messages to an SQS queue, which in turn triggers a Lambda function.

- **Label and Text Detection with AWS Rekognition**
  - Lambda function (Python with Boto3) extracts image details from SQS messages.
  - Uses AWS Rekognition to detect labels (vehicle identification) and extract plate numbers.

- **Database Update and Email Notification**
  - DynamoDB stores image metadata and detection results.
  - Sends email notifications (to a specified email) for blacklisted vehicles or no records found.

## Implementation Details

- **EC2 Instance**: Simulates a camera system, providing images for label and text detection.
- **AWS Services**: Uses Boto3 SDK for Python to interact with AWS services programmatically.

## Requirements
- Python 3.x
- AWS Account with appropriate permissions
- Boto3 library
- AWS CLI configured with credentials

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Adja002/label-and-text-detection-app.git
   cd label-and-text-detection-app
2. **Install dependencies:**
   ```bash
   pip install boto3
3. **Set up AWS credentials:**
   ```bash
   aws configure

## Contributing
Contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.


