# 🔐 Secret Management on AWS

## 📌 Overview

Applications often need sensitive information such as database passwords, API keys, access tokens, and other credentials.

The problem is that we should **not store these secrets directly inside our source code**.

For example, this is a bad practice:

```python
DB_PASSWORD = "MyPassword123"
```

If this code is pushed to GitHub, the password may become exposed.

AWS provides services that allow us to securely store and manage sensitive information outside our application code.

The main services we will discuss are:

* **AWS Secrets Manager**
* **AWS Systems Manager Parameter Store**

---

# 1. 🔐 What is Secret Management?

**Secret management** is the process of securely storing, controlling access to, retrieving, and rotating sensitive information used by applications.

Examples of secrets include:

```text
Database passwords
API keys
Access tokens
OAuth credentials
Private credentials
Application secrets
```

The basic idea is:

```text
Application
     │
     │ Request secret
     ▼
Secret Management Service
     │
     │ IAM authorization
     ▼
Secret
```

Instead of putting the secret inside the application code, we store it securely and allow authorized applications to retrieve it when required.

---

# 2. ❌ The Problem with Hard-Coded Secrets

Consider a Python application:

```python
DB_USERNAME = "admin"
DB_PASSWORD = "MyPassword123"
```

This creates several security problems.

### Problem 1 — GitHub Exposure

If we push the code:

```bash
git add .
git commit -m "Add application"
git push
```

the password may become part of the Git repository.

Even deleting the password later does not necessarily remove it from the repository's previous Git history.

---

### Problem 2 — Docker Images

If credentials are incorrectly included while building a Docker image, they can potentially become exposed through the image or its build history.

We want our Docker image to contain the application, not production credentials.

---

### Problem 3 — Multiple Environments

A real application may have:

```text
Development
Staging
Production
```

Each environment may have different credentials.

For example:

```text
Development → dev password
Staging     → staging password
Production  → production password
```

Hard-coding these credentials makes management difficult and risky.

---

# 3. ✅ The Better Approach

Instead of:

```text
Application
     │
     └── Password inside code ❌
```

we use:

```text
Application
     │
     │ IAM Role
     ▼
AWS Secrets Manager
     │
     ▼
Database Password
```

The application retrieves the secret only when it needs it.

This gives us a separation between:

```text
Application Code
        +
Sensitive Credentials
```

---

# 4. AWS Secrets Manager

**AWS Secrets Manager** is an AWS service designed to securely store and manage sensitive information.

For example, we can store:

```json
{
  "username": "admin",
  "password": "StrongPassword",
  "host": "database.example.com",
  "port": 5432,
  "database": "production"
}
```

The application does not need to store this information inside its source code.

Instead:

```text
                    AWS
┌──────────────────────────────────────┐
│                                      │
│        AWS Secrets Manager           │
│                                      │
│     production/database              │
│     ├── username                     │
│     ├── password                     │
│     ├── host                         │
│     └── database                     │
│                                      │
└──────────────────▲───────────────────┘
                   │
              IAM Permission
                   │
                   │
            ┌──────┴──────┐
            │ Application │
            │ EC2 / ECS   │
            │ EKS / Lambda│
            └─────────────┘
```

---

# 5. Real-World Example

Imagine we have an e-commerce application running on EC2.

The application needs to connect to PostgreSQL.

Without secret management:

```text
EC2 Application
      │
      └── DB Password inside code ❌
```

With AWS Secrets Manager:

```text
                   AWS
                    │
                    ▼
          AWS Secrets Manager
                    │
             DB Credentials
                    │
                    ▲
                    │
                IAM Role
                    │
                    ▼
                   EC2
                    │
                    ▼
              PostgreSQL
```

The EC2 application gets permission through an IAM role and retrieves the secret from Secrets Manager.

---

# 6. 🔑 IAM Role and Secrets Manager

One of the most important concepts is that storing a secret is not enough.

**We** also need to control **who can access it**.

For example:

```text
EC2 Application
      │
      ▼
IAM Role
      │
      ▼
secretsmanager:GetSecretValue
      │
      ▼
Specific Secret
```

The IAM policy should follow the **principle of least privilege**.

For example, an application may only need:

```text
secretsmanager:GetSecretValue
```

for one specific secret.

We should avoid giving the application unnecessary permissions.

---

# 7. IAM Role vs AWS Access Keys

A common mistake is putting AWS credentials directly into the application.

For example:

```python
AWS_ACCESS_KEY_ID = "AKIA..."
AWS_SECRET_ACCESS_KEY = "..."
```

