# Amazon EKS Complete Guide

> A practical guide to Amazon Elastic Kubernetes Service, Kubernetes fundamentals, EKS architecture, deployment workflows, commands, security, troubleshooting, and the concepts used in the Day 14 project.

---

# 1. What is Kubernetes?

Kubernetes is a container orchestration platform.

Docker solves the problem of packaging and running containers. Kubernetes solves the larger problem of managing many containers across machines.

A simple example:

```text
Without Kubernetes

Server
 ├── Container 1
 ├── Container 2
 └── Container 3
```

As the application grows, you may need:

- multiple containers
- multiple servers
- automatic recovery
- load balancing
- scaling
- rolling updates
- service discovery

Kubernetes provides mechanisms for these tasks.

---

# 2. Why Kubernetes?

Suppose an application has three container instances:

```text
             Application
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      Pod 1     Pod 2     Pod 3
```

If Pod 2 crashes, Kubernetes can create another pod.

If traffic increases, the application can be scaled to more replicas.

Kubernetes is therefore an orchestration layer around containers.

---

# 3. What is Amazon EKS?

Amazon Elastic Kubernetes Service (EKS) is AWS's managed Kubernetes service.

Instead of manually building and maintaining an entire Kubernetes control plane, AWS manages the Kubernetes control plane for you.

You still work with Kubernetes concepts such as:

- Pods
- Deployments
- Services
- Namespaces
- RBAC
- ConfigMaps
- Secrets
- Probes
- Resource requests and limits

---

# 4. Kubernetes vs Docker

Docker and Kubernetes are not direct replacements for each other.

### Docker

Docker is primarily used to:

- build container images
- distribute images
- run containers

### Kubernetes

Kubernetes is used to:

- manage containers at scale
- schedule workloads
- maintain desired replicas
- expose applications
- recover failed workloads
- perform rolling deployments
- manage cluster resources

A common workflow is:

```text
Application
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Container Registry
    ↓
Kubernetes
    ↓
Pods
```

---

# 5. EKS Architecture

A simplified EKS architecture is:

```text
                    AWS
                     │
             ┌───────┴────────┐
             │   EKS Cluster  │
             └───────┬────────┘
                     │
              Control Plane
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Worker      Worker      Worker
        Node        Node        Node
          │          │
        Pods       Pods
```

The main parts are:

- EKS control plane
- worker nodes
- Kubernetes API server
- scheduler
- controllers
- etcd
- Kubernetes workloads

---

# 6. EKS Control Plane

The control plane is responsible for managing the Kubernetes cluster.

Important components include:

### Kubernetes API Server

The API server is the main communication interface for Kubernetes.

Tools such as `kubectl` communicate with the API server.

### Scheduler

The scheduler decides which node should run a newly created pod.

### Controllers

Controllers continuously compare the desired state with the current state and take actions to move the cluster toward the desired state.

### etcd

etcd is Kubernetes' distributed key-value data store for cluster state.

In Amazon EKS, AWS manages the EKS control plane components.

---

# 7. Worker Nodes

Worker nodes are the machines where application pods run.

For example:

```text
EKS Cluster
│
├── Node 1
│    ├── Pod A
│    └── Pod B
│
└── Node 2
     ├── Pod C
     └── Pod D
```

Worker nodes need the resources required to run workloads, including CPU and memory.

---

# 8. EKS Node Groups

An EKS cluster can use different approaches for compute.

### Managed Node Groups

AWS manages important parts of the worker-node lifecycle.

### Self-Managed Nodes

You manage the EC2 worker nodes more directly.

### Fargate

AWS can run Kubernetes pods without you managing the underlying worker EC2 instances.

Each approach has different operational and cost characteristics.

---

# 9. Cluster

A Kubernetes cluster is the complete environment in which Kubernetes workloads run.

It contains:

- control plane
- worker nodes
- Kubernetes resources
- networking
- workloads

