#Adja Gueye s2110852
import boto3
import json
import os
import re

# Initialize DynamoDB, Textract, and SNS clients
dynamodb = boto3.client('dynamodb')
textract = boto3.client('textract')
sns = boto3.client('sns')

def lambda_handler(event, context):
    print(f'event: {event}')
    try:
        # Assuming the S3 bucket name and object key are known
        s3_bucket = os.environ['S3_BUCKET_NAME'] 
        image_file = event['Records'][0]['body']
    
        print(f"Image file name: {image_file}")
        
        # Initialize Rekognition client
        rekognition = boto3.client('rekognition')
        
        # Detect labels in the image using Rekognition
        rekognition_response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': image_file
                }
            },
            MaxLabels=10, 
            MinConfidence=80 
        )
        
        # Extracting relevant details from Rekognition response
        labels_with_confidence = [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in rekognition_response['Labels']]
        
        # Filter labels to only include vehicle types (car or van)
        vehicle_types = ['car', 'van']
        filtered_labels = [label['Name'] for label in labels_with_confidence if label['Name'].lower() in vehicle_types]
        
        # Extract confidence scores into a separate list
        confidence_scores = list({str(label['Confidence']) for label in labels_with_confidence}) 
        
        # Initialize Textract client
        # Use Textract to detect text in the image
        textract_response = textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': image_file
                }
            }
        )
        
        # Extracting relevant details from Textract response
        text_blocks = [block['Text'] for block in textract_response['Blocks'] if block['BlockType'] == 'LINE']
        
        # Concatenate text blocks into a single string
        full_text = ' '.join(text_blocks)
        
        # Regular expression for license plate number detection
        plate_number_pattern = re.compile(r'\b\d{4,5} [A-Z]{2} \d{1,2}|\b\d{4,5} [A-Z]{2}|\b\d{4,5}\b|\b\d{1,4} [A-Z]{2} \d{1,2}')
        
        # Find all matches of the pattern in the text
        matches = plate_number_pattern.findall(full_text)
        
        # If no plate numbers are detected, use the previous method to search for single plate number
        if not matches:
            plate_number_pattern = re.compile(r'\b\d+[A-Z]+\d+\b', re.IGNORECASE)
            match = plate_number_pattern.search(full_text)
            if match:
                matches.append(match.group())
        
        # Constructing the item to be put into DynamoDB
        dynamodb_item = {
            'id': {'S': image_file}, # Use the image_file as the id
            'labels': {'SS': filtered_labels}, # Use filtered labels
            'confidence_scores': {'NS': confidence_scores}, # Separate attribute for confidence scores
            'plate_numbers': {'SS': matches} if matches else {'NULL': True}
        }
        
        # Writing the item to DynamoDB
        dynamodb.put_item(
            TableName='my-table1-s2110852',
            Item=dynamodb_item
        )
        
        # Check the vehicle table for whitelist/blacklist status
        for plate_number in matches:
            vehicle_response = dynamodb.get_item(
                TableName='VehicleTable-s2110852', 
                Key={
                    'PlateNumber': {'S': plate_number} 
                }
            )
            if 'Item' in vehicle_response:
                vehicle_status = vehicle_response['Item']['Status']['S']
                if vehicle_status == 'blacklisted':
                    # Send an email notification
                    sns.publish(
                        TopicArn='arn:aws:sns:us-east-1:938556099999:EmailNotifications-s2110852', 
                        Message=f"Vehicle with plate number {plate_number} blacklisted detected.",
                        Subject='[URGENT]Security Alert: Blacklisted Vehicle Detected'
                    )
                else:
                    print(f"Vehicle with plate number {plate_number} is whitelisted.")
            else:
                # Vehicle not found in the table, send an email notification
                sns.publish(
                    TopicArn='arn:aws:sns:us-east-1:938556099999:EmailNotifications-s2110852', 
                    Message=f"Vehicle with plate number {plate_number} not found in the database.",
                    Subject='Security Alert: Unknown Vehicle Detected'
                )
        
        # Constructing the response to be sent
        response_data = {
            'statusCode': 200,
            'body': json.dumps({
                'image_file': image_file,
                'labels': filtered_labels, 
                'confidence_scores': confidence_scores, 
                'plate_numbers': matches
            })
        }
        
        return response_data
        
    except Exception as e:
        print(f"Error processing image: {e}")
        # Constructing the error response to be sent
        error_response = {
            'statusCode': 500,
            'body': json.dumps('Error processing image')
        }
        return error_response
