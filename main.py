from fastapi import FastAPI
import os
import socket

app = FastAPI()

# This gets set via an environment variable in the Helm chart later.
# Bumping it (and rebuilding the image) is how we'll visibly prove
# that ArgoCD picked up a change and rolled out a new version.
APP_VERSION = os.getenv("APP_VERSION", "v0.1.0")

@app.get("/")
def read_root():
    return {
        "message": "Hello from the GitOps demo app",
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