An EKS cluster is an AWS-managed Kubernetes cluster.

---

# 10. Pod

A Pod is the smallest deployable unit in Kubernetes.

A pod can contain one or more containers.

Typical application:

```text
Pod
└── Application Container
```

Pods receive their own network identity within the Kubernetes networking model.

Pods are generally considered replaceable rather than permanent machines.

---

# 11. Container

A container is a running instance of a container image.

For example:

```text
Docker Image
     ↓
Container
     ↓
Pod
```

Kubernetes schedules pods, and containers run inside those pods.

---

# 12. Deployment

A Deployment describes the desired state for an application.

Example:

```yaml
spec:
  replicas: 3
```

This tells Kubernetes that three replicas should be maintained.

Conceptually:

```text
Deployment
    │
    ▼
ReplicaSet
    │
    ├── Pod 1
    ├── Pod 2
    └── Pod 3
```

If one pod disappears, the Deployment's controllers work to restore the desired replica count.

---

# 13. ReplicaSet

A ReplicaSet maintains a specified number of pod replicas.

Deployments normally manage ReplicaSets for you.

You usually work with Deployments rather than manually creating ReplicaSets.

---

# 14. Namespace

A namespace provides logical separation inside a Kubernetes cluster.

Example:

```text
Cluster
│
├── default
├── monitoring
└── eks-demo
```

The Day 14 project uses:

```text
eks-demo
```

This keeps its resources organized.

Commands:

```bash
kubectl get namespaces
```

```bash
kubectl get pods -n eks-demo
```

---

# 15. Kubernetes Service

Pods are replaceable, so their IP addresses can change.

A Service provides a stable way to reach a group of pods.

Example:

```text
Service
   │
   ├── Pod 1
   ├── Pod 2
   └── Pod 3
```

The Service selects pods using labels.

Example:

```yaml
selector:
  app: eks-demo
```

---

# 16. Service Types

Common Kubernetes Service types include:

### ClusterIP

The default Service type.

Provides internal cluster access.

### NodePort

Exposes a service through a port on each node.

### LoadBalancer

Requests an external load balancer from the underlying cloud provider.

The Day 14 project uses:

```yaml
type: LoadBalancer
```

---

# 17. AWS Load Balancer with EKS

With a LoadBalancer Service, AWS can provision a load-balancing resource for the Kubernetes Service.

The project uses an AWS Network Load Balancer annotation:

```yaml
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
```

The resulting traffic flow is:

```text
Internet
   ↓
AWS Network Load Balancer
   ↓
Kubernetes Service
   ↓
Pods
```

---

# 18. Labels and Selectors

Labels are key-value metadata attached to Kubernetes resources.

Example:

```yaml
labels:
  app: eks-demo
```

A selector can find resources using that label:

```yaml
selector:
  app: eks-demo
```

This is how the Service identifies the pods to which it should send traffic.

---

# 19. Container Registry

Kubernetes needs access to the container image.

A container registry stores images so worker nodes can pull them.

AWS provides:

**Amazon Elastic Container Registry (ECR)**.

Workflow:

```text
Docker Build
    ↓
Docker Image
    ↓
Amazon ECR
    ↓
EKS Node
    ↓
Pod
```

---

# 20. Amazon ECR + EKS

Create an ECR repository:

```bash
aws ecr create-repository   --repository-name eks-demo   --region us-east-1
```

Authenticate Docker:

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

Build an x86_64 image on an Apple Silicon Mac:

```bash
docker build --platform linux/amd64   -t eks-demo:latest .
```

Tag:

```bash
docker tag eks-demo:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/eks-demo:latest
```

Push:

```bash
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/eks-demo:latest
```

Verify:

```bash
aws ecr describe-images   --repository-name eks-demo   --region us-east-1
```

---

# 21. Why `linux/amd64` Matters

Apple Silicon Macs use ARM64 architecture.

Many traditional EC2 instance types use x86_64/AMD64 architecture.

