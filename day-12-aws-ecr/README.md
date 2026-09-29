# Amazon ECR — Elastic Container Registry

## 📌 Overview

Amazon Elastic Container Registry (ECR) is a fully managed AWS service used to **store, manage, and distribute container images**.

In this hands-on project, I created a private ECR repository, authenticated Docker with AWS ECR, pushed a Docker image to the repository, pulled the image back, and ran the application using the image stored in ECR.

---

## 🎯 Objectives

* Understand Amazon ECR
* Create a private ECR repository
* Authenticate Docker with ECR
* Tag a Docker image for ECR
* Push a Docker image to ECR
* Pull an image from ECR
* Run the ECR image as a Docker container
* Understand the relationship between Docker and ECR

---

## 🧠 What is Amazon ECR?

**Amazon Elastic Container Registry (ECR)** is an AWS-managed container registry.

It allows developers and DevOps engineers to store Docker/container images and make them available to services such as:

* Amazon ECS
* Amazon EKS
* Amazon EC2
* AWS Lambda

A simple way to think about ECR is:

> **ECR is a container image registry integrated with AWS.**

---

## 🏗️ ECR Architecture

```text
                    Developer
                        │
                        │
                        ▼
                 Dockerfile
                        │
                        ▼
                  Docker Image
                        │
                        │ docker push
                        ▼
              ┌───────────────────┐
              │    Amazon ECR     │
              │                   │
              │  cloud-shop       │
              │      │            │
              │      └── v1       │
              └─────────┬─────────┘
                        │
                        │ docker pull
                        ▼
                  Docker Engine
                        │
                        ▼
                Cloud Shop App
```

---

# 🔑 Important ECR Concepts

## 1. Repository

A repository is a location in ECR where container images are stored.

Example:

```text
cloud-shop
```

---

## 2. Image

A Docker image contains the application code, dependencies, libraries, and configuration required to create a container.

Example:

```text
cloud-shop:v1
```

---

## 3. Tag

A tag identifies a particular version of an image.

Examples:

```text
v1
v2
latest
production
```

In this lab:

```text
v1
```

was used as the image tag.

---

## 4. Push

**Push** means uploading a Docker image to ECR.

```text
Local Docker
     │
     │ docker push
     ▼
    ECR
```

---

## 5. Pull

**Pull** means downloading an image from ECR.

```text
    ECR
     │
     │ docker pull
     ▼
Local Docker
```

---

# 🧪 Hands-On Lab

## Step 1 — Check the Local Docker Image

First, I checked the Docker images available locally:

```bash
docker images
```

The Cloud Shop application image was available as:

```text
cloud-shop:latest
```

---

## Step 2 — Create an ECR Repository

I created a **private ECR repository** named:

```text
cloud-shop
```

Repository structure:

```text
Amazon ECR
└── cloud-shop
```

### 📸 Screenshot

![ECR Repository](01-ecr-repository.png)

---

## Step 3 — Authenticate Docker with ECR

Before pushing an image, Docker needs permission to communicate with the ECR registry.

I used:

```bash
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin \
830955873996.dkr.ecr.us-east-1.amazonaws.com
```

Successful authentication returned:

```text
Login Succeeded
```

### What this command does

```text
aws ecr get-login-password
        ↓
Generates an authentication token
        ↓
docker login
        ↓
Docker becomes authenticated with ECR
```

---

## Step 4 — Tag the Docker Image

The local Docker image:

```text
cloud-shop:latest
```

was tagged using the ECR repository URI:

```bash
docker tag cloud-shop:latest \
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

The resulting image name was:

```text
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

### Why do we tag the image?

Docker needs the ECR registry address in the image name so it knows where the image should be pushed.

The format is:

```text
<account-id>.dkr.ecr.<region>.amazonaws.com/<repository>:<tag>
```

For this project:

```text
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

---

## Step 5 — Push the Image to ECR

I pushed the Docker image to the ECR repository:

```bash
docker push \
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

Docker uploaded the image layers to Amazon ECR.

### 📸 Screenshot

![Docker Push](03-docker-push.png)

---

## Step 6 — Verify the Image in ECR

After the push completed, I opened:

**AWS Console → ECR → Private repositories → cloud-shop**

The repository contained the:

```text
v1
```

image tag.

### 📸 Screenshot

