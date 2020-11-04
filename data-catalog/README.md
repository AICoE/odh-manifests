# DH-Data-Catalog

This repo contains our OpenShift templates for deploying our Data Catalog cluster.

## Components in this repo

This repo contains deployment artifacts for all components associated with
the internal Data Hub's data-catalog deployment. This includes hue and thriftserver.

The deployment instructions that follow deploy all of the above components.

## Deployment Instructions

### Deploy Manually to Dev

Run the following commands to deploy the cluster to your environment.
```
oc new-project dh-dev-analytics-factory
oc project dh-dev-analytics-factory
kustomize build data-catalog/overlays/dev/ --enable_alpha_plugins | oc -n dh-dev-analytics-factory apply -f -
```