If the image architecture does not match the node architecture, Kubernetes may fail to start the container.

For x86_64 nodes:

```bash
docker build --platform linux/amd64 -t eks-demo .
```

Always consider both:

```text
Developer machine architecture
            vs
Kubernetes node architecture
```

---

# 22. kubectl

`kubectl` is the command-line tool used to communicate with Kubernetes.

Check the client:

```bash
kubectl version --client
```

Get nodes:

```bash
kubectl get nodes
```

Get pods:

```bash
kubectl get pods
```

Get pods in a namespace:

```bash
kubectl get pods -n eks-demo
```

Get services:

```bash
kubectl get svc -n eks-demo
```

Get deployments:

```bash
kubectl get deployments -n eks-demo
```

---

# 23. kubectl describe

`describe` provides detailed information about a Kubernetes resource.

Example:

```bash
kubectl describe pod <pod-name> -n eks-demo
```

This is especially useful when troubleshooting:

- scheduling
- image pulls
- probes
- mounts
- events
- container failures

---

# 24. kubectl logs

View container logs:

```bash
kubectl logs <pod-name> -n eks-demo
```

For a pod with multiple containers:

```bash
kubectl logs <pod-name> -c <container-name> -n eks-demo
```

Logs are one of the first places to look when an application container fails.

---

# 25. kubectl exec

Execute a command inside a running container:

```bash
kubectl exec -it <pod-name> -n eks-demo -- /bin/sh
```

The exact shell depends on the container image.

---

# 26. kubectl apply

Apply Kubernetes manifests:

```bash
kubectl apply -f k8s/
```

Apply a specific file:

```bash
kubectl apply -f k8s/deployment.yaml
```

---

# 27. kubectl delete

Delete resources defined in manifests:

```bash
kubectl delete -f k8s/
```

Delete a specific pod:

```bash
kubectl delete pod <pod-name> -n eks-demo
```

Deleting a pod managed by a Deployment normally causes the Deployment to create a replacement.

---

# 28. eksctl

`eksctl` is a command-line tool designed specifically for creating and managing EKS clusters.

Check it:

```bash
eksctl version
```

Create a cluster:

```bash
eksctl create cluster   --name eks-demo   --region us-east-1   --nodes 2   --node-type t3.small
```

Delete:

```bash
eksctl delete cluster   --name eks-demo   --region us-east-1
```

---

# 29. Kubernetes Manifests

Kubernetes resources are commonly described using YAML files.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eks-demo
```

The important fields usually include:

- `apiVersion`
- `kind`
- `metadata`
- `spec`

---

# 30. Namespace Manifest

Example:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: eks-demo
```

This creates the project's namespace.

---

# 31. Deployment Manifest

A simplified Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eks-demo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: eks-demo
```

The Deployment then defines the pod template.

---

# 32. ServiceAccount

A ServiceAccount provides an identity to a pod.

Example:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eks-demo
  namespace: eks-demo
```

The Day 14 application uses its ServiceAccount when communicating with the Kubernetes API.

---

# 33. RBAC

RBAC means:

**Role-Based Access Control**

It determines what an identity is allowed to do.

The project intentionally uses read-only permissions.

Example:

```yaml
verbs:
  - get
  - list
```

The dashboard can read resources but cannot create, modify, or delete them.

---

# 34. Role

A Role defines permissions within a namespace.

The project grants access to selected resources such as:

```text
pods
services
events
deployments
```

with:

```text
get
list
```

permissions.

---

# 35. RoleBinding

A RoleBinding connects a Role to an identity such as a ServiceAccount.

Conceptually:

```text
ServiceAccount
      ↓
RoleBinding
      ↓
Role
      ↓
Permissions
```

---

# 36. ClusterRole

Some resources are cluster-scoped.

Nodes are an example.

The project therefore uses a ClusterRole for read-only node access.

```text
ClusterRole
    ↓
nodes
    ↓
get / list
```

---

