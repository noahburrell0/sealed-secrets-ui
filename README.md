# Sealed Secrets UI
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0) [![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/sealed-secrets-ui)](https://artifacthub.io/packages/search?repo=sealed-secrets-ui)

![image](https://i.imgur.com/0O9ebVu.png)

## Introduction

This application is designed to provide a web-based GUI for encrypting values for use with Bitnami Sealed Secrets.

This application currently supports:
- All Kubeseal scopes (`strict`, `namespace-wide`, and `cluster-wide`)
- Context selection
    - Multiple Kubeconfig files
    - Automatic context discovery from Kubeconfig files
- Encryption of raw text (kubeseal `--raw` equivilent)
- Whole file encryption (kubeseal `--raw --from-file` equivilent) with in-browser file uploads
- Kubeconfig authentication against GKE (gke-gcloud-auth-plugin)
- Direct API calls to seal secrets

This application currently **does not** support:
- Converting Kubernetes Secret manifests to SealedSecret manifests (yet)
- Any sort of authentication to the API or web UI
- Setting the namespace that the Sealed Secrets operator is installed to (must be `kube-system`)
- Authentication against any cloud provider (excluding Google) that require an authentication plugin

## Install With Helm

View the [chart docs](charts/sealed-secrets-ui/) for installation instructions and parameters.

## Running Locally

> Developed and tested with Python 3.10, not guarenteed to work with other versions.

1. Create a Python virtual environment.
```
python -m venv ./venv
```
2. Activate the virtual environment.
```
source venv/bin/activate
```
3. Setup the Kubeconfig directory.
```
export KUBECONF_DIR="/path/to/my/kubeconfigs"
```
4. Install requirements.
```
pip install -r requirements.txt
```
5. Run in local development mode.
```
python main.py
```
6. UI should be reachable at `http://localhost:5000/` by default.

## API Usage

For API usage information, please see [API.md](API.md).
