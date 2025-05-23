# Helm Chart - Sentiment Analysis App

This Helm chart deploys the sentiment analysis web application and its model service to a Kubernetes cluster, with optional Prometheus monitoring.

---

## Prerequisites

Minikube >= v1.30.0

kubectl configured to talk to Minikube

Helm >= v3.0.0

---

### Testing with Minikube

Below are the instructions to install this helm chart with minikube

```bash
minikube start
minikube addons enable ingress
```

Next add the hostnames to your system’s hosts file. To do this, you open your etc/hosts file by running


```bash
sudo nano /etc/hosts
```
(You can substitute nano for vim, code --wait, etc.)

```bash
127.0.0.1 sentiment.local grafana.sentiment.local prometheus.sentiment.local
```

Flush your DNS cache (if needed):

    macOS (Big Sur+):

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```


Linux (systemd-resolved):

        sudo systemd-resolve --flush-caches

```bash
  sudo systemd-resolve --flush-caches
```

Install the Prometheus Stack if you have not already 

1. Install the Prometheus stack with the matching selector
```bash
Install the kube-prometheus-stack under the monitoring namespace, giving it the label selector release=myprom:

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 1a) CRDs only (first time)
helm install prometheus-crds prometheus-community/kube-prometheus-stack-crds \
  --namespace monitoring --create-namespace

# 1b) Core stack, with serviceMonitorSelector matching 'myprom'
helm install myprom prometheus-community/kube-prometheus-stack \
  --set prometheus.prometheusSpec.serviceMonitorSelector.matchLabels.release=myprom \
  --set grafana.enabled=true
```
---

## 2. Create Secret

Before installing the chart, create the GitHub token secret. The Github token is your PAT token which is used to fetch the model artifact. You can create/manage your PAT [here](https://github.com/settings/tokens).

```bash
kubectl create secret generic github-token \                                
  --from-literal=GITHUB_TOKEN=<your github PAT token>
```
---

## 3. Install the Chart

In the root of the repo. Run the following command

```bash
helm install mysentiment ./sentiment-analysis --set prefix=mysentiment
```

You can install multiple versions by changing the prefix:

```bash
helm install version2 ./sentiment-analysis --set prefix=version2
```

In the console, you will see the various endpoints that the application has, including the grafana dashboard and the prometheus dashboard.

## Verify Installation

Verify the install by running

```bash
kubectl get pods
kubectl get svc
```

---
# Note for the Reviewers

The application does not require a config map. Yet, to demonstrate our knowledge, we created a `configmap.yaml` with a dummy config map and use it in the `deployment-app.yaml` file. 