This is not recommended.

Instead, when an application runs on AWS services such as EC2, ECS, or Lambda, we can use an **IAM role**.

Conceptually:

```text
Application
     │
     ▼
IAM Role
     │
     ▼
AWS Temporary Credentials
     │
     ▼
AWS Services
```

The application does not need to store long-term AWS access keys in its source code.

---

# 8. How the Complete Flow Works

Suppose we have:

```text
EC2
 │
 └── Application
```

The complete process is:

### Step 1

Create a secret in Secrets Manager.

```text
production/database
```

### Step 2

Create an IAM role for the EC2 instance.

### Step 3

Allow the role to retrieve the required secret.

### Step 4

The application starts.

### Step 5

The application requests the secret.

```text
GetSecretValue
```

### Step 6

AWS checks the IAM permissions.

### Step 7

If authorized, Secrets Manager returns the secret.

```text
EC2 Application
      │
      ▼
IAM Authorization
      │
      ▼
Secrets Manager
      │
      ▼
Database Credentials
```

---

# 9. Accessing Secrets Using Python

Applications can use the AWS SDK to retrieve secrets.

For Python, the AWS SDK is:

```text
boto3
```

Example:

```python
import boto3

client = boto3.client("secretsmanager")

response = client.get_secret_value(
    SecretId="production/database"
)

secret = response["SecretString"]

print(secret)
```

In a real application, we would normally parse the JSON and use the required values rather than printing the secret.

For example:

```python
import json

credentials = json.loads(secret)

username = credentials["username"]
password = credentials["password"]
```

> **Important:** Never print real secrets in application logs.

---

# 10. 🔒 Encryption

Secrets stored in AWS Secrets Manager are encrypted.

AWS Key Management Service (**AWS KMS**) can be used for encryption key management.

Conceptually:

```text
Secret
   │
   ▼
Encryption
   │
   ▼
AWS KMS
   │
   ▼
Encrypted Secret
```

When an authorized application retrieves the secret, AWS handles the required decryption according to the service configuration and permissions.

---

# 11. 🔄 Secret Rotation

Secrets should not necessarily remain unchanged forever.

For example:

```text
Old Password
     │
     ▼
Rotation
     │
     ▼
New Password
```

Secret rotation means periodically replacing an existing credential with a new one.

Example:

```text
Day 1
Password A

      ↓

Rotation

      ↓

Day 30
Password B

      ↓

Rotation

      ↓

Day 60
Password C
```

Secrets Manager supports secret rotation capabilities, including automated rotation patterns for supported use cases.

This reduces the risk associated with long-lived credentials.

---

# 12. AWS Systems Manager Parameter Store

Another AWS service used for configuration and parameter management is:

**AWS Systems Manager Parameter Store**

It can store application configuration such as:

```text
APP_ENV = production
LOG_LEVEL = info
API_URL = https://api.example.com
```

It also supports encrypted parameters using:

```text
SecureString
```

For example:

```text
/myapp/production/APP_ENV
/myapp/production/LOG_LEVEL
/myapp/production/API_URL
```

Parameter Store is particularly useful for centralized application configuration.

---

# 13. Secrets Manager vs Parameter Store

This is one of the most common AWS interview questions.

| Feature                   | Secrets Manager      | Parameter Store                 |
| ------------------------- | -------------------- | ------------------------------- |
| Store secrets             | ✅                    | ✅                               |
| Store configuration       | ✅                    | ✅                               |
| SecureString              | Not the main concept | ✅                               |
| Automatic rotation        | ✅                    | More limited/manual patterns    |
| Database credentials      | Excellent fit        | Possible                        |
| API keys                  | Excellent fit        | Possible                        |
| Application configuration | Possible             | Excellent fit                   |
| AWS Systems Manager       | Separate service     | Native                          |
| Cost                      | Paid service         | Standard parameters can be free |

### Easy way to remember

Think:

```text
Sensitive credentials
        ↓
Secrets Manager
```

and:

```text
Application configuration
        ↓
Parameter Store
```

This is a useful rule of thumb, although the final choice should depend on the application's requirements.

---

# 14. Real DevOps Scenario — ECS

Suppose we have a Docker application running on Amazon ECS.

The application requires:

```text
DB_USERNAME
DB_PASSWORD
STRIPE_API_KEY
JWT_SECRET
```

We don't want these values inside the Docker image.

Instead:

