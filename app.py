from flask import Flask, render_template, request, jsonify
import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('test.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(img_bytes)).convert('RGB')
        img_np = np.array(img)

        # Convert RGB to BGR (for OpenCV)
        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # 🧠 Apply OpenCV processing here (e.g., grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # Encode processed frame back to base64
        _, buffer = cv2.imencode('.jpg', processed)
        processed_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({'processed_image': processed_base64})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