# 37. ClusterRoleBinding

A ClusterRoleBinding connects a ClusterRole to an identity.

In the project:

```text
eks-demo ServiceAccount
          ↓
ClusterRoleBinding
          ↓
eks-demo-node-reader
          ↓
get/list nodes
```

---

# 38. Readiness Probe

A readiness probe answers:

> Is this container ready to receive traffic?

The project uses:

```text
/healthz
```

Example:

```yaml
readinessProbe:
  httpGet:
    path: /healthz
    port: 8000
```

If a pod is not ready, Kubernetes can prevent normal service traffic from being sent to it.

---

# 39. Liveness Probe

A liveness probe answers:

> Is this container still functioning?

Example:

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8000
```

If Kubernetes determines that a container is unhealthy according to the liveness configuration, the kubelet can restart it.

---

# 40. Startup Probe

A startup probe is useful for applications that take a long time to initialize.

It gives an application time to start before liveness checking becomes active.

The Day 14 project uses readiness and liveness probes; startup probes were not required for this application.

---

# 41. Resource Requests

Requests tell Kubernetes the resources a container needs for scheduling.

Example:

```yaml
requests:
  cpu: 50m
  memory: 64Mi
```

Kubernetes uses requests when making scheduling decisions.

---

# 42. Resource Limits

Limits restrict how much CPU and memory a container can consume.

Example:

```yaml
limits:
  cpu: 250m
  memory: 256Mi
```

Requests and limits are different:

```text
Request = resource expectation for scheduling
Limit   = resource ceiling
```

---

# 43. Replicas

A Deployment can run multiple copies of an application.

Example:

```yaml
replicas: 3
```

Conceptually:

```text
Deployment
 ├── Pod 1
 ├── Pod 2
 └── Pod 3
```

Multiple replicas can improve availability and allow traffic to be distributed between instances.

---

# 44. Topology Spread Constraints

The Day 14 Deployment uses topology spread constraints.

The purpose is to avoid placing all replicas unnecessarily close together when Kubernetes can distribute them.

The project uses:

```yaml
topologyKey: kubernetes.io/hostname
```

This uses node hostname as the topology domain.

The configuration uses:

```yaml
whenUnsatisfiable: ScheduleAnyway
```

This tells the scheduler that the spread preference should not prevent scheduling if the ideal distribution cannot be achieved.

---

# 45. Downward API

The Kubernetes Downward API allows a container to receive information about itself from Kubernetes.

The project uses it for values such as:

- pod name
- namespace
- pod IP
- node name

Example:

```yaml
- name: POD_NAME
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
```

This is useful when an application needs to know its own Kubernetes identity.

---

# 46. Kubernetes API

Applications inside Kubernetes can communicate with the Kubernetes API.

The Day 14 dashboard uses this to read cluster information.

Conceptually:

```text
Dashboard Pod
     │
     ▼
ServiceAccount
     │
     ▼
RBAC
     │
     ▼
Kubernetes API
     │
     ├── Pods
     ├── Nodes
     ├── Deployments
     └── Events
```

Because the application's permissions are read-only, it cannot use this access to modify the cluster.

---

# 47. Container Security

The project applies several container security settings.

### Non-root

```yaml
runAsNonRoot: true
```

### Fixed user

```yaml
runAsUser: 10001
```

### No privilege escalation

```yaml
allowPrivilegeEscalation: false
```

### Read-only filesystem

```yaml
readOnlyRootFilesystem: true
```

### Drop capabilities

```yaml
capabilities:
  drop:
    - ALL
