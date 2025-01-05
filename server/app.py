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
from ultralytics import YOLO
from transformers import AutoModel
app = Flask(__name__)
CORS(app)
yolo_freshness_model = YOLO("../models/best.pt")
model = ''
try:
    model = AutoModel.from_pretrained("../models/qwen_model")
except:
    print()
fruit_vegetable_list = [["fresh", "apple", "fruit"], ["fresh", "banana", "fruit"], ["fresh", "bellpepper", "vegetable"], ["fresh", "carrot", "vegetable"], ["fresh", "cucumber", "vegetable"], ["fresh", "mango", "fruit"], ["fresh", "orange", "fruit"], ["fresh", "potato", "vegetable"], ["rotten", "apple", "fruit"], ["rotten", "banana", "fruit"], ["rotten", "carrot", "vegetable"], ["rotten", "cucumber", "vegetable"], ["rotten", "mango", "fruit"], ["rotten", "orange", "fruit"], ["rotten", "potato", "vegetable"], ["rotten", "tomato", "vegetable"], ["rotten", "bellpepper", "vegetable"]]


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
        date = "NA"
        time = "NA"
        if "date" in request.json:
            date = request.json["date"]
        if "time" in request.json:
            time = request.json["time"]
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
        predictions = yolo_freshness_model.predict(image)[0]
        flag = True
        if len(predictions) == 0:
            flag = False
        for pred in predictions:
            if pred.boxes.conf.item() < 0.5:
                flag = False
                break
        if flag:
            analysed_details_dict = {}
            for pred in predictions:
                freshness_level = ""
                pred_class = pred.boxes.cls.item()
                if pred.boxes.conf.item() > 0.5 and pred.boxes.conf.item() <0.7:
                    freshness_level = "medium"
                else:
                    temp = fruit_vegetable_list[int(pred_class)][0]
                    if temp == "fresh":
                        freshness_level = "high"
                    else:
                        freshness_level = "low"
                predicted_item = fruit_vegetable_list[int(pred_class)][1]
                predicted_class = fruit_vegetable_list[int(pred_class)][2]
                joint_prediction = f"{freshness_level} {predicted_item} {predicted_class}"
                if joint_prediction in analysed_details_dict:
                    analysed_details_dict[joint_prediction] += 1
                else:
                    analysed_details_dict[joint_prediction] = 1
            ans = []
            for key, value in analysed_details_dict.items():
                details = key.split()
                ans.append({
                    "freshness": details[0],
                    "food_price": "NULL",
                    "food_name": details[1],
                    "food_category": details[2],
                    "food_count": value
                })
            ans = add_missing_fields(ans, required_food_fields)
            dynamodb.bulk_insert_food(ans, city, zipcode, date, time)
            return jsonify(ans)
        else:
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
