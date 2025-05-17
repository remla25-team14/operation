# Helm Chart - Sentiment Analysis App

This Helm chart deploys the sentiment analysis web application and its model service to a Kubernetes cluster, with optional Prometheus monitoring.

---

## Prerequisites

- The kubernetes cluster is up by running. You can do this by running `vagrant up`.

---

## Create Secret

Before installing the chart, create the GitHub token secret. The Github token is your PAT token which is used to fetch the model artifact. You can create/manage your PAT [here](https://github.com/settings/tokens).

```bash
kubectl create secret generic github-token \                                
  --from-literal=GITHUB_TOKEN=<your github PAT token>
```
---

## Install the Chart

In the root of the repo. Run the following command

```bash
helm install mysentiment ./sentiment-analysis --set prefix=mysentiment
```

You can install multiple versions by changing the prefix:

```bash
helm install version2 ./sentiment-analysis --set prefix=version2
```

## Verify Installation

Verify the install by running

```bash
kubectl get pods
kubectl get svc
```

---
# Note for the Reviewers

The application does not require a config map. Yet, to demonstrate our knowledge, we created a `configmap.yaml` with a dummy config map and use it in the `deployment-app.yaml` file. 