```

These settings reduce the privileges available to the application container.

---

# 48. Complete EKS Deployment Workflow

The complete workflow used in this project is:

```text
                 Developer
                     │
                     ▼
             FastAPI Application
                     │
                     ▼
                Dockerfile
                     │
                     ▼
              Docker Image
                     │
                     ▼
              Amazon ECR
                     │
                     ▼
              Amazon EKS
                     │
             ┌───────┴───────┐
             ▼               ▼
          Node 1           Node 2
             │               │
             └───────┬───────┘
                     ▼
                Kubernetes
                 Deployment
                     │
              ┌──────┼──────┐
              ▼      ▼      ▼
             Pod    Pod    Pod
              └──────┼──────┘
                     ▼
                Kubernetes
                  Service
                     │
                     ▼
             Network Load Balancer
                     │
                     ▼
                  Browser
```

---

# 49. Complete Hands-On Workflow

## Step 1: Verify tools

```bash
aws --version
kubectl version --client
eksctl version
docker --version
```

## Step 2: Verify AWS identity

```bash
aws sts get-caller-identity
```

## Step 3: Check AWS region

```bash
aws configure get region
```

## Step 4: Create ECR repository

```bash
aws ecr create-repository   --repository-name eks-demo   --region us-east-1
```

## Step 5: Login to ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

## Step 6: Build image

For x86_64 EKS nodes:

```bash
docker build --platform linux/amd64   -t eks-demo:latest .
```

## Step 7: Tag image

```bash
docker tag eks-demo:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/eks-demo:latest
```

## Step 8: Push image

```bash
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/eks-demo:latest
```

## Step 9: Verify ECR

```bash
aws ecr describe-images   --repository-name eks-demo   --region us-east-1
```

## Step 10: Create EKS cluster

```bash
eksctl create cluster   --name eks-demo   --region us-east-1   --nodes 2   --node-type t3.small
```

## Step 11: Verify nodes

```bash
kubectl get nodes
```

## Step 12: Apply Kubernetes resources

```bash
kubectl apply -f k8s/
```

## Step 13: Check pods

```bash
kubectl get pods -n eks-demo
```

## Step 14: Check service

```bash
kubectl get svc -n eks-demo
```

## Step 15: Check deployment

```bash
kubectl get deployment -n eks-demo
```

## Step 16: Access the Load Balancer

Wait until the Service receives an external address:

```bash
kubectl get svc eks-demo -n eks-demo
```

Then open the external address in a browser.

---

# 50. Verification Checklist

After deployment, verify:

```bash
kubectl get nodes
```

Expected:

```text
STATUS: Ready
```

Check pods:

```bash
kubectl get pods -n eks-demo
```

Expected:

```text
3 application replicas
```

Check service:

```bash
kubectl get svc -n eks-demo
```

Expected:

```text
TYPE: LoadBalancer
```

Check deployment:

```bash
kubectl get deployment -n eks-demo
```

Expected:

```text
AVAILABLE: 3
```

---

# 51. Useful kubectl Commands

List everything in the namespace:

```bash
kubectl get all -n eks-demo
```

List pods with node information:

```bash
kubectl get pods -n eks-demo -o wide
```

List events:

```bash
kubectl get events -n eks-demo
```

Watch pods:

```bash
kubectl get pods -n eks-demo -w
```

Describe deployment:

```bash
kubectl describe deployment eks-demo -n eks-demo
```

Describe service:

```bash
kubectl describe service eks-demo -n eks-demo
```

View logs:

```bash
kubectl logs <pod-name> -n eks-demo
```

View previous container logs:

```bash
kubectl logs <pod-name> -n eks-demo --previous
```

Check rollout:

```bash
kubectl rollout status deployment/eks-demo -n eks-demo
```

Restart deployment:

```bash
kubectl rollout restart deployment/eks-demo -n eks-demo
```

---

# 52. Scaling

A Deployment can be scaled manually:

```bash
kubectl scale deployment eks-demo   --replicas=5   -n eks-demo
```

Verify:

```bash
kubectl get pods -n eks-demo
```

The Day 14 project uses three replicas as its configured baseline.

---

# 53. Horizontal Pod Autoscaler

The Horizontal Pod Autoscaler (HPA) can adjust the number of pod replicas based on resource utilization or other supported metrics.

Conceptually:

```text
Low load
   ↓
