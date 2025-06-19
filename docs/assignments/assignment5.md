# Assignment 5

This guide provides a comprehensive walkthrough on setting up Istio for A/B testing with your Helm chart in a local Minikube environment from scratch.

## 1. Prerequisites

Before you begin, ensure you have the following installed and configured:

* **Minikube:** A tool that lets you run Kubernetes locally.
* **kubectl:** The Kubernetes command-line tool, configured to communicate with your Minikube cluster.
* **Helm:** A package manager for Kubernetes (version 3.0.0 or higher).
* A text editor (e.g., VSCode, Vim, or Nano).

## 2. Starting and Configuring Minikube

Start your Minikube cluster. You likely have a Minikube installation already. It is recommended to delete the existing installation and create a new one with higher resources:

```bash
minikube start --cpus=4 --memory=8g
```

Enable the ingress within Minikube:

```bash
minikube addons enable ingress
```

Then, install Istio in your Minikube by following the instructions [here](https://istio.io/latest/docs/setup/install/istioctl/).


## 3. Setting up Hostnames for Local Access

To access the services running in Minikube via a hostname, you need to map the service hostnames to your local machine's IP address.

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

## 4. Installing the Prometheus Stack

If you have monitoring enabled in your `values.yaml`, install the kube-prometheus-stack to collect metrics:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install myprom prometheus-community/kube-prometheus-stack
```

## 5. Creating the GitHub Token Secret

Your chart is configured to use a Kubernetes secret for a GitHub token, which can be used to fetch private model artifacts. Create this secret in your cluster:

```bash
# Replace <your github PAT token> with your actual GitHub Personal Access Token
kubectl create secret generic github-token --from-literal=GITHUB_TOKEN=<your github PAT token>
```

The secret name `github-token` and the key `GITHUB_TOKEN` are specified in your `values.yaml`.

## 6. Installing the Helm Chart for A/B Testing

Install your Helm chart from the root of your repository. This configuration will enable Istio-based A/B testing as defined in your `values.yaml`:

```bash
helm install mysentiment ./sentiment-analysis \
  --set prefix=mysentiment \
  --set ingress.controller=istio \
  --set traffic.abTesting.enabled=true \
  --set rateLimit.enabled=true
```

This command ensures the following settings from the `values.yaml` are active:

* `ingress.controller: istio`
* `traffic.abTesting.enabled: true`
* `rateLimit.enabled: true`

This will deploy two versions of your application (v1 and v2) and create the necessary Istio resources to route traffic between them. This will also turn on the rate limiting feature.

## 7. Verifying the A/B Testing Setup

After the installation, verify that the Istio resources for traffic routing have been correctly created.

Check the `VirtualService`:

This resource manages how requests are routed. It should be configured to inspect the `x-user-experiment` header to direct traffic.

```bash
kubectl get virtualservice mysentiment-app -o yaml
```

The output should show routing rules that match on the `x-user-experiment` header with values `A` (control) and `B` (experiment), directing traffic to the corresponding service subsets (`v1` and `v2`).

Check the `DestinationRule`:

This resource defines the available versions (subsets) of your application service.

```bash
kubectl get destinationrule mysentiment-app -o yaml
```

The output should define subsets named `v1` and `v2`, corresponding to the `v1` and `v2` deployments of your app and model.

## 8. Performing A/B Tests

With the setup complete, you can now test the header-based routing to simulate A/B testing. This provides a "sticky session" where a user with a specific header consistently receives the same version of the application.

To reach the control version (v1):

* Make a request without the `x-user-experiment` header or with the header set to `A`:

```bash
curl http://sentiment.local/
```

```bash
curl -H "x-user-experiment: A" http://sentiment.local/
```

To reach the experiment version (v2):

* Make a request with the `x-user-experiment` header set to `B`:

```bash
curl -H "x-user-experiment: B" http://sentiment.local/
```

By analyzing the logs and metrics from each version, you can gather data on their performance and user interactions to make informed decisions based on your A/B test results.


## Accessing the Grafana Dashboard

Once the helm chart is deployed, you can access the grafana dashboard. Complete the following steps to access the dashboard

### Accessing Grafana Dashboard

1. First, get the Grafana admin password:
```bash
kubectl get secret myprom-grafana -o jsonpath="{.data.admin-password}" | base64 --decode; echo
```

2. Access Grafana:
   - Open your browser and go to Access URL: http://grafana.{{ App service endpoint }}
   - Login with:
     * Username: `admin`
     * Password: (use the password obtained in step 1)
