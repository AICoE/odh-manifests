# SUPERSET

Helm deployment for the Data Hub's Superset instance

## Runbook

The Runbook for Superset can be found in the dh-runbooks repository at [SUPERSET.md](https://gitlab.cee.redhat.com/data-hub/dh-runbooks/blob/master/SUPERSET.md)

## Deployment Instructions

### Prerequisites

We use [helm](https://helm.sh/) to install our helm charts. We also need the helm secrets plugin.
To install these use the commands below:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

sudo helm plugin install https://github.com/zendesk/helm-secrets
```

We are using sops to encrypt and decrypt our secret variable files using the ArgoCD ksops key(s).
You can find the public key [here](http://keys.gnupg.net/pks/lookup?op=vindex&fingerprint=on&search=0xBD2C73FF891FBC7E).
For the private key please reach out to [Internal Datahub Devs](mailto:data-hub@redhat.com).

#### Deploy ArgoCD-Manager rolebinding

Before using ArgoCD to manage the Superset deployment in stage or
production, you must manually apply the ArgoCD-Manager rolebinding
contained in [superset/argocd-manager-rolebinding.yaml](superset/argocd-manager-rolebinding.yaml)

See [Kustomize](https://github.com/kubernetes-sigs/kustomize/tree/master/docs)
docs for more info.

#### Deploy ODH Operator

To deploy Superset we first need to deploy the ODH Operator.

Follow the steps in this repo to deploy the ODH Operator: [dh-internal-odh-install](https://gitlab.cee.redhat.com/data-hub/dh-internal-odh-install)

> **NOTE**: Superset requires an ODH image that was built from v0.5 or higher.

##### Note: The above step require cluster-admin

This should create the necessary CRDs, rolebindings and serviceaccounts and deploy the ODH Operator.

##### Note: Due to the nature of LDAP authentication. We must create an Admin user before any user logs in for the first time. This Admin user can then give Admin access to other users. Other users may log in normally using their LDAP credentials

```bash
oc rsh <superset-pod>
superset fab create-admin
Username [admin]: User1
User first name [admin]: User1
User last name [user]: UserLastName
Email [admin@fab.org]: User1@redhat.com
Password:
Repeat for confirmation:
```

### Deploying to Development

Run the following command from the `superset` folder of this repository to deploy
Superset in a development environment:

```bash
oc new-project dh-dev-superset
helm secrets install --generate-name -f secrets.enc.yaml -f helm_vars/dev/values.yaml -f helm_vars/dev/secrets.yaml
```

To update the current deployment run the following:

```bash
helm list
helm secrets upgrade -f secrets.enc.yaml -f helm_vars/dev/values.yaml -f helm_vars/dev/secrets.yaml <chart_name_from_previous_command>
```

### Deploying to Stage

Run the following command from the `superset` folder of this repository to deploy
Superset to stage:

```bash
helm secrets install --generate-name -f secrets.enc.yaml -f helm_vars/stage/values.yaml -f helm_vars/stage/secrets.yaml
```

To update the current deployment run the following:

```bash
helm list
helm secrets upgrade -f secrets.enc.yaml -f helm_vars/stage/values.yaml -f helm_vars/stage/secrets.yaml <chart_name_from_previous_command>
```

### Deploying to Production

Run the following command from the `superset` folder of this repository to deploy
Superset to production:

```bash
helm secrets install --generate-name -f secrets.enc.yaml -f helm_vars/prod/values.yaml -f helm_vars/prod/secrets.yaml
```

To update the current deployment run the following:

```bash
helm list
helm secrets upgrade -f secrets.enc.yaml -f helm_vars/prod/values.yaml -f helm_vars/prod/secrets.yaml <chart_name_from_previous_command>
```