![ECR Image](02-ecr-image.png)

---

## Step 7 — Pull the Image from ECR

To verify that the image could be retrieved from ECR, I removed the local ECR tag and pulled the image again.

```bash
docker rmi \
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

Then:

```bash
docker pull \
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

This downloaded the image from Amazon ECR back into the local Docker environment.

### 📸 Screenshot

![Docker Pull](04-docker-pull.png)

---

## Step 8 — Run the ECR Image

After pulling the image, I ran it as a Docker container:

```bash
docker run -d \
--name cloud-shop-ecr \
-p 3000:3000 \
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

The application was then accessible at:

```text
http://localhost:3000
```

### 📸 Screenshot

![Cloud Shop Running](05-cloud-shop-running.png)

---

# 🔄 Complete Workflow

The complete workflow performed in this lab was:

```text
Cloud Shop Application
          │
          ▼
      Dockerfile
          │
          ▼
    Docker Image
    cloud-shop:latest
          │
          │ docker tag
          ▼
 ECR-compatible Image
          │
          │ docker push
          ▼
┌────────────────────────────┐
│       Amazon ECR           │
│                            │
│ Repository: cloud-shop     │
│ Image: v1                  │
└─────────────┬──────────────┘
              │
              │ docker pull
              ▼
        Local Docker
              │
              │ docker run
              ▼
       Cloud Shop App
```

---

# 🆚 Docker Hub vs Amazon ECR

Docker Hub and Amazon ECR both provide container image registry functionality.

| Feature                  | Docker Hub        | Amazon ECR             |
| ------------------------ | ----------------- | ---------------------- |
| Container image registry | ✅                 | ✅                      |
| Docker support           | ✅                 | ✅                      |
| Private repositories     | ✅                 | ✅                      |
| AWS IAM integration      | ❌                 | ✅                      |
| AWS service integration  | Limited           | ✅                      |
| ECS/EKS integration      | External registry | Native AWS integration |
| AWS-based CI/CD          | Possible          | Strong integration     |

For personal projects, Docker Hub can be convenient. ECR becomes particularly useful when containerized applications are being deployed within an AWS environment.

---

# 🔐 Security

ECR integrates with AWS Identity and Access Management (IAM), allowing access to repositories to be controlled through AWS permissions.

A typical organization could have:

```text
Developer
   │
   └── Push permission

CI/CD Pipeline
   │
   └── Push permission

EC2 / ECS / EKS
   │
   └── Pull permission
```

This allows different AWS resources and users to receive only the permissions they need.

---

# 💰 Cost Consideration

Amazon ECR is a paid AWS service based on factors such as container image storage and data transfer.

For learning projects, unused repositories and images should be cleaned up after completing the lab.

Docker Hub may be sufficient for many personal projects, while ECR is useful when learning or building AWS-based container workflows.

---

# 🧹 Cleanup

After completing the lab, the ECR repository can be deleted if it is no longer required.

The local container can also be removed:

```bash
docker stop cloud-shop-ecr
docker rm cloud-shop-ecr
```

The local ECR image can be removed with:

```bash
docker rmi \
830955873996.dkr.ecr.us-east-1.amazonaws.com/cloud-shop:v1
```

If the ECR repository is no longer needed, it can be deleted from:

**AWS Console → ECR → Private repositories → cloud-shop → Delete**

> ⚠️ Deleting the repository removes the images stored inside it.

---

# 📚 Key Takeaways

* ECR is AWS's managed container registry.
* An ECR repository stores container images.
* Docker images need to be tagged with the ECR repository URI before pushing.
* `docker push` uploads an image to ECR.
* `docker pull` downloads an image from ECR.
* ECR integrates with AWS IAM.
* ECR is useful for AWS-based container deployment and CI/CD workflows.
* ECR can work with services such as ECS, EKS, and EC2.

---

# 🚀 What I Practiced

```text
✅ Created a private ECR repository
✅ Authenticated Docker with ECR
✅ Tagged a Docker image
✅ Pushed an image to ECR
✅ Verified the image in ECR
✅ Pulled the image from ECR
✅ Ran the ECR image as a Docker container
```

---

## 🛠️ Technologies Used

* Amazon ECR
* AWS CLI
* Docker
* Amazon Web Services
* Node.js / Cloud Shop Application
* macOS Terminal
