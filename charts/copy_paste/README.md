# Copy Paste Helm Chart

A Helm chart for deploying the Copy Paste application to Kubernetes.

## Overview

This chart deploys the Copy Paste application, a simple pastebin-like service built with Django. It includes a PostgreSQL database for storage and supports various configuration options.

## Dependencies

This chart depends on the following:

- [homelab-helm-charts](https://github.com/jheckmanorg/homelab_helm_charts) - A library of common Helm templates
- [postgresql](https://github.com/bitnami/charts/tree/master/bitnami/postgresql) - The PostgreSQL database chart from Bitnami

## Installation

```bash
# Add the Bitnami repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install the chart
helm install copy-paste ./charts/copy_paste
```

## Configuration

The following table lists the configurable parameters of the Copy Paste chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Image repository | `${ECR_REGISTRY}/${ECR_REPOSITORY}` |
| `image.pullPolicy` | Image pull policy | `Always` |
| `image.tag` | Image tag | `""` |
| `imagePullSecrets` | Image pull secrets | `[]` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `8000` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.hosts` | Ingress hosts | `[{host: chart-example.local, paths: [{path: /, pathType: Prefix}]}]` |
| `ingress.tls` | Ingress TLS configuration | `[]` |
| `postgresql.enabled` | Enable PostgreSQL | `true` |
| `postgresql.auth.database` | PostgreSQL database name | `copy_paste` |
| `postgresql.auth.username` | PostgreSQL username | `copy_paste` |
| `postgresql.auth.existingSecret` | Name of existing secret containing PostgreSQL credentials | `copy-paste-postgresql-auth` |
| `env` | Environment variables | See values.yaml |
| `envOverrides` | Environment variable overrides | `[]` |
| `secrets.django.secretKey` | Django secret key | `changeme` |
| `cronJobs` | List of cron jobs | See values.yaml |

## Template Structure

This chart uses a single template file that includes all the necessary resources:

```yaml
# templates/all.yaml
{{- include "common.serviceaccount" . }}
---

{{- include "common.secrets" . }}
---

{{- include "common.service" . }}
---

{{- include "common.deployment" . }}
---

{{- include "common.ingress" . }}
---

{{- include "common.cronjobs" . }}
---

{{- include "common.init-job" . }}
```
