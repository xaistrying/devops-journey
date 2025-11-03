#!/bin/bash

set -e

# NAMESPACE
kubectl apply -f namespaces/dev-namespace.yaml

# GO
kubectl apply -f manifests/go/

# JAVA
kubectl apply -f manifests/java/

# PHP
kubectl apply -f manifests/php/
