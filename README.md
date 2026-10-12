# gitops-demo-app

A minimal FastAPI application used to practice a GitOps delivery flow on Azure Kubernetes Service (AKS) with ArgoCD.

The app is intentionally small. The point of this project is the delivery chain around it, not the application itself.

## The app

| Endpoint | Response |
|----------|----------|
| `GET /` | A greeting, the current `version`, and the pod `hostname` |
| `GET /health` | `{"status": "ok"}`, used for the liveness and readiness probes |

The version comes from the `APP_VERSION` environment variable. Because the response shows the version and the pod name, it is easy to see a new release being rolled out.

## Run it locally

```bash
docker build -t gitops-demo-app .
docker run -p 8000:8000 gitops-demo-app
curl http://localhost:8000/
```

The image is based on `python:3.12-slim` and runs the app with uvicorn on port 8000.

## How the GitOps flow works

This repository only holds the application code and the Dockerfile. The Kubernetes deployment lives in a separate repository, [gitops-demo-config](https://github.com/AMNOURDDINE/gitops-demo-config), as a Helm chart.

1. I change the app and build a new container image with a new tag.
2. I push the image to Azure Container Registry.
3. I update the image tag in the config repository.
4. ArgoCD, running in the AKS cluster, detects the change in Git and syncs it.
5. Kubernetes performs a rolling update, and `GET /` shows the new version.

Nothing is deployed by hand with `kubectl`. Git is the single source of truth for what runs in the cluster.
