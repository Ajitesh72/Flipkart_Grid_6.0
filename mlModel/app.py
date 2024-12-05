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



def get_location_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="atharvasankhe12@gmail.com")
    location = geolocator.reverse((latitude, longitude), language='en')
    if location:
        return location.address
    return "Location not found"

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'images')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Function to check allowed image extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return jsonify({"message": "Flask is running"})

@app.route('/api/v1/analyze_product_details', methods=['POST'])
def analyze_product_details():
    data = request.get_json()
    if 'image' in request.json:
        # Handle base64 image
        print("hi")
        image_data = request.json['image']
        image_data = image_data.split(',')[1]  # Strip off data URL part
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        
        # Save the image
        imgId = str(uuid.uuid4())
        filename = imgId+'.png'  # You can generate a unique name or use timestamps
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        located = request.json['location']
        print(f"Image saved successfully at {filepath}")
        print(f"Location: {located}")
        location = get_location_from_coordinates(located.get('latitude'),located.get('longitude'))
        
        print(location)
        location_parts = location.split(',')
        exactLocation = [part.strip() for part in location_parts[-4:]]
        # city = location_parts[-4].strip()
        zipcode = location_parts[-2].strip()
        city = location_parts[-4].strip()
        print(city)
        # pincode = location_parts[-2].strip()
        # country = location_parts[-1].strip()
        # with open(filepath, 'rb') as f:
        #     image_data = f.read()
        
        


        # Prepare the prompt and send the image to the Gemini API
        # prompt = "This image contains packaged products.Please analyze the image and provide:for each product:1)Product Name: 2)Product Category 3)Product Quantity 4)Product Count 5)Expiry Date (if available) 6)Freshness Index (based on visual cues) 7)Estimated Shelf Life 8) If there are multiple products,give answer for each"
        prompt = """This image contains packaged products. Please analyze the image and provide the details for each product in the following structured format:
        {
            "product_name": "<Product Name (if available or mention 'NULL' in the value)>>",
            "product_category": "<Product Category (if available or mention 'NULL' in the value)>>",
            "product_count": "<Product Count (if available or mentiod '1' in the value)>>",
            "product_prcie": "<Product Price (if available or mention 'NULL' in the value)>",
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
        # print(result.text)
        json_string_cleaned = result.text.strip().replace("```json", "").replace("```", "").strip()
        ans = json.loads(json_string_cleaned)
        print(ans)


        # parsed_data = json.loads(result.text)




        response = dynamodb.bulk_insert(ans,city,zipcode)
        # print(f"DynamoDB response: {response}")  

        return jsonify({
            'message': f'Image saved successfully at {filepath}',
            'location':  [city, zipcode]
        })



    return jsonify({'error': 'No image provided'}), 400

if __name__ == '__main__':
    # dynamodb.CreatATableProduct()
    app.run(debug=True,port=8000)
