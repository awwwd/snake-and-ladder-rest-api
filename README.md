# Snake and Ladder REST API
This is a simple Snake and Ladder REST API created using Python FastAPI framework. It
uses mongodb as backend datastore and also provides the API Documentation in Swagger UI.

> Note: All configuration variables are overridable from outside as environment variables.

### Kubernetes Deployment View
![Deployment](assets/deployment.png?raw=true "Kubernetes Deployment View")

### App Components
Refer to Swagger UI to get an overview on application components and API.

http://snake-ladder-api.traefik.k8s/docs

> Note: The link only works after deployment

## Pre-requisites
Make sure you have the following tools installed for development or to simulate a actual kubernetes style
deployment in your local cluster.
- Docker Desktop (development + deployment)
- Helm (deployment)

## Development Setup
Use docker-compose for development
```shell
$ docker-compose up
```
And access http://localhost:8080/docs for Swagger page


## Setup Guide
1. Install traefik to use as a Load Balancer
```shell
# Add helm repo and update [optionally]
$ helm repo add traefik https://helm.traefik.io/traefik
$ helm repo update

# Create the traefik config file
$ cat << EOF > traefik-values.yaml
dashboard:
  enabled: true
  domain: traefik.k8s
kubernetes:
  namespaces:
    - default
    - kube-system
    - app
    - db
EOF

# Install traefik
$ helm install traefik/traefik traefik --values traefik-values.yaml

# Add these entries in /etc/hpsts
# 127.0.0.1	localhost traefik.k8s snake-ladder-api.traefik.k8s
```

2. Run the kubernetes deployment files
```shell
# This script will deploy the db and app components
# Creates individual namespaces for database and application
# Creates a HPA and Ingress for application
$ bash k8s-setup.sh
Usage: bash k8s-setup.sh (deploy|destroy)

# Let's deploy the cluster
$ bash k8s-setup.sh deploy
```

3. Access the Swagger UI (API Documentation) form your browser http://snake-ladder-api.traefik.k8s/docs


4. To bring down the cluster
```shell
$ bash k8s-setup.sh destroy
```