Fewer pods

High load
   ↓
More pods
```

HPA is an important Kubernetes scaling concept, although it is not configured in this Day 14 project.

---

# 54. Cluster Autoscaling

Pod scaling and node scaling are different problems.

### Pod scaling

Changes the number of application pods.

### Node scaling

Changes the amount of compute available to the cluster.

Tools and approaches used in EKS environments can include:

- Cluster Autoscaler
- Karpenter
- EKS managed node groups

These are related concepts rather than components configured in this project.

---

# 55. Troubleshooting: ImagePullBackOff

If a pod cannot pull its image:

```bash
kubectl get pods -n eks-demo
```

You may see:

```text
ImagePullBackOff
```

Check:

```bash
kubectl describe pod <pod-name> -n eks-demo
```

Common causes:

- incorrect ECR image URI
- image does not exist
- incorrect image tag
- registry authentication/permissions
- architecture mismatch

For an Apple Silicon development machine, verify the image architecture when using x86_64 nodes.

---

# 56. Troubleshooting: CrashLoopBackOff

If the container repeatedly starts and crashes:

```bash
kubectl get pods -n eks-demo
```

Check logs:

```bash
kubectl logs <pod-name> -n eks-demo
```

Then inspect the pod:

```bash
kubectl describe pod <pod-name> -n eks-demo
```

Possible causes include:

- application startup failure
- missing environment variables
- incorrect command
- filesystem permissions
- application configuration problems

---

# 57. Troubleshooting: Pending Pod

A pod may remain in:

```text
Pending
```

Inspect it:

```bash
kubectl describe pod <pod-name> -n eks-demo
```

Look at the Events section.

Possible causes include:

- insufficient CPU
- insufficient memory
- scheduling constraints
- node availability
- taints and tolerations

---

# 58. Troubleshooting: Readiness Probe Failure

If the readiness probe fails, check:

```bash
kubectl describe pod <pod-name> -n eks-demo
```

Verify:

- application is running
- port is correct
- `/healthz` exists
- application listens on the expected interface
- startup timing is sufficient

The project uses:

```text
0.0.0.0:8000
```

and:

```text
/healthz
```

---

# 59. Troubleshooting: Load Balancer

Check the Service:

```bash
kubectl get svc -n eks-demo
```

If the external address is not available, inspect:

```bash
kubectl describe svc eks-demo -n eks-demo
```

Then inspect Kubernetes events:

```bash
kubectl get events -n eks-demo
```

---

# 60. Troubleshooting: RBAC

If the dashboard cannot read Kubernetes resources, verify the ServiceAccount:

```bash
kubectl get serviceaccount -n eks-demo
```

Check Roles:

```bash
kubectl get role -n eks-demo
```

Check RoleBindings:

```bash
kubectl get rolebinding -n eks-demo
```

Check ClusterRole:

```bash
kubectl get clusterrole
```

Check ClusterRoleBinding:

```bash
kubectl get clusterrolebinding
```

The project intentionally grants only the permissions required for read-only dashboard functionality.

---

# 61. Security Best Practices

Important Kubernetes security practices include:

- use least-privilege RBAC
- avoid running containers as root
- restrict container capabilities
- disable unnecessary privilege escalation
- use read-only filesystems where possible
- keep images updated
- avoid embedding secrets in images
- restrict network exposure
- use namespaces for logical isolation
- monitor cluster activity
- protect the Kubernetes API
- use private networking where appropriate for production architectures

The Day 14 project demonstrates several of these principles.

---

# 62. Secrets

Sensitive information should not normally be hard-coded into application images or source code.

Kubernetes provides Secret resources for sensitive configuration.

For example:

```text
Database password
API credential
Application secret
```

should be handled through an appropriate secret-management approach.

For production AWS workloads, AWS-native secret-management solutions can also be considered.

Secrets were not required by the Day 14 dashboard itself.

---

# 63. ConfigMaps

ConfigMaps provide non-sensitive configuration data.

Typical examples include:

```text
environment names
feature flags
application configuration
```

Secrets and ConfigMaps can be provided to containers through environment variables or mounted files.

---

# 64. Storage in EKS

Containers are generally ephemeral.

For persistent application data, Kubernetes provides storage abstractions such as:

```text
PersistentVolume
PersistentVolumeClaim
StorageClass
```

On AWS, EBS-backed storage is commonly used for block-storage workloads.

The Day 14 dashboard does not require persistent application storage.

---

# 65. Networking Concepts to Remember

A simplified Kubernetes networking model is:

```text
Pod IP
  ↓
