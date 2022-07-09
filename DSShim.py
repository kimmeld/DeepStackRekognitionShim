from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import logging
from PIL import Image
import io

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
rekognition_client = boto3.client('rekognition')


@app.route("/v1/vision/detection", methods=["POST"])
def process_image():
    # Get image to analyze
    f = request.files['image']
    image = {"Bytes": f.stream.read()}

    dsresp = {'predictions': [], 'success': True}

    # Call Rekognition
    logger.info("Calling Rekognition")
    try:
        resp = rekognition_client.detect_labels(Image=image)
        requestid = resp['ResponseMetadata']['RequestId']
        statuscode = resp['ResponseMetadata']['HTTPStatusCode']
        logger.info(f"Rekognition RequestID: {requestid}, Status: {statuscode}")

        # Now convert the AWS response into something resembling what DeepStack will return
        with Image.open(io.BytesIO(image['Bytes'])) as img:
            for l in resp['Labels']:
                for i in l['Instances']:
                    # Rekognition returns label locations in a range of 0-1, but DeepStack returns them in pixels
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
    except ClientError:
        logger.error("Error calling Rekognition")
        dsresp['success'] = False

    return jsonify(dsresp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
