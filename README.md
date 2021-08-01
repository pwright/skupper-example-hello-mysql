# Skupper MySQL Hello World

A minimal HTTP application deployed on a Kubernetes cluster using [Skupper](https://skupper.io/) to query a database running locally.

* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Step 1: Configure console session](#step-1-configure-console-session)
* [Step 2: Log in to your clusters](#step-2-log-in-to-your-clusters)
* [Step 3: Set the current namespaces](#step-3-set-the-current-namespaces)
* [Step 4: Install Skupper in your namespaces](#step-4-install-skupper-in-your-namespaces)
* [Step 5: Create a Skupper gateway](#step-5-create-a-skupper-gateway)
* [Step 6: Deploy the frontend application](#step-6-deploy-the-frontend-application)
* [Step 7: Expose the message broker](#step-7-expose-the-message-broker)
* [Step 8: Run the client](#step-8-run-the-client)

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

Skupper is designed for use with multiple namespaces, typically on
different clusters.  The `skupper` command uses your
[kubeconfig][kubeconfig] and current context to select the namespace
where it operates.

[kubeconfig]: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/

Your kubeconfig is stored in a file in your home directory.  The
`skupper` and `kubectl` commands use the `KUBECONFIG` environment
variable to locate it.

A single kubeconfig supports only one active context per user.
Since you will be using multiple contexts at once in this
exercise, you need to create distinct kubeconfigs.

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each
session.


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

## Step 5: Create a Skupper gateway

Creating a gateway allows you expose your local service on the service network.


Console for _public_:

~~~ shell
skupper token create ~/public.token
~~~

## Step 6: Deploy the frontend application

Console for _public_:

~~~ shell
kubectl apply -f broker1.yaml
~~~

## Step 7: Expose the message broker

Console for _public_:

~~~ shell
kubectl get services
~~~

## Step 8: Run the client

Console for _public_:

~~~ shell
kubectl run client --attach --rm --restart Never --image quay.io/skupper/activemq-example-client --env SERVER=broker1
~~~