Service
  ↓
Load Balancer
  ↓
External Client
```

Important concepts include:

- Pod networking
- Service discovery
- ClusterIP
- LoadBalancer
- DNS
- security groups
- VPC networking

EKS integrates Kubernetes workloads with AWS networking.

---

# 66. Desired State

One of the most important Kubernetes concepts is desired state.

Suppose you declare:

```yaml
replicas: 3
```

You are telling Kubernetes:

> I want three replicas.

Kubernetes continuously works toward that desired state.

If one pod disappears:

```text
Desired: 3
Current: 2
```

Controllers can create another pod.

```text
Desired: 3
Current: 3
```

This controller-based model is fundamental to Kubernetes.

---

# 67. Declarative vs Imperative Management

### Declarative

You define what the desired state should be:

```bash
kubectl apply -f deployment.yaml
```

### Imperative

You directly request an action:

```bash
kubectl scale deployment eks-demo   --replicas=5   -n eks-demo
```

Kubernetes commonly encourages declarative configuration through manifests and version-controlled YAML.

---

# 68. Rolling Updates

Deployments support controlled application updates.

A common workflow is:

```text
Old Pods
   ↓
New Pods gradually start
   ↓
Traffic moves to healthy Pods
   ↓
Old Pods terminate
```

This helps avoid taking the entire application offline during normal updates.

Useful command:

```bash
kubectl rollout status deployment/eks-demo -n eks-demo
```

---

# 69. Rollback

If a Deployment update causes a problem, Kubernetes Deployment history can be used for rollback when revisions are available.

Check history:

```bash
kubectl rollout history deployment/eks-demo -n eks-demo
```

Rollback:

```bash
kubectl rollout undo deployment/eks-demo -n eks-demo
```

---

# 70. Production Considerations

The Day 14 project is a learning and portfolio deployment.

A production EKS environment would normally require additional considerations such as:

- authentication and authorization
- private networking
- ingress architecture
- TLS
- secret management
- centralized logging
- monitoring
- alerting
- image vulnerability scanning
- backup and disaster recovery
- autoscaling
- cost controls
- network policies
- infrastructure as code
- CI/CD
- multi-AZ architecture

These topics extend beyond the scope of this project.

---

# 71. Cost Awareness

AWS resources can generate charges while they are running.

An EKS learning cluster can involve multiple billable resources, depending on the architecture and configuration.

After completing a temporary lab, clean up resources that are no longer needed.

For this project:

```bash
kubectl delete -f k8s/
```

Then:

```bash
eksctl delete cluster   --name eks-demo   --region us-east-1
```

Also verify that no other lab resources were left running.

---

# 72. Complete Cleanup

Delete Kubernetes resources:

```bash
kubectl delete -f k8s/
```

Delete the EKS cluster:

```bash
eksctl delete cluster   --name eks-demo   --region us-east-1
```

If the ECR repository is no longer needed, it can also be removed:

```bash
aws ecr delete-repository   --repository-name eks-demo   --region us-east-1
```

Only delete resources that you are certain are no longer needed.

---

# 73. Day 14 Project Mapping

The concepts used directly in the project are:

| EKS/Kubernetes Concept | Used in Project |
|---|---|
| EKS | Yes |
| ECR | Yes |
| Docker | Yes |
| Pods | Yes |
| Deployment | Yes |
| Service | Yes |
| LoadBalancer | Yes |
| Namespace | Yes |
| ServiceAccount | Yes |
| RBAC | Yes |
| Role | Yes |
| ClusterRole | Yes |
| RoleBinding | Yes |
| ClusterRoleBinding | Yes |
| Readiness Probe | Yes |
| Liveness Probe | Yes |
| Resource Requests | Yes |
| Resource Limits | Yes |
| Downward API | Yes |
| Kubernetes API | Yes |
| Topology Spread Constraints | Yes |
| HPA | Not configured |
| Karpenter | Not configured |
| Persistent Storage | Not required |
| ConfigMap | Not required |
| Secret | Not required |

---

# 74. Important Mental Model

Remember the following hierarchy:

```text
AWS
 │
 └── EKS Cluster
       │
       ├── Control Plane
       │
       └── Worker Nodes
             │
             └── Pods
                   │
                   └── Containers
