from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import logging
from PIL import Image
import io

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s')
rekognition_client = boto3.client('rekognition')


@app.route("/v1/vision/detection", methods=["POST"])
def process_image():
    print(request.files)
    f = request.files['image']
    # f.save("./image.jpg")

    image = {"Bytes": f.stream.read()}
    resp = rekognition_client.detect_labels(Image=image)

    # Now convert the AWS response into something resembling what DeepStack will return
    print(resp)

    img = Image.open(io.BytesIO(image['Bytes']))

    dsresp = {'predictions': [], 'success': True}
    for l in resp['Labels']:
        for i in l['Instances']:
            bb = i['BoundingBox']
            top = bb['Top'] * img.height
            bottom = bb['Height'] * img.height + top
            left = bb['Left'] * img.width
            right = bb['Width'] * img.width + left
            ds = {'x_min': int(left), 
                'x_max': int(right), 
                'y_min': int(top),
                'y_max': int(bottom), 
                'confidence': i['Confidence'] / 100,
                'label': l['Name']}
            dsresp['predictions'].append(ds)

    print(dsresp)
    return jsonify(dsresp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