```text
                    AWS
                     │
                     ▼
             Secrets Manager
             ┌───────────────┐
             │ DB Password   │
             │ Stripe Key    │
             │ JWT Secret    │
             └───────┬───────┘
                     │
                 IAM Role
                     │
                     ▼
                ECS Task
                     │
                     ▼
               Application
```

The Docker image can remain generic.

For example:

```text
my-app:v1
```

The same image can be used in:

```text
Development
Staging
Production
```

while each environment retrieves its own secrets.

---

# 15. Same Docker Image, Different Secrets

This is an important DevOps concept.

We can build one image:

```text
my-app:v1
```

Then deploy it to:

```text
Development
       ↓
my-app:v1

Staging
       ↓
my-app:v1

Production
       ↓
my-app:v1
```

But each environment can use different secrets:

```text
Development
    ↓
dev/database

Staging
    ↓
staging/database

Production
    ↓
production/database
```

This means we don't need to rebuild the application simply because the database password is different.

---

# 16. Secret Management with EKS

The same concept applies to Kubernetes.

A production EKS environment may look like:

```text
                 EKS Cluster
                     │
                     ▼
                 Kubernetes
                    Pod
                     │
                     ▼
       AWS Secrets Manager
                     │
                     ▼
              Database Secret
```

AWS provides integrations such as the **AWS Secrets and Configuration Provider for the Kubernetes Secrets Store CSI Driver** to make AWS-managed secrets available to Kubernetes workloads.

The important concept is:

```text
Kubernetes workload
        ↓
AWS authorization
        ↓
Secrets Manager
        ↓
Secret
```

This is useful when building secure production workloads on EKS.

---

# 17. ❌ Things We Should NOT Do

### Don't hard-code passwords

```python
DB_PASSWORD = "MyPassword123"
```

### Don't commit `.env` containing real secrets

```text
.env
```

If it contains real credentials, it should not be committed to GitHub.

### Don't put secrets in Dockerfiles

Avoid:

```dockerfile
ENV DB_PASSWORD="MyPassword123"
```

### Don't put secrets directly into Kubernetes YAML committed to Git

For example:

```yaml
password: MyPassword123
```

### Don't give unnecessary IAM permissions

Avoid broad permissions when the application only needs one specific secret.

---

# 18. Principle of Least Privilege

The principle of least privilege means:

> Give an application only the permissions it actually needs.

For example:

```text
Application A
      │
      └── Secret A ✅

Application B
      │
      └── Secret B ✅
```

Instead of:

```text
Application A
      │
      └── All Secrets ❌
```

If Application A is compromised, limiting its permissions reduces the potential damage.

---

# 19. Secret Lifecycle

A good secret-management process looks like:

```text
Create
  ↓
Store securely
  ↓
Encrypt
  ↓
Control access
  ↓
Retrieve when required
  ↓
Monitor
  ↓
Rotate
  ↓
Revoke/Delete when no longer needed
```

This is the **secret lifecycle**.

---

# 20. Real Production Architecture

A realistic application might look like:

```text
                         Internet
                            │
                            ▼
                           ALB
                            │
                            ▼
                      ECS / EKS
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      AWS Secrets Manager        Parameter Store
              │                           │
              │                           │
       DB Password                    APP_ENV
       API Key                        LOG_LEVEL
       OAuth Secret                   API_URL
              │
              ▼
             RDS
```

This separates:

```text
Application Code
        +
Configuration
        +
Sensitive Secrets
```

instead of putting everything inside the application.

---

# 21. 🔥 Most Asked Interview Questions

## Q1. What is secret management?

**Answer:**

> Secret management is the secure storage, access control, retrieval, monitoring, and rotation of sensitive information such as passwords, API keys, and credentials.

---

## Q2. What is AWS Secrets Manager?

**Answer:**

> AWS Secrets Manager is a managed AWS service used to securely store, retrieve, and manage sensitive credentials and secrets. It also provides features such as encryption and secret rotation.

---

## Q3. Why shouldn't secrets be stored in source code?

**Answer:**

> Source code can be committed to Git repositories, shared with developers, included in build artifacts, or exposed through logs. Keeping secrets outside the source code reduces the risk of accidental exposure.

---

## Q4. How does an EC2 application access Secrets Manager?

**Answer:**

```text
EC2
 ↓
IAM Role
 ↓
GetSecretValue permission
 ↓
Secrets Manager
 ↓
Secret
```

The application uses the EC2 instance's IAM role instead of storing AWS access keys in the source code.

---

## Q5. What is secret rotation?

