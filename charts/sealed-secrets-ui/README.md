# Sealed Secrets UI

A web interface for sealing your secrets for use with Bitnami Sealed Secrets.

## Quickstart
```
helm repo add sealed-secrets-ui https://noahburrell0.github.io/sealed-secrets-ui/

helm repo update

helm install sealed-secrets-ui sealed-secrets-ui/sealed-secrets-ui \
-n sealed-secrets-ui \
--create-namespace \
--set kubeconfig.sealedSecret=false \
--set kubeconfig.files.kubeconfig='<INSERT KUBECONFIG FILE CONTENTS>'
```

## Sealed Secrets UI Parameters
> `kubeconfig` configuration parameters are required.

|Name|Description|Value|
|-|-|-|
|`authFiles.enabled`|Enables adding authentication files such as a GCP Service Account file.|`false`|
|`authFiles.files`|Auth files either encrypted or plaintext (depending on `authFiles.sealedSecret`), key is filename and value is file contents|`{}`|
|`authFiles.sealedSecret`|Indicates if `authFiles.files` are sealed secrets, if `false` then `authFiles.files` will be deployed as a secret|`true`|
|`authFiles.sealedSecretConfig.scope`|If `authFiles.sealedSecret` is `true` specifies scope configuration (valid options: `strict`, `namespace-wide`, `cluster-wide`)|`""`|
|`configs.authFilesDir`|The directory in the container to mount any auth files to|`/auth`|
|`configs.basepath`|The base path of the application if operating on a path other than the root path|`""`|
|`configs.debug`|Enable debug logging in the container (WARNING: will expose secrets inputted in the web interface)|`False`|
|`configs.defaultScope`|The default scope to select in the web interface (valid options: `strict`, `namespace-wide`, `cluster-wide`)|`strict`|
|`configs.kubeconfigDir`|The directory in the container to mount the kubeconfig files to|`/kubeconfigs`|
|`configs.scopeToolTop`|A custom tooltip that appears when hovering the scope selector in the web interface|`""`|
|`kubeconfig.files`|Kubeconfig files either encrypted or plaintext (depending on `kubeconfig.sealedSecret`), key is filename and value is file contents|`{}`|
|`kubeconfig.sealedSecret`|Indicates if `kubeconfig.files` are sealed secrets, if `false` then `kubeconfig.files` will be deployed as a secret|`true`|
|`kubeconfig.sealedSecretConfig.scope`|If `kubeconfig.sealedSecret` is `true` specifies scope configuration (valid options: `strict`, `namespace-wide`, `cluster-wide`)|`""`|

## Common Parameters
|Name|Description|Value|
|-|-|-|
|`replicaCount`|The number of replicas which should be deployed|`1`|
|`image.repository`|Container image registry|`ghcr.io/noahburrell0/sealed-secrets-ui`|
|`image.pullPolicy`|Image pull policy|`IfNotPresent`|
|`image.tag`|Sealed Secrets UI image tag (immutable tags are recommended)|`""`|
|`imagePullSecrets`|Sealed Secrets UI image pull secrets|`[]`|
|`nameOverride`|String to partially override common.names.fullname|`""`|
|`fullnameOverride`|String to fully override common.names.fullname|`""`|
|`serviceAccount.create`|Enable the creation of a ServiceAccount for Sealed Secrets UI pods|`true`|
|`serviceAccount.name`|The name of the ServiceAccount to use|`""`|
|`serviceAccount.annotations`|Annotations for Sealed Secrets UI Service Account|`{}`|
|`podAnnotations`|Additional pod annotations|`{}`|
|`podSecurityContext`|Set Sealed Secrets UI pod's Security Context|`{}`|
|`securityContext.runAsUser`|Set Sealed Secrets UI container's Security Context runAsUser|`1000`|
|`securityContext.runAsGroup`|Set Sealed Secrets UI container's Security Context runAsGroup|`1000`|
|`service.type`|Sealed Secrets UI service type|`ClusterIP`|
|`service.port`|Sealed Secrets UI service Port|`5000`|
|`ingress.enabled`|Enable ingress resource for Sealed Secrets UI|`true`|
|`ingress.className`|Set the ingress class to user|`""`|
|`ingress.annotations`|Additional annotations for the Ingress resource. To enable certificate autogeneration, place here your cert-manager annotations.|`{}`|
|`ingress.host`|Hostname used for the ingress resource|`example.local`|
|`ingress.tls`|TLS configuration for the ingress resource|`[]`|
|`resources.limits.cpu`|The requested cpu limit for the container|`100m`|
|`resources.limits.memory`|The requested memory limit for the container|`128Mi`|
|`resources.requests.cpu`|The requested cpu resources for the container|`100m`|
|`resources.requests.memory`|The requested memory resources for the container|`128Mi`|
|`autoscaling.enabled`|Enable Horizontal Pod Autoscaling|`false`|
|`autoscaling.minReplicas`|Minimum number of replicas|`1`|
|`autoscaling.maxReplicas`|Maximum number of replicas|`100`|
|`autoscaling.targetCPUUtilizationPercentage`|Target CPU utilization percentage|`50`|
|`autoscaling.targetMemoryUtilizationPercentage`|Target Memory utilization percentage|`80`|
|`nodeSelector`|Node labels for pod assignment|`{}`|
|`tolerations`|Tolerations for pod assignment|`[]`|
|`affinity`|Affinity for pod assignment|`{}`|
|`extraDeploy`|Array of extra objects to deploy with the release|`[]`|
|`extraEnvs`|Map of extra environment variables to inject into the configmap|`{}`|