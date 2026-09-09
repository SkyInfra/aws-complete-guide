# Day 3 — AWS IAM 🔐

> **AWS Complete Guide — Day 3 of 30**

## 1. What is AWS IAM?

**IAM (Identity and Access Management)** is an AWS service that controls **who can access AWS resources and what they are allowed to do**.

Think of IAM as the **security system of your AWS environment**.

For example:

Imagine a company has:

* 10 developers
* 2 DevOps engineers
* 1 database administrator

They should not all have the same access.

A developer may need access to EC2 but should not be able to delete the production database.

IAM allows us to create these access rules.

```text
User → Authentication → IAM → Permissions → AWS Resource
```

For example:

```text
Developer
   ↓
IAM
   ↓
Can access EC2
Cannot delete RDS
```

---

# 2. Why Do We Need IAM?

Without access control, anyone with access to an AWS account could potentially perform dangerous operations.

IAM allows us to:

* Create identities
* Control access
* Grant permissions
* Remove permissions
* Create temporary access
* Enable MFA
* Follow least privilege
* Control access to AWS resources

The main goal is:

> **Only the right person or service should have the right permissions to the right resources.**

---

# 3. Main Components of IAM

The four important IAM components are:

```text
IAM
│
├── Users
├── Groups
├── Roles
└── Policies
```

Let's understand each one.

---

# 4. IAM Users

An **IAM user** represents a person or workload that needs AWS access.

For example:

```text
Company
│
├── Ali
├── Ahmed
└── Haseeb
```

Each IAM user can have credentials and permissions.

Depending on the access method, credentials can include:

* Password
* Access key ID
* Secret access key
* MFA

### Example

Suppose Haseeb is a developer.

He needs to:

* View EC2 instances
* Start EC2 instances
* Stop EC2 instances

But he should not:

* Delete the production database
* Modify IAM permissions

We can create an IAM user and give that user only the required permissions.

---

# 5. IAM Groups

A **group** is a collection of IAM users.

Instead of assigning the same permissions to every user individually, we can put users into a group and assign permissions to the group.

Example:

```text
Developers Group
│
├── Haseeb
├── Ali
└── Ahmed
```

We can attach an EC2-related policy to the `Developers` group.

Then all users in that group receive those permissions.

### Why use groups?

Groups make permission management easier.

Instead of:

```text
Haseeb → permissions
Ali    → permissions
Ahmed  → permissions
```

We can do:

```text
Developers Group
       ↓
   Permissions
       ↓
Haseeb + Ali + Ahmed
```

---

# 6. IAM Roles

An **IAM role** is an identity that provides **temporary permissions**.

Roles are commonly used by:

* AWS services
* Applications
* EC2 instances
* Lambda functions
* Users needing temporary access
* External identities

For example:

Suppose an EC2 server needs to read files from an S3 bucket.

Instead of putting AWS access keys directly inside the EC2 server, we can give the EC2 instance an IAM role.

```text
EC2
 ↓
IAM Role
 ↓
Permission
 ↓
S3
```

The EC2 instance can then access the allowed S3 resources using temporary credentials.

### Important

Avoid storing long-term AWS access keys inside:

```text
Application code
GitHub repositories
Docker images
EC2 configuration files
```

For AWS workloads, **IAM roles are generally preferred**.

---

# 7. IAM Policies

A **policy** defines what an identity is allowed or denied to do.

IAM policies are written in **JSON**.

For example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

This policy means:

```text
Effect  → Allow
Action  → Read/Get an S3 object
Resource → Objects inside my-bucket
```

So the identity can read objects from that S3 bucket.

---

# 8. Allow and Deny

IAM policies can contain:

```text
Allow
Deny
```

### Allow

Allows an action.

Example:

```text
Allow → Start EC2 instance
```

### Deny

Explicitly prevents an action.

Example:

```text
Deny → Delete S3 bucket
```

An explicit **Deny** takes precedence over an Allow.

---

# 9. Principle of Least Privilege

One of the most important IAM security concepts is:

> **Give only the permissions that are required to perform a task.**

Suppose a developer only needs to read an S3 bucket.

Do not give:

```text
AdministratorAccess
```

Instead, give only:

```text
s3:GetObject
```

For example:

```text
❌ Developer
   → AdministratorAccess

✅ Developer
   → Read required S3 objects
```

This reduces the damage that can occur if credentials are compromised or an account is misused.

---

# 10. IAM Authentication vs Authorization

These two concepts are important.

### Authentication

Authentication answers:

> **Who are you?**

Examples:

```text
Username + Password
Access Keys
MFA
```

### Authorization

Authorization answers:

> **What are you allowed to do?**

Example:

```text
User
 ↓
Authenticated
 ↓
IAM Policy
 ↓
Allowed to read S3
```

Simple way to remember:

```text
Authentication = Who are you?
Authorization  = What can you do?
```

---

# 11. MFA

**MFA = Multi-Factor Authentication**

MFA adds another layer of security.

Instead of only:

```text
Password
```

you can require:

```text
Password
+
MFA code
```

This helps protect accounts if a password is compromised.

For important AWS identities, MFA is an important security control.

---

# 12. IAM Managed Policies

AWS provides predefined policies called **AWS managed policies**.

Example:

