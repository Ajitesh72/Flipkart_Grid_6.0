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

def CreatATableFood():
    existing_tables = client.list_tables()['TableNames']
    if 'food' not in existing_tables:
        client.create_table(
            AttributeDefinitions = [
                {
                    'AttributeName': 'id',        # Name of the attribute
                    'AttributeType': 'S'          # N -> Number
                }
            ],
            TableName = 'food',  # Name of the table
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

    table = resource.Table('food')
    table.meta.client.get_waiter('table_exists').wait(TableName='food')
    print("Table is now active.")

# def addproductToTable(id, location):
#     productTable = resource.Table('product')
#     response = productTable.put_item(
#         Item = {

#             'id':id,
#             'location'  : location,
            
#         }
#     )
#     return response


def bulk_insert_product(products,city,zipcode):
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
    return "success"

def bulk_insert_food(foods,city,zipcode):
    # Reference the DynamoDB table
    table = resource.Table('food')

    # Using batch_writer to insert multiple items at once
    with table.batch_writer() as writer:
        for food in foods:
            writer.put_item(Item={
                'id': str(uuid4()),  # Generate a unique ID for each product
                'food_name': food['food_name'],
                'food_category': food['food_category'],
                'food_count': food['food_count'],
                'food_price': food['food_price'],
                'freshness': food['freshness'],
                'estimated_shelf_life': food['estimated_shelf_life'],
                'city': city,
                'zipcode': zipcode
            })
    return "success"
    
def fetch_all_products():
    result = {
        "error": False,
        "data": [], 
    }
    try:
        # Reference the DynamoDB table
        table = resource.Table('product')

        # Scan the table to get all items
        response = table.scan()

        # Get the list of items
        products = response["Items"]

        # Handling pagination if more items exist
        while 'LastEvaluatedKey' in response:
            # Continue scanning to get the next set of results
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            products.extend(response["Items"])
        result["error"] = False
        result['data'] = products
        return result
    except Exception as e:
        print(f"Error fetching data: {e}")
        result['error'] = True
        result['data'] = []
        return result
    
def fetch_all_foods():
    result = {
        "error": False,
        "data": [], 
    }
    try:
        # Reference the DynamoDB table
        table = resource.Table('food')

        # Scan the table to get all items
        response = table.scan()

        # Get the list of items
        foods = response["Items"]

        # Handling pagination if more items exist
        while 'LastEvaluatedKey' in response:
            # Continue scanning to get the next set of results
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            foods.extend(response["Items"])
        result["error"] = False
        result['data'] = foods
        return result
    except Exception as e:
        print(f"Error fetching data: {e}")
        result['error'] = True
        result['data'] = []
        return result


