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

This assignment covers the management of data and models using DVC, versioned releases with GitHub, with remote storage on DagsHub. Furthermore ML Testing is also included here.

#### ML Configuration Management steps:

Prerequesites
- Python 3.11 or higher
- Git
- Make
- Conda (for environment management)

1. **Environment Setup**
First, create and activate a conda environment (or any that you like):

```bash
# Create conda environment
conda create -n model-training-2 python=3.11

# Activate the environment
conda activate model-training-2

# Install pip in the conda environment
conda install pip
```

2. navigate to `model-training` and **Install dependencies using Make**
```bash
make setup
```

3. **DVC and DagsHub Setup**
The repository comes with pre-configured DVC settings that point to our team's DagsHub storage. No account creation or login is needed - the credentials are already set up in the repository.

To get started with the data:

```bash
# If you have any existing DVC config, remove it first to avoid conflicts
rm -f .dvc/config*

# Configure DVC with our team's DagsHub storage credentials (all in one command)
dvc remote add -d storage s3://dvc_cloud_setup && dvc remote modify storage endpointurl https://dagshub.com/api/v1/repo-buckets/s3/s.hakimi && dvc remote modify storage access_key_id 04dc266bcc211e1d07d5fdfa4f9c999979cf7bb3 && dvc remote modify storage secret_access_key 04dc266bcc211e1d07d5fdfa4f9c999979cf7bb3 && dvc remote modify storage region us-east-1 && dvc pull
```

This will download the following files form the cloud storage:
- Raw data files in `data/raw/`
- Processed features in `data/processed/`
- Trained model in `models/`
- Model artifacts in `model_service_artifacts/`

- All data files are tracked using DVC
- Data is stored on DagsHub S3 storage
- Git is used only for code version control
- DVC configuration is version controlled and will be automatically available after cloning

4. **Pipeline reproduction**
The model training process is defined as a DVC pipeline in `dvc.yaml`. To reproduce the entire pipeline:

```bash
# Reproduce the pipeline
dvc repro
```

This command will:
1. Check if any pipeline stages need to be rerun based on changes to their dependencies
2. Process the raw restaurant reviews data
3. Generate features using the Bag of Words vectorizer
4. Train the sentiment analysis model
5. Save the model and artifacts

If no files have changed, `dvc repro` will indicate that the pipeline is up to date. If any input files or code have changed, only the affected stages will be rerun.

5. (Optional) **See & Run the experiment**

```bash
# View all experiments and their metrics
dvc exp show

# This will display a table showing:
# - Experiment names and creation times
# - Metrics for each experiment (accuracy, precision, recall, F1)
# - Parameter values used
# - File hashes for tracking changes
```

To run new experiments with different parameters:

```bash
# Modify parameters in params.yaml, then run:
dvc exp run

# Or run with parameter modifications directly:
dvc exp run --set-param training.random_state=123
dvc exp run --set-param training.test_size=0.3
```

The experiments are tracked and can be:
- Compared using `dvc exp show`
- Applied using `dvc exp apply <experiment-name>`
- Shared with others using `dvc exp push` and `dvc exp pull`

#### GitHub Releases
The GitHub releases stores only deployment-ready model artifacts which can be downloaded by other repositories

1. **Update Version**
```bash
# Edit version.txt with new version (e.g., 0.1.3)
echo "0.1.3" > version.txt
git add version.txt
git commit -m "Bump version to 0.1.3"
git push origin your-branch
```

2. **Create Release**
```bash
# Create and push version tag
git tag v0.1.3
git push origin v0.1.3
```

This triggers the CI workflow which will:
1. Run the DVC pipeline
2. Create a GitHub Release
3. Attach model artifacts:
   - `c1_BoW_Sentiment_Model.pkl`
   - `c2_Classifier_v1.pkl`
4. Automatically bump version for next release

#### Rolling Back to Previous Versions

```bash
# 1. Checkout specific git version (tag)
git checkout <commit-hash-or-tag>

# 2. Restore DVC-tracked files
dvc checkout

# 3. Pull data if needed
dvc pull
```


#### ML Testing

Model Metrics and Evaluation

The pipeline generates accuracy-related metrics in JSON format across multiple stages:

Training Metrics (`reports/metrics.json`)
Generated by the `train` stage, includes:
- **Accuracy**: Model accuracy on test set
- **Confusion Matrix**: Detailed classification results

Evaluation Metrics (`reports/evaluation.json`) 
Generated by the `evaluate` stage, includes:
- **Accuracy**: Overall model accuracy
- **Precision**: Precision score for sentiment classification
- **Recall**: Recall score for sentiment classification  
- **F1**: F1 score combining precision and recall

These metrics are automatically tracked by DVC and can be compared across different experiments using `dvc exp show`.

| Category          | Location               | Status         | Notes |
|-------------------|------------------------|----------------|-------|
| Feature & Data    | `tests/test_feat_data.py` | Done           |
| Model Development | `tests/test_model_dev.py` | Done           |
| ML Infrastructure | `tests/test_ml_infra.py` | Done           |
| Monitoring        | `tests/test_monitoring.py` | Done           |
| Metamorphic       | `tests/test_metamorphic.py` | Done

### Run the tests
```bash
# 1) install dev dependencies
pip install -e .

# 2) run tests separately (switch between the 5 .py files names)
pytest tests/test_feat_data.py -q

# 3) run all tests with coverage + ML-Test-Score
pytest -q
```


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
   - Main application: http://sentiment.local
   - Grafana dashboard: http://grafana.sentiment.local
   - Prometheus: http://prometheus.sentiment.local

7. **Verify A/B Testing**:

   The traffic is automatically split:
   - 90% of traffic goes to v1
   - 10% of traffic goes to v2

   You can verify this by:
   - Checking the pods: `kubectl get pods -l app=sentiment-sentiment-chart-app --show-labels`
   - Viewing the VirtualService configuration: `kubectl get virtualservice sentiment-sentiment-chart-vs -o yaml`
   - Monitoring traffic distribution in Grafana
   - Or by using curl using the following instructions
   Once deployed, test using your new header name:

   No header or `version: A`

   ```bash
   curl http://<hostname>/
   ```

   With version: B

   ```bash
   curl -H "version: B" http://<hostname>/
   ```


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
