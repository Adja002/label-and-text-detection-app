#Adja Gueye s2110852
import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

try:
    # Table creation
    table = dynamodb.create_table(
        TableName='VehicleTable-s2110852',
        KeySchema=[
            {
                'AttributeName': 'PlateNumber',
                'KeyType': 'HASH' 
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PlateNumber',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='VehicleTable-s2110852')
    print("Table created successfully.")

except Exception as e:
    # Catch any exception that occurs during the table creation
    print(f"An error occurred: {e}")
