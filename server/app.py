from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64
import os
import uuid
import awsDynamo as dynamodb
from geopy.geocoders import Nominatim
import google.generativeai as genai
import httpx
import base64
from decouple import config
import json
import typing_extensions as typing
import PIL.Image
import ssl
import certifi
import logging
app = Flask(__name__)
CORS(app)

class Product(typing.TypedDict):
    product_name: str
    product_category: str
    product_count: str
    product_price: str
    expiry_date: str
    estimated_shelf_life: str

model = genai.GenerativeModel("gemini-1.5-pro-latest")
GOOGLE_API_KEY=config("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
logging.basicConfig(level=logging.INFO)


def get_location_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="atharvasankhe12@gmail.com", ssl_context=ssl.create_default_context(cafile=certifi.where()))
    location = geolocator.reverse((latitude, longitude), language='en')
    if location:
        return location.address
    return "Location not found"
required_product_fields = ["product_name", "product_category", "product_count", "product_price", "expiry_date", "estimated_shelf_life"]
required_food_fields = ["food_name", "food_category", "food_count", "food_price", "freshness", "estimated_shelf_life"]
def add_missing_fields(data, required_fields):
    fixed_data = []

    for item in data:
        fixed_item = item.copy()
        print()
        
        for field in required_fields:
            if field not in fixed_item:  # Add missing fields with value "NULL"
                fixed_item[field] = "NULL"
        fixed_data.append(fixed_item)
        print("fixed_item", fixed_item)
    return fixed_data

@app.route('/')
def home():
    return jsonify({"message": "Flask is running"})

@app.route('/api/v1/analyze_product_details', methods=['POST'])
def analyze_product_details():
    # try:
    data = request.get_json()
    if 'image' in request.json:
        logging.info(GOOGLE_API_KEY)
        # Handle base64 image
        image_data = request.json['image']
        image_data = image_data.split(',')[1]  # Strip off data URL part
        image = Image.open(BytesIO(base64.b64decode(image_data)))




        located = request.json['location']
        print(f"Location: {located}")
        location = get_location_from_coordinates(located.get('latitude'),located.get('longitude'))
        location_parts = location.split(',')
        zipcode = location_parts[-2].strip()
        city = location_parts[-4].strip()
        logging.info(city)


        # model part
        prompt = """This image contains packaged products. Please analyze the image and provide the details for each product in the following structured format:
        {
            "product_name": "<Product Name (if available or mention 'NULL' in the value)>>",
            "product_category": "<Product Category (if available or mention 'NULL' in the value)>>",
            "product_count": "<Product Count (if available or mentiod '1' in the value)>>",
            "product_price": "<Product Price (if available or mention 'NULL' in the value)>",
            "expiry_date": "<Expiry Date (if available or mention 'NULL' in the value)>",            
            "estimated_shelf_life": "<Estimated Shelf Life if available or mentioned 'NULL' in the value>"
        }
        If there are multiple products, provide the details for each product as separate objects in an array.
        For example:
        [
            {
                "product_name": "Apple",
                "product_category": "Fruit",
                "product_count": '5',
                "product_price": 10,
                "expiry_date": "null",
                "estimated_shelf_life": "2 weeks"
            },
            {
                "product_name": "Milk",
                "product_category": "Dairy",
                "product_count": '1',
                "product_price": null,
                "expiry_date": "2024-12-15",
                "estimated_shelf_life": "1 week"
            }
        ]
        If some details are not mentioned then return "null" in the value 
        """
        result = model.generate_content(
        [prompt, image]
            #     generation_config=genai.GenerationConfig(
            #     response_mime_type="application/json", response_schema=list[Product]
            # ),
        )
        json_string_cleaned = result.text.strip().replace("```json", "").replace("```", "").strip()
        ans = json.loads(json_string_cleaned)
        ans = add_missing_fields(ans, required_product_fields)
        logging.info(ans)
        date = "NA"
        time = "NA"
        if "date" in request.json:
            date = request.json["date"]
        if "time" in request.json:
            time = request.json["time"]
        #send to dynamodb
        dynamodb.bulk_insert_product(ans, city, zipcode, date, time)
        return jsonify(ans)

    return jsonify({'error': 'No image provided'}), 400
    # except:
    #     return jsonify({'error': 'Some error occured. please try again!'}), 402


@app.route('/api/v1/analyze_freshness', methods=['POST'])
def analyze_freshness():
    data = request.get_json()
    # try:
    if 'image' in request.json:
        
        # Handle base64 image
        image_data = request.json['image']
        image_data = image_data.split(',')[1]  # Strip off data URL part
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        



        located = request.json['location']
        print(f"Location: {located}")
        location = get_location_from_coordinates(located.get('latitude'),located.get('longitude'))
        location_parts = location.split(',')
        zipcode = location_parts[-2].strip()
        city = location_parts[-4].strip()
        logging.info(city)


        # model part
        prompt = """This image contains foods or vegeatbles. Please analyze the image and provide the details for each fruit or vegetable in the following structured format:
        {
            "food_name": "<Product Name >>",
            "food_category": "<Product Category >>",
            "food_count": "<Product Count (count the number of item for eg. "2" if two fresh apple)>>",
            "food_price": "<Product Price (if available or mention 'NULL' in the value)>",
            "freshness": "<Freshnes of food (High, Good,Medium,Poor) (to be estimated by analyzing the image and condition of food)>",            
            "estimated_shelf_life": "<Estimated Shelf Life if available or mentioned 'NULL' in the value>"
        }
        If there are multiple products, provide the details for each product as separate objects in an array.
        For example:
        [
            {
                "food_name": "Apple",
                "food_category": "Fruit",
                "food_count": '5',
                "food_price": "NULL",
                "freshness": "High",
                "estimated_shelf_life": "2 weeks"
            },
            {
                "food_name": "Carrot",
                "food_category": "Vegetable",
                "food_count": '2',
                "food_price": "NULL",
                "freshness": "Good",
                "estimated_shelf_life": "1 week"
            },
            {
                "food_name": "Apple",
                "food_category": "Fruit",
                "food_count": '2',
                "food_price": "NULL",
                "freshness": "Poor",
                "estimated_shelf_life": "0 weeks"
            }
        ]
        If some details are not mentioned then return "null" in the value 
        """
        result = model.generate_content(
        [prompt, image]
            #     generation_config=genai.GenerationConfig(
            #     response_mime_type="application/json", response_schema=list[Product]
            # ),
        )
        json_string_cleaned = result.text.strip().replace("```json", "").replace("```", "").strip()
        ans = json.loads(json_string_cleaned)
        ans = add_missing_fields(ans, required_food_fields)
        logging.info(ans)
        date = "NA"
        time = "NA"
        if "date" in request.json:
            date = request.json["date"]
        if "time" in request.json:
            time = request.json["time"]
        #send to dynamodb
        print(date, time)
        dynamodb.bulk_insert_food(ans, city, zipcode, date, time)
        return jsonify(ans)
    else:
        return jsonify({'error': 'No image provided'}), 400
    # except:
    #     return jsonify({'error': 'Some error occured. please try again!'}), 402

@app.route('/api/v1/get_product_details', methods=['GET'])
def get_product_details():
    response = dynamodb.fetch_all_products()
    
    if response["error"] == False:
        return jsonify(response['data'])
    else:
        return jsonify({"message": "some error occured"})
    
@app.route('/api/v1/get_food_details', methods=['GET'])
def get_food_details():
    response = dynamodb.fetch_all_foods()
    if response["error"] == False:
        return jsonify(response['data'])
    else:
        return jsonify({"message": "some error occured"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
