import boto3
from decouple import config
AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)
resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)


def CreatATableProduct():
    existing_tables = client.list_tables()['TableNames']
    if 'product' not in existing_tables:
        client.create_table(
            AttributeDefinitions = [
                {
                    'AttributeName': 'id',        # Name of the attribute
                    'AttributeType': 'S'          # N -> Number
                },
                {
                    'AttributeName': 'location',  # Name of the second attribute
                    'AttributeType': 'S'          # S -> String (location will be a string)
                }
            ],
            TableName = 'product',  # Name of the table
            KeySchema = [
                {
                    'AttributeName': 'id',  # Partition key
                    'KeyType': 'HASH'       # HASH -> partition key
                },
                {
                    'AttributeName': 'location',  # Sort key
                    'KeyType': 'RANGE'            # RANGE -> sort key
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,  # Set the read capacity units (e.g., 5)
                'WriteCapacityUnits': 5  # Set the write capacity units (e.g., 5)
            }
            
        )

    table = resource.Table('product')
    table.meta.client.get_waiter('table_exists').wait(TableName='product')
    print("Table is now active.")

def addproductToTable(id, location):
    productTable = resource.Table('product')
    response = productTable.put_item(
        Item = {

            'id':id,
            'location'  : location,
            
        }
    )
    return response


