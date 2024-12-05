import boto3
from decouple import config
from uuid import uuid4
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
                }
            ],
            TableName = 'product',  # Name of the table
            KeySchema = [
                {
                    'AttributeName': 'id',  # Partition key
                    'KeyType': 'HASH'       # HASH -> partition key
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


def bulk_insert(products,city,zipcode):
    # Reference the DynamoDB table
    table = resource.Table('product')

    # Using batch_writer to insert multiple items at once
    with table.batch_writer() as writer:
        for product in products:
            writer.put_item(Item={
                'id': str(uuid4()),  # Generate a unique ID for each product
                'product_name': product['product_name'],
                'product_category': product['product_category'],
                'product_count': product['product_count'],
                'product_price': product['product_price'],
                'expiry_date': product['expiry_date'],
                'estimated_shelf_life': product['estimated_shelf_life'],
                'city': city,
                'zipcode': zipcode
            })
    

def fetch_all_products():
    # Reference the DynamoDB table
    table = client.Table('product')

    # Scan the table to get all items
    response = table.scan()

    # Get the list of items
    products = response.get('Items', [])

    # Handling pagination if more items exist
    while 'LastEvaluatedKey' in response:
        # Continue scanning to get the next set of results
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        products.extend(response.get('Items', []))

    return products

