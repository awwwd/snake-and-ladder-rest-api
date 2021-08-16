#!/usr/bin/env bash

case "$1" in
  deploy)
    echo "[INFO] Deploying mongodb in kubernetes..."
    kubectl apply -f deployment/db/deployment.yml
    sleep 10
    echo "[INFO] Deploying app in kubernetes..."
    kubectl apply -f deployment/app/deployment.yml
  ;;
  destroy)
    echo "[INFO] Deleting mongodb from kubernetes..."
    kubectl delete -f deployment/db/deployment.yml
    echo "[INFO] Deleting app from kubernetes..."
    kubectl delete -f deployment/app/deployment.yml
  ;;
  *)
    echo "Usage: bash k8s-setup.sh (deploy|destroy)"
  ;;
esac
