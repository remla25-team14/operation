# Operation Repository — REMLA Assignment 1

This repository serves as the orchestration layer for our machine learning application, enabling seamless deployment of all components (frontend, backend, and model service) via Docker Compose.

---

## Included Repositories

This project consists of the following repositories:

- [`lib-ml`](https://github.com/remla25-team14/lib-ml): Shared preprocessing logic used by both training and model-service.
- [`model-training`](https://github.com/remla25-team14/model-training): Trains the sentiment classifier and uploads the model artifact.
- [`model-service`](https://github.com/remla25-team14/model-service): Exposes a REST API to analyze restaurant reviews using the trained model.
- [`lib-version`](https://github.com/remla25-team14/lib-version): Provides a shared utility to expose version information from a `VERSION` file, used by the app to return its version dynamically.
- [`app`](https://github.com/remla25-team14/app): Web interface (React frontend + Flask backend) that interacts with the model service.
- [`operation`](https://github.com/remla25-team14/operation): This repo; integrates and launches all components.

---

## Run the System

### 1. Create `.env` file

Create a `.env` file in this directory with your GitHub token for model download:

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

This token is required so that `model-service` can download the model artifact from GitHub Actions.

> Optional: Use the provided `run.sh` script to auto-load versioning and launch the system.

---

### 2. Start the System

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

### 3. Open in Browser

- App frontend: http://localhost:5001
- Model service: http://localhost:5002/version

---

## ️Environment Variables

| Variable         | Description                                   |
|------------------|-----------------------------------------------|
| `GITHUB_TOKEN`   | Required to download model artifact           |
| `OWNER_REPO`     | Hardcoded: `remla25-team14/model-training`    |
| `ARTIFACT_ID`    | Current: `3053668556`                         |
| `APP_VERSION`    | Auto-loaded from `../app/VERSION`             |

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
- Model is trained and published as a GitHub Artifact
- `lib-ml` is created and reused in both training and inference
- `model-service` loads the model dynamically using `GITHUB_TOKEN`
- `app` integrates frontend, backend, versioning, and feedback flow
- Dockerfiles and GitHub Actions are implemented for all components
- This repository integrates everything with Docker Compose
- System is tested end-to-end — emotion analysis is working

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
   kubectl get nodes



