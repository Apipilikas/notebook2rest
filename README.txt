# Notebook2REST
A tool for turning jupyter notebooks into a REST API.

``` mermaid
sequenceDiagram
    Notebook repo->>Workflow: Notebook change triggered
    Workflow->>Notebook2REST: Parse notebook
    Notebook2REST->>Workflow: Generate FastAPI, build image
    Workflow->>ECR:Push new image
    Workflow->>AWS Cluster: redeploy helm chart with new image

```
