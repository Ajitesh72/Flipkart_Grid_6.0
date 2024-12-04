from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64
import os
import uuid
from geopy.geocoders import Nominatim
import google.generativeai as genai
import httpx
import base64

app = Flask(__name__)
CORS(app)

model = genai.GenerativeModel("gemini-1.5-flash")
GOOGLE_API_KEY=""
genai.configure(api_key=GOOGLE_API_KEY)


def get_location_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="atharvasankheer@gmail.com")
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
    if 'image' in request.json:
        # Handle base64 image
        print("hi")
        image_data = request.json['image']
        image_data = image_data.split(',')[1]  # Strip off data URL part
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        
        # Save the image
        filename = str(uuid.uuid4())+'.png'  # You can generate a unique name or use timestamps
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
        state = location_parts[-3].strip()
        city = location_parts[-4].strip()
        print(city)
        # pincode = location_parts[-2].strip()
        # country = location_parts[-1].strip()
        with open(filepath, 'rb') as f:
            image_data = f.read()

        # Prepare the prompt and send the image to the Gemini API
        prompt = "This image contains packaged products.Please analyze the image and provide:for each product:1)Product Name: 2)Product Category 3)Product Quantity 4)Product Count 5)Expiry Date (if available) 6)Freshness Index (based on visual cues) 7)Estimated Shelf Life 8) If there are multiple products,give answer for each"
        response = model.generate_content(
            [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(image_data).decode("utf-8"),
                },
                prompt,
            ]
        )
        print(response.text)



        return jsonify({
            'message': f'Image saved successfully at {filepath}',
            'location': exactLocation
        })



    return jsonify({'error': 'No image provided'}), 400

if __name__ == '__main__':
    app.run(debug=True,port=8000)
