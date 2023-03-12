# Sealed Secrets UI
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

![image](https://i.imgur.com/0O9ebVu.png)

## Introduction

This application is designed to provide a web-based GUI for encrypting Kubernetes secrets for use with Bitnami Sealed Secrets using the Kubeseal utility.

This application currently supports:
- All Kubeseal scopes (`strict`, `namespace-wide`, and `cluster-wide`)
- Context selection
    - Multiple Kubeconfig files
    - Automatic context discovery from Kubeconfig files
- Encryption of raw text (Ie. Kubeseal's `--raw` parameter)
- Whole file encryption (Ie. Kubeseal's `--raw --from-file` parameters) with in-browser file uploads
- Direct API calls to seal secrets

This application currently **does not** support:
- Converting Kubernetes Secret manifests to SealedSecret manifests (yet)
- Any sort of authentication to the API or web UI
- Setting the namespace that the Sealed Secrets operator is installed to (must be `kube-system`)

## Setup

### Run in Kubernetes
This application is designed to run in Kubernetes! A set of base Kubernetes manifests are available in the [manifests](manifests/) directory. A mount method for your Kubeconfig file/s is not included in these manifests. Please see the note below and consult with the Kubernetes docs to implement your chosen method.

Docker images are available in GHCR [here](https://github.com/noahburrell0/sealed-secrets-ui/pkgs/container/sealed-secrets-ui).

Just mount in your Kubeconfig and update the `configmap.yaml` with your settings. Optionally, you may wish to set up an ingress for ease of access (not included in manifests).

### Kubeconfig/s
Kubeconfig files can be mounted into the container using either a PersistenVolume or by mounting a secret. The directory that the files are mount into should be specified by the `KUBECONF_DIR` environment variable. Please consult with the Kubernetes documentation if you are unsure how to do this.

### Environment Variables
Set your environment variable in the [configmap](manifests/configmap.yaml).

|Variable|Type|Required|Default|Notes|
|-|-|:-:|-|-|
|KUBECONF_DIR|String|✔|None|Absolute path to directory containing kubeconfig file/s, do not include a trailing `/` .
|BASE_PATH|String||`""`|Defines the base path the web UI and API operate on, do not include a trailing `/` .
|DEFAULT_SCOPE|String||None|Defines the scope selected by default in the web UI. Valid options: `strict`, `namespace-wide`, or `cluster-wide`.
|SCOPE_TOOLTIP|String||None|Enables an in-browser tooltip when hovering the scope selection.
|DEBUG|Boolean||`False`|May output sensitive information in logs if enabled.

### Accessing the Web UI
By default, the application listens on `0.0.0.0:5000` and the kubernetes service is configured on the same port. To access the API and web UI (assuming no ingress is configured and the service has not been reconfigured as a loadbalancer), use `kubectl` to create a proxy to the application.

```
kubectl port-forward service/sealed-secrets-ui-svc 5000:5000 -n sealed-secrets-ui
```

Assuming the `BASE_PATH` env has not been modified, the web UI should now by accessible at `http://localhost:5000/`

## Running Locally

> Developed with Python 3.10, not guarenteed to work with other versions.

1. Fork and/or clone this repository.
2. Create a Python virtual environment.
```
python -m venv ./venv
```
3. Activate the virtual environment.
```
source venv/bin/activate
```
4. Setup the Kubeconfig directory.
```
export KUBECONF_DIR="/path/to/my/kubeconfigs"
```
5. Install requirements.
```
pip install -r requirements.txt
```
6. Run in local development mode.
```
python main.py
```
7. UI should be reachable at `http://localhost:5000/` by default unless you have set the `BASE_PATH` environment variable.

## API Usage

For API usage information, please see [API.md](API.md).
