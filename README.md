# Operation Repository — REMLA Assignment 1

This repository serves as the orchestration layer for our machine learning application, enabling seamless deployment of all components (frontend, backend, and model service) via Docker Compose.

---

## Included Repositories

This project consists of the following repositories:

- [`lib-ml`](https://github.com/remla25-team14/lib-ml): Shared preprocessing logic used by both training and model-service.
- [`model-training`](https://github.com/remla25-team14/model-training): Trains the sentiment classifier and publishes model releases.
- [`model-service`](https://github.com/remla25-team14/model-service): Exposes a REST API to analyze restaurant reviews using the trained model.
- [`lib-version`](https://github.com/remla25-team14/lib-version): Provides a shared utility to expose version information from a `VERSION` file, used by the app to return its version dynamically.
- [`app`](https://github.com/remla25-team14/app): Web interface (React frontend + Flask backend) that interacts with the model service.
- [`operation`](https://github.com/remla25-team14/operation): This repo; integrates and launches all components.

---

## Run the System

By default, the system is configured to use the `latest` version for both the `model-service` image and the trained model artifact. The application will automatically fetch the latest release from the `model-training` repository.

### Overriding Default Versions (Optional)

You can override the default versions by setting environment variables before running the system. This is useful for testing specific releases.

**1. Override Trained Model Version:**

To use a specific trained model, set the `TRAINED_MODEL_VERSION` variable. This version must match a release tag in the `model-training` repository.

```bash
export TRAINED_MODEL_VERSION=v0.1.3
```

**2. Override Model Service Image:**

To use a specific `model-service` Docker image, set the `MODEL_SERVICE_IMAGE_TAG` variable. This version must match an image tag on GHCR.

```bash
export MODEL_SERVICE_IMAGE_TAG=v0.1.6-rc.1
```

After launching the system with overrides, you can verify the versions being used by checking the labels in the web application UI.

---

### Start the System

```bash
./run.sh
```

This will:
- Load the app version from `../app/VERSION`
- Build and launch:
  - the React+Flask app (on port `5001`)
  - the model-service (on port `5002`)
- Bind all internal APIs together using Docker networking

---

### Open in Browser

- App frontend: http://localhost:5001
- Model service: http://localhost:5002/version

---

## ️Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_SERVICE_IMAGE_TAG` | Docker image tag for the `model-service` | `latest` |
| `TRAINED_MODEL_VERSION` | GitHub release tag for model download | `latest` |
| `APP_VERSION` | Auto-loaded from `../app/VERSION` | - |

---

## Model Release Workflow

The system uses GitHub releases for model delivery:

1. **Model Training**: Trains model and creates a GitHub release with model artifacts
2. **Model Service**: Downloads model from the specified release tag
3. **Caching**: Models are cached locally by version for faster startup

To use a new model version:
1. Train and release a new model in `model-training`
2. Update `TRAINED_MODEL_VERSION` environment variable
3. Restart the system

---

## Monitoring and Observability

We have instrumented the backend service with Prometheus to expose and collect metrics for improved observability. These metrics include:

- **Application Info (`app_info`)**: Captures the application version as a gauge metric.
- **Sentiment Ratio (`sentiment_ratio`)**: A gauge tracking the ratio of positive reviews to total reviews.
- **Sentiment Predictions (`sentiment_predictions_total`)**: A counter labeled by `sentiment` (`positive` or `negative`) counting each prediction.
- **Model Response Time (`model_response_time_seconds`)**: A histogram measuring the response time from the model service.

The backend exposes these metrics at the `/metrics` endpoint. In Kubernetes, the `ServiceMonitor` defined in `app/kubernetes/monitoring.yml` scrapes the `sentiment-app-service` (port `http`) every second at the `/metrics` path.

By integrating Prometheus with our application and Kubernetes `ServiceMonitor`, we enable real-time monitoring, alerting, and dashboarding of key performance and usage metrics.

---

## Progress Log

### Assignment 1 – Versioning, Releases and Containerization

- All components are split into individual repositories
- Model is trained and published as a GitHub Release
- `lib-ml` is created and reused in both training and inference
- `model-service` loads the model dynamically from GitHub releases
- `app` integrates frontend, backend, versioning, and feedback flow
- Dockerfiles and GitHub Actions are implemented for all components
- This repository integrates everything with Docker Compose
- System is tested end-to-end — sentiment analysis is working

---

## Contributors

See `ACTIVITY.md` for individual contributions and PR links.



# Kubernetes Vagrant Setup - REMLA Assignment 2

This project provisions a Kubernetes environment using **Vagrant** and **Ansible**.

---

## Prerequisites

- Vagrant (latest version)
- VirtualBox or another Vagrant-supported provider
- Ansible

## Quick Start

1. **Add your SSH key**:
   ```bash
   mkdir -p ssh_keys
   cp ~/.ssh/id_rsa.pub ssh_keys/your_ssh_key.pub

---
2. **Start the cluster**:
   ```bash
   vagrant up
   
3. **Run finalization**:
   ```bash
   cd ansible
   ansible-playbook -u vagrant -i 192.168.56.100, finalization.yml
   ```

4. **Control kubectl from host**:
   ```bash
   export KUBECONFIG="$(pwd)/ansible/.kube/config"
   ```
   To check if this worked, you can run the following command on your host machine:
   ```bash
   kubectl get nodes
   ```


