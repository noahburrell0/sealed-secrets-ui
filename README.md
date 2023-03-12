# Sealed Secrets UI
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

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
- Converting Kubernetes Secret manifests to SealedSecret manifests
- Any sort of authentication to the API or web UI
- Setting the namespace that the Sealed Secrets operator is installed to (must be `kube-system`)

## Usage

### Kubeconfig/s
Kubeconfig files can be mounted into the container using either a PersistenVolume or by mounting a secret. The directory that the files are mount into should be specified by the `KUBECONF_DIR` environment variable.

### Environment Variables
|Variable|Type|Required|Default|Notes|
|-|-|:-:|-|-|
|KUBECONF_DIR|String|✔|None|Absolute path to directory containing kubeconfig file/s, do not include a trailing `/` .
|BASE_PATH|String||`""`|Defines the base path the web UI and API operate on, do not include a trailing `/` .
|DEFAULT_SCOPE|String||None|Defines the scope selected by default in the web UI. Valid options: `strict`, `namespace-wide`, or `cluster-wide`.
|SCOPE_TOOLTIP|String||None|Enables an in-browser tooltip when hovering the scope selection.
|DEBUG|Boolean||`False`|May output sensitive information in logs if enabled.

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

