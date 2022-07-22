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

# Rekognition options
# TODO:  Refactor these configuration options into environment variables
RESIZE_IMAGE = False
MINIMUM_CONFIDENCE = 75

@app.route("/v1/vision/detection", methods=["POST"])
def process_image():
    dsresp = {'predictions': [], 'success': True}

    # Get image to analyze
    f = request.files['image']
    img = Image.open(f.stream)

    # Save width and height, this is required to build the DeepStack response
    width = img.width
    height = img.height

    # Resize the image, this makes Rekognition perform better (less data to send to AWS)
    if RESIZE_IMAGE:
        img.thumbnail((1024,1024))

    # Build Rekognition request
    buf = io.BytesIO()   
    img.save(buf, "jpeg")
    buf.seek(0)
    image = { "Bytes": buf.read() }

    # Call Rekognition
    logger.info("Calling Rekognition")
    try:
        resp = rekognition_client.detect_labels(Image=image, MinConfidence=MINIMUM_CONFIDENCE)
        requestid = resp['ResponseMetadata']['RequestId']
        statuscode = resp['ResponseMetadata']['HTTPStatusCode']
        logger.info(f"Rekognition RequestID: {requestid}, Status: {statuscode}")

        # Now convert the AWS response into something resembling what DeepStack will return
        for l in resp['Labels']:
            for i in l['Instances']:
                # Rekognition returns label locations in a range of 0-1, but DeepStack returns them in pixels
                bb = i['BoundingBox']
                top = bb['Top'] * height
                bottom = bb['Height'] * height + top
                left = bb['Left'] * width
                right = bb['Width'] * width + left
                ds = {'x_min': int(left), 
                    'x_max': int(right), 
                    'y_min': int(top),
                    'y_max': int(bottom), 
                    'confidence': int(i['Confidence']) / 100,
                    'label': l['Name']}
                dsresp['predictions'].append(ds)
    except ClientError as e:        
        logger.error("Error calling Rekognition")
        logger.error(str(e))
        dsresp['success'] = False

    return jsonify(dsresp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
