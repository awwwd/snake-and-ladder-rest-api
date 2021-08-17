#!/usr/bin/env bash

case "$1" in
  deploy)
    echo "[INFO] Deploying mongodb in kubernetes as statefulset..."
    kubectl apply -f deployment/db/statefulset.yml
    sleep 5
    echo "[INFO] Deploying app in kubernetes..."
    kubectl apply -f deployment/app/deployment.yml
  ;;
  destroy)
    echo "[INFO] Deleting mongodb sts from kubernetes..."
    kubectl delete -f deployment/db/statefulset.yml
    echo "[INFO] Deleting app from kubernetes..."
    kubectl delete -f deployment/app/deployment.yml
  ;;
  *)
    echo "Usage: bash k8s-setup.sh (deploy|destroy)"
  ;;
esac