```text
AmazonS3ReadOnlyAccess
```

These policies are maintained by AWS.

There are also **customer managed policies**, which you create and maintain yourself.

```text
Policies
│
├── AWS Managed Policies
│
└── Customer Managed Policies
```

---

# 13. User vs Group vs Role vs Policy

| Component | Purpose                        |
| --------- | ------------------------------ |
| User      | Represents an identity         |
| Group     | Collection of users            |
| Role      | Provides temporary permissions |
| Policy    | Defines permissions            |

Think of it like this:

```text
User
 ↓
Member of Group
 ↓
Group has Policy
 ↓
Permissions are granted
```

And for an AWS service:

```text
EC2
 ↓
IAM Role
 ↓
IAM Policy
 ↓
S3
```

---

# 14. Real-World Example

Imagine a company has:

```text
Company
│
├── Developers
├── DevOps Team
└── Database Team
```

### Developers

Need:

```text
EC2 → Start/Stop
S3  → Read
```

### DevOps Team

Need:

```text
EC2 → Full management
ECS → Management
CloudWatch → Management
```

### Database Team

Need:

```text
RDS → Management
```

Instead of giving everyone administrator access:

```text
Everyone
   ↓
AdministratorAccess
```

we create specific permissions:

```text
Developers Group
      ↓
Limited Policies

DevOps Group
      ↓
DevOps Policies

Database Group
      ↓
RDS Policies
```

This follows the **principle of least privilege**.

---

# 15. IAM and AWS Root User

When an AWS account is created, there is a **root user**.

The root user has extremely powerful permissions.

The root user should **not be used for normal daily work**.

A better approach is:

```text
AWS Account
    ↓
Root User
    ↓
Secure it with MFA
    ↓
Create appropriate IAM access
    ↓
Use least privilege
```

The root user should generally be reserved for tasks that specifically require root-user credentials.

---

# 16. IAM and DevOps

IAM is extremely important for a Cloud/DevOps engineer.

You will frequently work with:

```text
EC2
S3
ECR
ECS
Lambda
CloudWatch
RDS
AWS CLI
CI/CD
```

All of these involve access control.

For example:

```text
GitHub Actions
      ↓
AWS Authentication
      ↓
IAM Role
      ↓
ECR
      ↓
Push Docker Image
```

Or:

```text
EC2
 ↓
IAM Role
 ↓
S3
 ↓
Download Application Files
```

Understanding IAM is therefore essential before working deeply with AWS.

---

# 17. IAM Mental Model

Remember this simple model:

```text
WHO?
 ↓
User / Role
 ↓
WHAT CAN THEY DO?
 ↓
Policy
 ↓
WHERE?
 ↓
AWS Resource
```

Example:

```text
EC2 Role
   ↓
Policy
   ↓
s3:GetObject
   ↓
my-bucket/*
```

Meaning:

> This EC2 role can read objects from this S3 bucket.

---

# 18. Important IAM Terms

| Term            | Meaning                                      |
| --------------- | -------------------------------------------- |
| IAM             | Identity and Access Management               |
| User            | Identity representing a person/workload      |
| Group           | Collection of users                          |
| Role            | Identity that provides temporary permissions |
| Policy          | JSON document defining permissions           |
| Permission      | What an identity is allowed to do            |
| Authentication  | Verifying identity                           |
| Authorization   | Determining allowed actions                  |
| MFA             | Multi-Factor Authentication                  |
| Least Privilege | Give only required permissions               |
| Root User       | Original AWS account identity                |

---

# 19. Day 3 Key Takeaways

The most important things to remember are:

1. **IAM controls access to AWS resources.**
2. **Users represent identities.**
3. **Groups organize users with common permissions.**
4. **Roles provide temporary access and are heavily used by AWS services/workloads.**
5. **Policies define permissions.**
6. **Policies are written in JSON.**
7. **Use least privilege.**
8. **Enable MFA for important identities.**
9. **Avoid putting AWS access keys inside code or GitHub.**
10. **Do not use the root user for everyday AWS work.**

---

# 20. Quick Revision

### Q1. What is IAM?

IAM is AWS's service for managing identities and controlling access to AWS resources.

### Q2. What are the four main IAM components?

```text
Users
Groups
Roles
Policies
```

### Q3. What is a policy?

A JSON document that defines permissions.

### Q4. What is a role?

An identity that provides temporary permissions and is commonly assumed by AWS services, applications, users, or external identities.

### Q5. What is least privilege?

Giving an identity only the permissions it actually needs.

### Q6. Authentication vs Authorization?

```text
Authentication → Who are you?
Authorization  → What can you do?
```

### Q7. Why is MFA important?

It adds an additional authentication factor and improves account security.

---

# Day 3 Summary

```text
                    AWS IAM
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
     Users          Groups           Roles
       │               │               │
       └───────────────┼───────────────┘
                       ↓
                    Policies
                       ↓
                  Permissions
                       ↓
                AWS Resources
```

IAM is the foundation of **AWS access control and security**.

Before deploying applications in AWS, you need to understand **who can access your resources and what they are allowed to do**.

## ✅ Day 3 Completed

**Topic:** AWS Identity and Access Management (IAM)

**Progress:** 3 / 30

**Next:** Day 4 — EC2 Fundamentals