```

And for exposing an application:

```text
Internet
   ↓
AWS Load Balancer
   ↓
Kubernetes Service
   ↓
Pods
   ↓
Containers
```

And for deploying an image:

```text
Source Code
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Amazon ECR
    ↓
EKS Node pulls Image
    ↓
Pod starts Container
```

These three diagrams are the core mental model for this project.

---

# 75. Interview Questions

### What is Amazon EKS?

EKS is AWS's managed Kubernetes service.

### What is a Pod?

A Pod is Kubernetes' smallest deployable unit and can contain one or more containers.

### What is a Deployment?

A Deployment manages the desired state and replicas of an application.

### Why do we use a Service?

A Service provides a stable networking abstraction for reaching a group of pods.

### Why use a LoadBalancer Service?

It allows the application to be exposed through a cloud load balancer.

### What is ECR?

Amazon Elastic Container Registry is AWS's container image registry.

### What is RBAC?

Role-Based Access Control defines which actions an identity can perform on Kubernetes resources.

### Why does the project use a ServiceAccount?

The application uses a ServiceAccount identity to authenticate to the Kubernetes API from inside the cluster.

### Why is the application's RBAC read-only?

The dashboard only needs to read cluster information, so it does not need permissions to modify resources.

### What is a readiness probe?

It tells Kubernetes whether a container is ready to receive traffic.

### What is a liveness probe?

It helps Kubernetes determine whether a container is still functioning.

### Why build `linux/amd64` on an Apple Silicon Mac?

The development machine is ARM64 while the selected EKS worker nodes are x86_64, so the image must be compatible with the node architecture.

### What happens when a pod crashes?

A controller such as a Deployment's ReplicaSet works to restore the desired number of replicas.

### What is the difference between scaling pods and scaling nodes?

Pod scaling changes application replicas. Node scaling changes the compute capacity available to run workloads.

---

# 76. Final Takeaways

The most important concepts to remember from EKS are:

```text
EKS
 ↓
Managed Kubernetes Control Plane

Node
 ↓
Runs Pods

Pod
 ↓
Runs Containers

Deployment
 ↓
Maintains Desired Replicas

Service
 ↓
Provides Stable Access to Pods

LoadBalancer
 ↓
Provides External Access

ECR
 ↓
Stores Container Images

ServiceAccount + RBAC
 ↓
Controls Kubernetes API Permissions

Probes
 ↓
Help Kubernetes Manage Application Health

Requests/Limits
 ↓
Control Resource Expectations

Downward API
 ↓
Provides Pod Metadata to the Container
```

The Day 14 project combines these concepts into a complete deployment:

```text
FastAPI
   ↓
Docker
   ↓
ECR
   ↓
EKS
   ↓
Kubernetes Deployment
   ↓
3 Pods
   ↓
Service
   ↓
Network Load Balancer
   ↓
Helm EKS Control Room
```

This is the core Cloud + DevOps workflow demonstrated by the project.
