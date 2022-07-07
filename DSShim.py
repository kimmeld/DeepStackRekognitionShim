from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import logging

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

    dsresp = {'predictions': [], 'success': True}
    for l in resp['Labels']:
        ds = {'x_min': 0, 'x_max': 0, 'y_min': 0,
              'y_max': 0, 'confidence': l['Confidence'] / 100,
              'label': l['Name']}
        dsresp['predictions'].append(ds)

    print(dsresp)
    return jsonify(dsresp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
