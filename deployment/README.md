# Deployment examples

## Run as a SystemD service

`dsshim.service` is a sample systemd unit file which can be used to run the shim using `waitress`.

## Run in Kubernetes

Another option is to run the shim as a Kubernetes deployment.  This uses the package on ghcr.io.

`k8s-dsshim-deployment.yaml` creates a Kubernetes deployment running a single instance of DSShim.  It also creates a `Service` so that the shim can be accessed.  You may wish to create an `Ingress` depending on how your cluster is set up, but in some cases a `Service` plus a network route into your cluster may be sufficient.

`k8s-dsshim-secret.yaml` contains the environment variables required to access AWS Rekognition, these need to be updated for your AWS account.

`k8s-dsshim-config.yaml` creates a `ConfigMap` which provides the environment variables for configuring the shim.
