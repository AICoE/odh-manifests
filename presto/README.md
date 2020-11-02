# DH-Presto

This repo contains our OpenShift templates for deploying our Presto
cluster.

## Components in this repo

This repo contains deployment artifacts for all components associated with
the internal Data Hub's Presto deployment. The list of components deployed
are the following:

  1. Presto Operator Subscription and operator group definititon.
  2. Presto Cluster CRD.
  3. Secret to connect to the ceph s3 bucket.

The deployment instructions that follow deploy all of the above components.

## Deployment Instructions

### Deploy Manually

Run the following commands to deploy the cluster to your environment.
```
oc new-project dh-dev-presto
oc project dh-dev-presto
kustomize build presto/overlays/dev/ --enable_alpha_plugins | oc -n dh-dev-presto apply -f -
```

## Further Documentation

### Installation Issues

If you get the following error:
`error: unable to recognize "STDIN": no matches for kind "Presto" in version "starburstdata.com/v1"`
Wait a few minutes for the operator to generate the necessary CRDs and then run the command again.