**Answer:**

> Secret rotation is the process of periodically replacing an existing credential with a new credential to reduce the risk of long-lived secrets.

---

## Q6. Secrets Manager vs Parameter Store?

**Answer:**

> Secrets Manager is specifically designed for managing sensitive secrets and provides features such as secret rotation. Parameter Store is primarily used for centralized application configuration and parameters, although it can also store encrypted SecureString values.

---

## Q7. Why use IAM roles with Secrets Manager?

**Answer:**

> IAM roles allow applications to access only the secrets they are authorized to access without embedding long-term AWS access keys in the application.

---

## Q8. What is the principle of least privilege?

**Answer:**

> It means giving an application or user only the permissions required to perform its job and nothing more.

---

# 22. 🧠 Simple Mental Model

Remember this:

```text
❌ Bad Architecture

Application
    │
    └── Password inside code


✅ Good Architecture

Application
    │
    │ IAM Role
    ▼
Secrets Manager
    │
    ▼
Secret
```

The key idea is:

> **Code should know how to retrieve a secret, not contain the secret itself.**

---

# 23. 🛠️ Hands-On Lab

For this topic, a practical lab can be built using:

```text
EC2
 +
IAM Role
 +
AWS Secrets Manager
 +
Python / Boto3
```

### Lab Architecture

```text
                 AWS
                  │
                  ▼
          Secrets Manager
                  │
          demo/database
                  │
                  ▲
                  │
              IAM Role
                  │
                  ▼
                 EC2
                  │
                  ▼
              Python App
```

### Lab Steps

1. Create a secret in AWS Secrets Manager.
2. Store sample database credentials.
3. Create an IAM policy with least-privilege access.
4. Create an IAM role.
5. Attach the role to an EC2 instance.
6. Install/use Python and Boto3.
7. Retrieve the secret from EC2.
8. Verify successful access.
9. Test access without the required IAM permission.
10. Remove the resources after testing.

### Expected Learning

After completing the lab, you should understand:

```text
Secret creation
      ↓
Secret storage
      ↓
IAM authorization
      ↓
Application request
      ↓
Secret retrieval
```

---

# 24. 🧹 Security Checklist

Before deploying an application, check:

* [ ] No passwords hard-coded in source code
* [ ] No API keys committed to GitHub
* [ ] `.env` with real secrets is ignored
* [ ] Secrets stored in an appropriate secret-management service
* [ ] IAM follows least privilege
* [ ] Applications use IAM roles where possible
* [ ] Secrets are encrypted
* [ ] Secret access is monitored
* [ ] Secrets are rotated when appropriate
* [ ] Secrets are removed/revoked when no longer required

---

# 25. 🎯 Key Takeaways

### Secret Management

Securely storing and controlling access to sensitive information.

### AWS Secrets Manager

Best suited for managing sensitive credentials and secrets.

### Parameter Store

Useful for centralized application configuration and parameters, including encrypted SecureString values.

### IAM

Controls **who or what can access a secret**.

### IAM Role

Allows AWS workloads to obtain permissions without embedding long-term AWS credentials in application code.

### Secret Rotation

Periodically changes credentials to reduce the risk of long-lived secrets.

### Least Privilege

Give applications only the permissions they actually need.

---

# ⭐ Final Concept

The whole topic can be remembered with one sentence:

> **Store sensitive information outside your application code, protect it with encryption and IAM permissions, and allow only authorized applications to retrieve it when needed.**

```text
                 SECRET MANAGEMENT
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
     Secure          IAM Access       Rotation
     Storage          Control
        │               │                │
        └───────────────┼────────────────┘
                        │
                        ▼
                Secure Application
```

---

## 📚 Day 15 Summary

**Topic:** Secret Management on AWS

**Main Services:**

* AWS Secrets Manager
* AWS Systems Manager Parameter Store
* AWS IAM
* AWS KMS

**Main Concepts:**

* Secrets
* IAM roles
* Least privilege
* Encryption
* Secret retrieval
* Secret rotation
* Secure application configuration

**Real-world use cases:**

* EC2 + Secrets Manager
* ECS + Secrets Manager
* EKS + Secrets Manager
* Lambda + Secrets Manager
* RDS credentials
* API keys
* Application configuration

**Most important interview question:**

> **Why shouldn't we store secrets in application code?**

Because source code can be exposed through Git repositories, build artifacts, logs, or other development workflows. Secret-management services provide a controlled and secure way for authorized applications to retrieve sensitive information.

