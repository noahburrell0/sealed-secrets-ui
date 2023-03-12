## API Usage
The base URL of the API is available at `<base_path>/api`. There are currently 2 endpoints available.

---

### `/<base_path>/api/seal/raw`

![](https://img.shields.io/static/v1?label=Method&message=POST&color=blue) ![](https://img.shields.io/static/v1?label=Content-Type&message=application/json&color=darkgreen) ![](https://img.shields.io/static/v1?label=Returns&message=application/json&color=darkgreen)

**Description:** Seals a text value, 1 per request.

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

### `/<base_path>/api/seal/file`

![](https://img.shields.io/static/v1?label=Method&message=POST&color=blue) ![](https://img.shields.io/static/v1?label=Content-Type&message=multipart/form-data&color=darkred) ![](https://img.shields.io/static/v1?label=Returns&message=application/json&color=darkgreen)

**Description:** Seals a whole file, 1 per request.

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
