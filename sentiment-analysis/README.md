# Helm Chart - Sentiment Analysis App

## Table of Contents
1. [Overview](#helm-chart---sentiment-analysis-app)  
2. [Prerequisites](#prerequisites)  
3. [Features](#this-helm-chart-supports)  
4. [Configuration Reference (`values.yaml`)](#configuration-reference-valuesyaml)  
   - [Global](#global)  
   - [Model Service](#model-service)  
   - [Application (App)](#application-app)  
   - [GitHub Integration](#github-integration)  
   - [Monitoring (Prometheus & Grafana)](#monitoring-prometheus--grafana)  
     - [Grafana](#grafana)  
   - [Ingress Configuration](#ingress-configuration)  
   - [A/B Testing (Canary Releases with Istio)](#ab-testing-canary-releases-with-istio)  
   - [Shared Volume (optional)](#shared-volume-optional)  
5. [Testing with Minikube](#testing-with-minikube)  
6. [Create GitHub Token Secret](#2-create-secret)  
7. [Install the Chart](#3-install-the-chart)  
8. [Verify Installation](#verify-installation)  
9. [Accessing the Grafana Dashboard](#accessing-the-grafana-dashboard)  
10. [Sticky Session for A/B Testing](#sticky-session)  
11. [Note for the Reviewers](#note-for-the-reviewers)


This Helm chart deploys the sentiment analysis web application and its model service to a Kubernetes cluster, with optional Prometheus monitoring.

---

## Prerequisites

Minikube >= v1.30.0

kubectl configured to talk to Minikube

Helm >= v3.0.0

---

This Helm chart supports:

- Istio or NGINX ingress controllers
- A/B testing (canary releases) using Istio routing with Sticky sessions.
- Prometheus/Grafana monitoring
- Prometheus/Grafana monitoring (optional Alertmanager e-mail alerts)
- Versioned app and model deployments
- Configurable GitHub token for private artifact access

---

## Configuration Reference (`values.yaml`)

### Global

| Key               | Type     | Default     | Description                                     |
|------------------|----------|-------------|-------------------------------------------------|
| `fullnameOverride` | string  | `""`        | Optionally override the chart’s full name       |
| `prefix`           | string  | `sentiment` | Used to prefix resource names                   |

---

### Model Service

| Key                   | Type     | Description                                       |
|------------------------|----------|---------------------------------------------------|
| `model.image`          | string   | Image for the model service                      |
| `model.port`           | int      | Port the model service listens on (default: 5000)|
| `model.artifactId`     | string   | Optional model artifact identifier               |
| `model.modelurl`       | string   | DNS name used by the app to reach the model      |

---

### Application (App)
| Key                       | Type     | Description                                         |
|---------------------------|----------|-----------------------------------------------------|
| `app.port`                | int      | Port the app listens on inside the container        |
| `app.servicePort`         | int      | Port exposed via Kubernetes service                 |
| `app.images.v1`           | string   | Container image for app version `v1`                |
| `app.images.v2`           | string   | Container image for app version `v2`                |

---

### GitHub Integration

| Key                   | Type     | Description                                      |
|------------------------|----------|--------------------------------------------------|
| `githubTokenSecretName` | string | Kubernetes secret name holding GitHub token     |
| `githubTokenKey`        | string | Key in the secret that stores the token         |

---

### Monitoring (Prometheus & Grafana)

| Key                       | Type     | Description                                      |
|---------------------------|----------|--------------------------------------------------|
| `monitoring.enabled`      | bool     | Enable/disable monitoring stack                  |
| `monitoring.release`      | string   | Helm release name of the Prometheus stack        |
| `prometheus.prometheusSpec.externalUrl` | string | External URL of Prometheus |
| `prometheus.prometheusSpec.routePrefix` | string | Route prefix if behind a reverse proxy           |
| `alert.enabled`                 | bool | Turn alerting resources on/off                                 |
| `alert.threshold`               | float| Request-rate threshold used in alert rule                      |
| `alert.smtpFrom` / `smtpUser`   | str  | Gmail (or other SMTP) user                                      |
| `alert.smtpPass`               | str  | **App Password** – inject with `--set`                          |
| `alert.receiverEmail`           | str  | Destination address for notifications                        |
| `prometheus.release`            | str  | Must match kube-prometheus-stack release name                   |

#### Grafana

| Key                                   | Type     | Description                        |
|----------------------------------------|----------|------------------------------------|
| `grafana.enabled`                      | bool     | Enable Grafana                     |
| `grafana.dashboard.uid`               | string   | UID of the dashboard               |
| `grafana.dashboard.title`             | string   | Title of the dashboard             |
| `grafana.dashboard.refreshInterval`   | string   | Default refresh rate               |
| `grafana.dashboard.tags`              | list     | Tags for the dashboard             |
| `grafana.dashboard.editable`          | bool     | Whether the dashboard is editable  |
| `grafana.datasource.uid`              | string   | Datasource UID to use              |
| `grafana.env.GF_SERVER_ROOT_URL`      | string   | Public root URL of Grafana         |
| `grafana.env.GF_SERVER_SERVE_FROM_SUB_PATH` | string | Serve Grafana from a subpath      |

---

### Ingress Configuration

| Key                      | Type     | Description                                                  |
|--------------------------|----------|--------------------------------------------------------------|
| `ingress.enabled`        | bool     | Enable ingress (required for external access)                |
| `ingress.controller`     | string   | `"nginx"` or `"istio"` — controls which ingress to deploy    |
| `ingress.host`           | string   | Domain or host to route traffic to                           |
| `ingress.className`      | string   | Ingress class name (`nginx` for NGINX ingress controller)    |

---

### A/B Testing (Canary Releases with Istio)

| Key                             | Type   | Description                                                   |
|----------------------------------|--------|---------------------------------------------------------------|
| `traffic.abTesting.enabled`      | bool   | Enable Istio-based canary routing                             |
| `traffic.abTesting.matchHeader`  | string | Header used to differentiate users (e.g., `x-user-experiment`)|
| `traffic.abTesting.controlValue` | string | Value that represents control group                           |
| `traffic.abTesting.experimentValue` | string | Value for experiment group                                   |
| `traffic.abTesting.appVersions`  | list   | Versions of the app to deploy (e.g. `["v1", "v2"]`)           |

---

### Shared Volume (optional)

| Key                   | Type     | Description                                         |
|------------------------|----------|-----------------------------------------------------|
| `sharedVolume.enabled` | bool    | Mount a shared host volume into app pods            |
| `sharedVolume.path`    | string  | Mount path inside the container                     |
| `sharedVolume.hostPath`| string  | Path on host (or node) to mount       

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

### For the Vagrant cluster

1. **Start the cluster**:
   ```bash
   vagrant up
   cd ansible
   ansible-playbook -u vagrant -i 192.168.56.100, finalization.yml
   export KUBECONFIG="$(pwd)/ansible/.kube/config"
   kubectl get nodes
   ```

2. **Get the cluster external IP**:
   ```bash
   # For Vagrant setup
   CLUSTER_IP=192.168.56.100
   
   # Or get Istio LoadBalancer IP (after Istio is installed)
   kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
   ```

3. **Configure host resolution**:
   ```bash
   # Add to /etc/hosts (replace with your actual cluster IP)
   sudo sh -c 'echo "192.168.56.100   sentiment.local grafana.sentiment.local prometheus.sentiment.local" >> /etc/hosts'
   ```



## 1. Install the Prometheus stack with the matching selector

Install the kube-prometheus-stack, giving it the label selector release=myprom:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install myprom prometheus-community/kube-prometheus-stack
```
---

## 2. Create Secret

Before installing the chart, create the GitHub token secret. The Github token is your PAT token which is used to fetch the model artifact. You can create/manage your PAT [here](https://github.com/settings/tokens).

```bash
kubectl create secret generic github-token --from-literal=GITHUB_TOKEN=<your github PAT token>
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

### Enable e-mail alerts (optional)
```bash
helm upgrade --install mysentiment ./sentiment-analysis \
  --set alert.enabled=true \
  --set alert.smtpUser=myapp@gmail.com \
  --set alert.smtpFrom=myapp@gmail.com \
  --set alert.smtpPass="$GMAIL_APP_PASSWORD" \
  --set alert.receiverEmail=dev-team@example.com
```

## Verify Installation

Verify the install by running

```bash
kubectl get pods
kubectl get svc
```

# Accessing the Grafana Dashboard

Once the helm chart is deployed, you can access the grafana dashboard. Complete the following steps to access the dashboard

## Accessing Grafana Dashboard

1. First, get the Grafana admin password:
```bash
kubectl get secret -n monitoring myprom-grafana -o jsonpath="{.data.admin-password}" | base64 --decode; echo
```

2. Access Grafana:
   - Open your browser and go to Access URL: http://grafana.sentiment.local/
   - Login with:
     * Username: `admin`
     * Password: (use the password obtained in step 1)

3. Find the Dashboard
  Go to **Dashboards** → **Browse**
  Search for "Sentiment Analysis A/B Testing"
  The dashboard should show 4 panels:
   - **Positive Sentiment Ratio by Version** (gauge)
   - **Model Response Time (95th percentile)** (timeseries)
   - **Sentiment Predictions Rate by Version** (timeseries)
   - **Application Info** (stat)
   
## Sticky Session

Sticky Sessions for A/B Testing

This chart supports **sticky session routing** using Istio’s header-based traffic management to implement basic A/B testing.

A sticky session means that:
- Once a user is routed to **version A or B** of the app,
- They will **continue to see the same version** across future requests,
- As long as they continue sending the same identifying header or cookie.
Customizing the Sticky Session Header

This Helm chart uses a configurable HTTP header to implement **sticky session-based A/B testing** with Istio.

By default, the chart uses:

```yaml
traffic:
  abTesting:
    matchHeader: x-user-experiment
```

To change the header name you can either change it in the `chart.yaml` file, like above or you can set it in the Helm Cli like below

```bash
helm upgrade --install mysentiment ./sentiment-analysis \
  --set prefix=mysentiment \
  --set traffic.abTesting.enabled=true \
  --set traffic.abTesting.matchHeader=x-ab-group \
  --set traffic.abTesting.experimentValue=B \
  --set traffic.abTesting.controlValue=A
```

Once deployed, test using your new header name:

No header or `x-ab-group: A`

```bash
curl http://<hostname>/
```

With x-ab-group: B

```bash
curl curl -H "x-ab-group: B" http://<hostname>/
```
---
# Note for the Reviewers

The application does not require a config map. Yet, to demonstrate our knowledge, we created a `configmap.yaml` with a dummy config map and use it in the `deployment-app.yaml` file. 

