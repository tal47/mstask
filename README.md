# Home exercise
## Prerequisite:
Install Helm.

## Configure Ingress Controller
### Create a namespace for ingress resources
```sh
kubectl create namespace ingress-basic
```

### Add the official stable repository
```sh
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
```

### Use Helm to deploy an NGINX ingress controller
```sh
helm install nginx-ingress stable/nginx-ingress \
    --namespace ingress-basic \
    --set controller.replicaCount=2 \
    --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux
```

### Get external IP using:
```sh
kubectl get service -l app=nginx-ingress --namespace ingress-basic
```

## Docker handling (only if needed)
### Docker build
```sh
$ docker build -t taltal47/mstaskpython .
```

### Docker push
```sh
$ docker push taltal47/mstaskpython
```

### Docker run (for testing)
```sh
$ docker run -d -p 80:8080 taltal47/mstaskpython
```
