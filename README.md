# Skupper MySQL Hello World

A minimal HTTP application deployed on a Kubernetes cluster using [Skupper](https://skupper.io/) to query a database running locally.

* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Step 1: Configure console session](#step-1-configure-console-session)
* [Step 2: Log in to your clusters](#step-2-log-in-to-your-clusters)
* [Step 3: Set the current namespaces](#step-3-set-the-current-namespaces)
* [Step 4: Install Skupper in your namespaces](#step-4-install-skupper-in-your-namespaces)
* [Step 5: Deploy the frontend application](#step-5-deploy-the-frontend-application)
* [Step 6: Expose the frontend](#step-6-expose-the-frontend)
* [Step 7: Create a Skupper gateway](#step-7-create-a-skupper-gateway)
* [Step 8: Test access](#step-8-test-access)

## Overview

This example is a simple application that shows how you can
use Skupper to access a local database at a remote site without
exposing it to the public internet.

It contains one service:

* A MySQL database running locally.

The example uses one Kubernetes namespace, "public",
to represent the public cloud.

## Prerequisites

* The `kubectl` command-line tool, version 1.15 or later
([installation guide][install-kubectl])

* The `skupper` command-line tool, the latest version ([installation
guide][install-skupper])

* Access to a Kubernetes namespace, from any provider you choose,
on any cluster you choose

[install-kubectl]: https://kubernetes.io/docs/tasks/tools/install-kubectl/
[install-skupper]: https://skupper.io/start/index.html#step-1-install-the-skupper-command-line-tool-in-your-environment

## Step 1: Configure console session

The `skupper` command uses your
[kubeconfig][kubeconfig] and current context to select the namespace
where it operates.

Console for _public_:

~~~ shell
export KUBECONFIG=~/.kube/config-public
~~~

## Step 2: Log in to your clusters

The methods for logging in vary by Kubernetes provider.  Find
the instructions for your chosen providers and use them to
authenticate and configure access for each console session.  See
the following links for more information:

* [Minikube](https://skupper.io/start/minikube.html#logging-in)
* [Amazon Elastic Kubernetes Service (EKS)](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
* [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster)
* [Google Kubernetes Engine (GKE)](https://skupper.io/start/gke.html#logging-in)
* [IBM Kubernetes Service](https://skupper.io/start/ibmks.html#logging-in)
* [OpenShift](https://skupper.io/start/openshift.html#logging-in)


## Step 3: Set the current namespaces

Use `kubectl create namespace` to create the namespaces you wish to
use (or use existing namespaces).  Use `kubectl config set-context` to
set the current namespace for each session.


Console for _public_:

~~~ shell
kubectl create namespace public
kubectl config set-context --current --namespace public
~~~

## Step 4: Install Skupper in your namespaces

The `skupper init` command installs the Skupper router and service
controller in the current namespace.  Run the `skupper init` command
in each namespace.

[minikube-tunnel]: https://skupper.io/start/minikube.html#running-minikube-tunnel

**Note:** If you are using Minikube, [you need to start `minikube
tunnel`][minikube-tunnel] before you install Skupper.


Console for _public_:

~~~ shell
skupper init
~~~

## Step 5: Deploy the frontend application

Console for _public_:

~~~ shell
kubectl create deployment hello-mysql-frontend --image quay.io/pwright/hello-mysql-frontend
~~~

## Step 6: Expose the frontend

Console for _public_:

~~~ shell
kubectl get services
~~~

## Step 7: Create a Skupper gateway

Creating a link requires use of two `skupper` commands in conjunction,
`skupper token create` and `skupper link create`.

The `skupper token create` command generates a secret token that
signifies permission to create a link.  The token also carries the
link details.  The `skupper link create` command then uses the link
token to create a link to the namespace that generated it.

**Note:** The link token is truly a *secret*.  Anyone who has the
token can link to your namespace.  Make sure that only those you trust
have access to it.


Console for _public_:

~~~ shell
skupper gateway create mydb localhost 3306
~~~

## Step 8: Test access

Console for _public_:

~~~ shell
kubectl
~~~