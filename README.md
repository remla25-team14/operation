# REMLA Operations Repository

This repository serves as the orchestration layer for our machine learning application, providing seamless deployment and management of all system components including frontend, backend, and model services.

## Table of Contents

* [Architecture Overview](#architecture-overview)
* [Prerequisites](#prerequisites)
* [Quick Start](#quick-start)

  * [Assignment 1: Docker Deployment](#assignment-1-docker-deployment)
  * [Assignment 2: Kubernetes with Vagrant](#assignment-2-kubernetes-with-vagrant)
  * [Assignment 3: Operate and Monitor Kubernetes](#assignment-3-operate-and-monitor-kubernetes)
  * [Assignment 4: ML Configuration Management & ML Testing](#assignment-4-ml-configuration-management--ml-testing)
  * [Assignment 5: Istio Service Mesh](#assignment-5-istio-service-mesh)
* [Monitoring](#monitoring)
* [Contributors](#contributors)
* [Support](#support)

---

## Architecture Overview

The REMLA system consists of six interconnected repositories that work together to provide a complete ML-powered sentiment analysis application:

### Core Components

| Repository                                                           | Purpose                                    | Technology        |
| -------------------------------------------------------------------- | ------------------------------------------ | ----------------- |
| [`lib-ml`](https://github.com/remla25-team14/lib-ml)                 | Shared preprocessing logic                 | Python            |
| [`model-training`](https://github.com/remla25-team14/model-training) | Model training pipeline                    | Python/MLOps      |
| [`model-service`](https://github.com/remla25-team14/model-service)   | REST API for model inference               | Python/Flask      |
| [`lib-version`](https://github.com/remla25-team14/lib-version)       | Version management utility                 | Python            |
| [`app`](https://github.com/remla25-team14/app)                       | Web interface                              | React + Flask     |
| [`operation`](https://github.com/remla25-team14/operation)           | **This repo** - Orchestration & deployment | Docker/Kubernetes |


---

## Prerequisites
* Docker and Docker Compose
* Git
* GitHub Personal Access Token (for model artifact access)

### For Kubernetes Deployment

* Vagrant (latest version)
* VirtualBox or compatible provider
* Ansible

---

## Quick Start

### Assignment 1: Docker Deployment

By default, the system is configured to use the `latest` version for both the `model-service` image and the trained model artifact. The application will automatically fetch the latest release from the `model-training` repository.

#### Overriding Default Versions (Optional)

You can override the default versions by setting environment variables before running the system. This is useful for testing specific releases.

**1. Override Trained Model Version:**

To use a specific trained model, set the `TRAINED_MODEL_VERSION` variable. This version must match a release tag in the `model-training` repository.

```bash
export TRAINED_MODEL_VERSION=v0.1.3
```

**2. Override Model Service Image:**

To use a specific `model-service` Docker image, set the `MODEL_SERVICE_IMAGE` variable. This version must match an image tag on GHCR, like `v0.1.6`.

```bash
export MODEL_SERVICE_IMAGE=ghcr.io/remla25-team14/model-service:v0.1.6
```

After launching the system with overrides, you can verify the versions being used by checking the labels in the web application UI.

#### 1. Environment Setup

Create a folder inside of `operations` named `secrets`, with a text file where you put your PAT:

```bash
cd /operations
mkdir -p secrets
touch github_token.txt
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 2. Launch the Application
```bash
./run.sh
```

#### 3. Access the Application

* **Web Interface**: [http://localhost:5001](http://localhost:5001)
* **Model Service API**: [http://localhost:5002/version](http://localhost:5002/version)
* **Metrics Endpoint**: [http://localhost:5001/metrics](http://localhost:5001/metrics)


#### Environment Variables

| Variable       | Description                      | Default/Example                   |
| -------------- | -------------------------------- | --------------------------------- |
| `GITHUB_TOKEN` | GitHub token for artifact access | Required                          |
| `MODEL_SERVICE_IMAGE` | Model service Docker image | `ghcr.io/remla25-team14/model-service:latest` |
| `TRAINED_MODEL_VERSION` | Model artifact version | `latest` |

### Assignment 2: Kubernetes with Vagrant

1. **Prepare SSH access**:
   ```bash
   mkdir -p ssh_keys
   cp ~/.ssh/id_rsa.pub ssh_keys/your_ssh_key.pub
   ```
2. **Provision the cluster**:
   ```bash
   vagrant up
   ```
3. **Complete cluster setup**:

   ```bash
   cd ansible
   ansible-playbook -u vagrant -i 192.168.56.100, finalization.yml
   ```
4. **Configure local kubectl**:

   ```bash
   export KUBECONFIG="$(pwd)/ansible/.kube/config"
   kubectl get nodes
   ```

### Assignment 3: Operate and Monitor Kubernetes

This assignment involves deploying the application to a Kubernetes cluster and configuring monitoring with Prometheus and Grafana.

#### Steps:

1. **Start Minikube**:

   ```bash
   minikube start
   minikube addons enable ingress
   ```

2. **Edit `/etc/hosts`**:
   Add the following entries (use the ingress IP address shown by `kubectl get ingress`):
   ```bash
   192.168.49.2 sentiment.local
   192.168.49.2 grafana.sentiment.local
   192.168.49.2 prometheus.sentiment.local
   ```
3. **Create GitHub Token Secret**:

   ```bash
   kubectl create secret generic github-token --from-literal=GITHUB_TOKEN=<your_github_token>
   ```

4. **Install Prometheus Monitoring Stack**:

   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   helm install myprom prometheus-community/kube-prometheus-stack
   ```

5. **Install Helm Chart**:

   ```bash
   helm install mysentiment ./sentiment-analysis \
     --set prefix=mysentiment \
     --set ingress.enabled=true \
     --set ingress.controller=nginx \
     --set ingress.className=nginx \
     --set ingress.host=sentiment.local \
     --set rateLimit.enabled=false \
     --set traffic.abTesting.enabled=false
   ```

#### Overriding Model Service Version (Kubernetes/Helm)

You can override both the model service image and trained model version for Kubernetes deployments. Both overrides must be set together to ensure consistency:

```bash
helm install mysentiment ./sentiment-analysis \
  --set modelServiceOverride.enabled=true \
  --set modelServiceOverride.image=ghcr.io/remla25-team14/model-service:v0.1.6 \
  --set modelServiceOverride.imageTag=v0.1.6 \
  --set modelServiceOverride.trainedModelVersion=v0.1.3 \
  --set prefix=mysentiment \
  --set ingress.enabled=true \
  --set ingress.controller=nginx \
  --set ingress.className=nginx \
  --set ingress.host=sentiment.local
```

Note: Always set both `modelServiceOverride.image` and `modelServiceOverride.imageTag` to ensure the container image and environment variables are consistent.

After deployment, you can verify the versions:
1. Check the pod's image and environment variables:
   ```bash
   kubectl describe pod <model-pod-name>
   ```
2. Access the model service's version endpoint:
   ```bash
   curl http://sentiment.local/version
   ```

### Assignment 4: ML Configuration Management & ML Testing

Documentation coming soon / maintained in separate repo(s).

### Assignment 5: Istio Service Mesh

This assignment sets up advanced traffic routing (A/B testing) using Istio's service mesh capabilities.

#### Steps:

1. **Start Minikube** (if using minikube):

   ```bash
   minikube start --cpus=4 --memory=8g
   ```

2. **Install Istio**:

   ```bash
   curl -L https://istio.io/downloadIstio | sh -
   cd istio-*/
   export PATH="$PWD/bin:$PATH"
   istioctl install --set profile=demo -y
   kubectl label namespace default istio-injection=enabled
   ```

3. **Install Prometheus Stack**:

   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   helm install myprom prometheus-community/kube-prometheus-stack
   ```

4. **Create GitHub Token Secret**:

   ```bash
   kubectl create secret generic github-token --from-literal=GITHUB_TOKEN=<your_github_token>
   ```

5. **Install Helm Chart with Istio and A/B Testing**:

   ```bash
   helm upgrade --install sentiment ./sentiment-analysis \
     --set traffic.abTesting.enabled=true \
     --set ingress.controller=istio \
     --set app.images.v2=ghcr.io/remla25-team14/app/app:v2-feedback-experiment
   ```

6. **Access the Application**:

   The application will be available at:
   - Main application: http://sentiment.local:32514
   - Grafana dashboard: http://grafana.sentiment.local:32514
   - Prometheus: http://prometheus.sentiment.local:32514

   Note: The port number (32514) might be different in your setup. You can find the correct port with:
   ```bash
   kubectl get svc -n istio-system istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}'
   ```

7. **Verify A/B Testing**:

   The traffic is automatically split:
   - 90% of traffic goes to v1
   - 10% of traffic goes to v2

   You can verify this by:
   - Checking the pods: `kubectl get pods -l app=sentiment-sentiment-chart-app --show-labels`
   - Viewing the VirtualService configuration: `kubectl get virtualservice sentiment-sentiment-chart-vs -o yaml`
   - Monitoring traffic distribution in Grafana

8. **Access Grafana Dashboard**:

   ```bash
   kubectl get secret myprom-grafana -o jsonpath="{.data.admin-password}" | base64 --decode; echo
   ```

   Navigate to http://grafana.sentiment.local:32514
   - Username: `admin`
   - Password: (retrieved from above command)
   - Look for the "Sentiment Analysis A/B Testing" dashboard

The A/B testing setup automatically splits traffic between v1 and v2 versions of your application, allowing you to gradually roll out new features and monitor their performance through Grafana dashboards.

---

## Monitoring

The application includes comprehensive observability features powered by Prometheus:

### Available Metrics

* `app_info`: Application version info (gauge)
* `sentiment_ratio`: Ratio of positive to total reviews (gauge)
* `sentiment_predictions_total`: Count of predictions by sentiment type (counter)
* `model_response_time_seconds`: Model latency (histogram)

### Setup

* Metrics are exposed at `/metrics`
* Uses `ServiceMonitor` for Prometheus scraping (1s interval)
* Grafana dashboards can visualize metrics

---

## Contributors

See [`ACTIVITY.md`](./ACTIVITY.md) for detailed contribution history and pull request links.

---

## Support

If you encounter issues or have questions:

1. Check individual repo documentation
2. Visit `/metrics` for health info
3. Use `docker-compose logs [service-name]`
4. For Kubernetes:

   * `kubectl describe pods`
   * `kubectl logs [pod-name]`
