# Sealed Secrets UI
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

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

## Interface

### Raw Values
![image](https://i.imgur.com/0O9ebVu.png)

### Whole Files
![image](https://i.imgur.com/OOMElW4.png)

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
The base URL of the API is available at `<base_path>/api`. There are currently 2 endpoints available.

---

### ![](https://img.shields.io/static/v1?label=Method&message=POST&color=blue) `/<base_path>/api/seal/raw`

**Description:** Seals a text value, 1 per request.

**Content-Type:** application/json

**Returns:** application/json

**Schema:**
```
{
    "context": string(required),
    "scope": string(required: "strict", "namespace-wide", or "cluster-wide"),
    "value": string(required),
    "namespace": string(required if "scope" == "strict" or "namespace-wide"),
    "secretName": string(required if "scope" == "strict")
}
```

**Example Request:**
```
{
    "context":"kubernetes-admin@kubernetes",
    "scope":"strict",
    "namespace":"my-namespace",
    "secretName":"my-sealed-secret",
    "value":"Hello World!"
}
```

**Example Response:**
```
{
    "data": "AgCdYNF39uuRtxzlkA6o6pHA99LdEfP279cViRFChgKwDrr0Q4Ey9+tfTnxIUvmiJrHG2Y24/bBdjeUJj7A86kg5NjWL/ngQLQO42I//YO21IuxgVlB+p3WK0iZRw0No/cgWyVMmJhEOQFp6HUOPKOgL67/B1Tjry96++weF/TPBa3cbb9XuRWMj+YSjpHTOOJrblg0reqpT5Serv9tTu2dV9/dpF17delxGDmSLdpKjqpoENTSJFLI7HDjYlIqikdYrSCCQKCm85aJ/Z1zzGeq8D02B9s9QOvZcX0j6b/1VsBlwOnGqEPq0T1NQFteBq9yI+uf7vte3es5qxN1lc9YPppBkhAKUSgEx/rxRkdArRBJrBccsQKFZ6XQvTX7+IK+diaJPy4KgxNPbzx1q6b0k9to4nfC4beqMs+0qi5H2UgJeDiV3IO4/IwI37aDy8Aqg9rYxO9gCzf5RQxA4Buta8kxLDGIw0btJqf7btvQhr0ti5sq5JjrM9pl/OrZNCKysyF2CAwb6hnKuvOroWOImPHUMISDn7qxk8VfTLicmK9tzYMmg05B5yEnWUY9jzZURwIne6VejLdSgwCWpjNnjjVoNYmHHh9urHtGG5utMHIFsAJXk7LJQLxAWiNXYL3yHpJO+tQ6rxy63ZOwslJwIKZmXDQ0Ept9jKQFixswYlWHshA5SR8X8+9WRoDq9sJIqALfrqVa93CscSJw="
}
```

---

### ![](https://img.shields.io/static/v1?label=Method&message=POST&color=blue) `/<base_path>/api/seal/file`

**Description:** Seals a whole file, 1 per request.

**Content-Type:** form/multipart

**Returns:** application/json

**Schema:**
```
Form 1:
    name: "json"
    content: json({
        "context": string(required),
        "scope": string(required: "strict", "namespace-wide", or "cluster-wide"),
        "value": string(required),
        "namespace": string(required if "scope" == "strict" or "namespace-wide"),
        "secretName": string(required if "scope" == "strict")
    })

Form 2:
    name: "file"
    filename: arbitrary, name of file to send
    Content-Type: mime-type of file
    content: file contents
```

**Example Request:**
```
-----------------------------164851293116400020413430862486
Content-Disposition: form-data; name="json"

{"context":"kubernetes-admin@kubernetes","scope":"strict","namespace":"my-namespace","secretName":"my-sealed-secret"}
-----------------------------164851293116400020413430862486
Content-Disposition: form-data; name="file"; filename="example.txt"
Content-Type: text/plain

Hello World!

-----------------------------164851293116400020413430862486--
```

**Example Response:**
```
{
    "data": "AgAycOlZVQtp7b6/QyjIJ1VY1fd+MdXdMyjvRwtlevt8D+CK5nFRYY3hPJ1T/1LukTAJm6tz4mAFthXGy+Iteqcwz2GZQNtLh7Gt+6c9Xxi4HNjmpwCQbXd4o5BiK0tc4Nzgte21szQXPDkIkYStUGSTsfvhPNCtkhaV2kISMxjbdbVmz0js1Ud21cx3qvavPUO7sM1foNG99Hym2l98K6x9FfwRoKC2UulIL16/+17CiiZIMDaRyfp/HkwblTWD/wBdtb1gVU/A2P3etBgsiUHX9FG22kr98zLUwRQPAAjkkY+wAldWXb57lVHGyfhWVbbkW0P3VsdHsF/kp3SuEBHdtvSTYLuBYOnTowQqJcwm/rJJYJhC8GwFZqx1BRGOksg2JHBA5B74CWCbvX8/OkfFlYUbgQ+XTu/4LUi014dCwMsSz/pw8DQPxyjJMqERt5eAnEFTkmRUTnANsS9PwTz+Fua/r0o+AXWPfcpqg2yR9qCbFOSTeGuK9njRSgzSpbcKk2fcxPYUFYFD3662+RKzh8p47IuS9KLSBBl3qxj2PcILDIpWHCs5goipnkfDe+aStpONM23ggyzHxX/B9QWxww51Qq6y4Cm720K6qzlXo+zpxCFOPUCuJLlIFPg3mi5EaIbP1Q5pXVw5gMWy/qetOKu8qM+hrwnRBrS5jnyhgG2QzIb0ETzrOaM6cv6FX0Fm9hU+Fg/8EeMrfW9Q"
}
```
