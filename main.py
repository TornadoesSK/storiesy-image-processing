import cv2
import numpy as np
from sklearn.cluster import KMeans
import base64
from flask import Flask, request

app = Flask(__name__)

def image_to_cartoon(input_b64):
        # Decode base64 string into bytes
    img_bytes = base64.b64decode(input_b64)

    # Convert bytes into numpy array
    img_array = np.frombuffer(img_bytes, np.uint8)

    # Decode the image using cv2
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # CARTOONIZE
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    line_size = 7
    blur_value = 7

    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray_img, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

    k = 7
    data = img.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
    img_reduced = kmeans.cluster_centers_[kmeans.labels_]
    img_reduced = img_reduced.reshape(img.shape)
    img_reduced = img_reduced.astype(np.uint8)
    blurred = cv2.bilateralFilter(img_reduced, d=7, sigmaColor=200,sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    cartoon_ = cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
    # CARTOONIZE  END

    # Encode the image back into base64 string
    _, img_base64 = cv2.imencode('.png', cartoon_)
    img_base64_string = base64.b64encode(img_base64).decode('utf-8')

    return img_base64_string


@app.route('/cartoonize', methods=['POST'])
def echo():
    request_data = request.get_json()
    user_input = request_data['image']
    return {'image': image_to_cartoon(user_input)}