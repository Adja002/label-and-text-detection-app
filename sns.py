#Adja Gueye s2110852

import boto3

def create_sns_topic():
    try:
        # Create SNS client
        sns_client = boto3.client('sns')
        
        # Create SNS topic
        topic_response = sns_client.create_topic(Name='EmailNotifications-s2110852')
        
        # Get the ARN of the newly created topic
        topic_arn = topic_response['TopicArn']
        
        # Subscribe email endpoint to the topic
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint='a.gueye@alustudent.com'
        )
        
        print("SNS Topic ARN:", topic_arn)
        
        return topic_arn
        
    except Exception as e:
        print("An error occurred while creating SNS topic:", e)
        return None

if __name__ == "__main__":
    create_sns_topic()
