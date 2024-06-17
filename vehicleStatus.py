#Adja Gueye s2110852
import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

def update_vehicle_status(plate_number, image_file, status):
    try:
        # Update the vehicle table with the specified status
        response = dynamodb.put_item(
            TableName='VehicleTable-s2110852',
            Item={
                'PlateNumber': {'S': plate_number}, # Use the plate number as the primary key
                'Status': {'S': status}
            }
        )
        print(f"Vehicle status updated successfully for plate number: {plate_number}")
    except Exception as e:
        # Catch any exception that occurs during the put_item operation
        print(f"An error occurred while updating the vehicle status for plate number {plate_number}: {e}")

# Vehicles Statuses
update_vehicle_status('6585 OC 11', 'IMG_20240212_152041.jpg', 'blacklisted')
update_vehicle_status('106520C22', 'IMG_20240212_125129.jpg', 'blacklisted')
update_vehicle_status('8740 NV 12', 'IMG_20240212_151830.jpg', 'whitelisted')
update_vehicle_status('2547 EZ 16', 'IMG_20240212_151946.jpg', 'whitelisted')
