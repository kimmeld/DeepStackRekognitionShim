# Introduction
This tool is a shim which allows [AWS Rekognition](https://aws.amazon.com/rekognition/) to be used with [Blue Iris](https://blueirissoftware.com/).  It works by exposing enough of the DeepStack API so that Blue Iris will work, the requests are then proxied to Rekognition and the response transformed to look like what DeepStack would respond with.

# Why?

For my use of AWS Rekognition, the approximate AWS costs are $3CAD/month, whereas an Nvidia Jetson will cost approximately $130CAD, resulting in a payback period of over three years.

I've also found that AWS Rekognition is more accurate than DeepStack in many cases.

Another goal of this is to replace a Node-RED flow that does roughly the same thing with something that's more native to Blue Iris.  The Node-RED flow does three major things:

* Recieves Blue Iris alerts via MQTT and runs them through AWS Rekognition
* Determines whether or not to send the alert, then sends it via Home Assistant
* Logs the image and response from Rekognition to a PostgreSQL database

This shim can replace most of this, apart from the PostgreSQL logging, with only some small code to create the notification remaining in Node-RED.

# Quick Start
```
# Create venv, install required packages
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# AWS access details and region
# NOTE:  You can use any method supported by boto3 to pass these parameters
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=...

# Run it
python DSShim.py

# Or run it via the flask command...
export FLASK_APP=DSShim
python -m flask run --no-debugger --host 0.0.0.0 --port 5000 
```
NOTE:  Neither option to run this is recommended to run a Flask application in Production.  See the [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/deploying/) for more appropriate options.

Configure Blue Iris as shown below.

# Blue Iris Configuration
![Blue Iris Configuration](images/blueiris_config.png)

Select the Use AI server option and point it to the address of the machine that is running the shim.  Do not select any non-default options as these make no sense when using the shim.

# Blue Iris Camera Configuration
This is largely the same as described in the manual, however the names of the labels will be different (e.g., DeepStack returns 'car' vs Rekognition's 'Car').

Camera Settings, Trigger tab, Artificial Intelligence button:
![Blue Iris Camera Configuration](images/blueiris_camera_config.png)

Important notes:

* "Detect/ignore static objects" seems to cause periodic calls to the shim to look for static objects.  This will increase your AWS bill.
* "+ real-time images" will cause each motion detection to make multiple calls to the shim.  This will increase your AWS bill, but may be useful in some circumstances.
