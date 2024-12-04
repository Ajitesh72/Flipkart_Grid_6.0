from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64
import os
import uuid
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

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
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

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
        # state = location_parts[-3].strip()
        # pincode = location_parts[-2].strip()
        # country = location_parts[-1].strip()
        return jsonify({
            'message': f'Image saved successfully at {filepath}',
            'location': exactLocation
        })



    return jsonify({'error': 'No image provided'}), 400
    

if __name__ == '__main__':
    app.run(debug=True,port=8000)
