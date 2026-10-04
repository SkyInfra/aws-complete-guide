# Amazon S3 — Complete Guide

> A practical, beginner-friendly guide to Amazon Simple Storage Service (S3), covering storage, security, encryption, versioning, lifecycle management, access control, replication, events, CLI usage, troubleshooting, and real-world DevOps use cases.

## Table of Contents

1. [What is Amazon S3?](#1-what-is-amazon-s3)
2. [Object Storage](#2-object-storage)
3. [Buckets](#3-buckets)
4. [Objects and Object Keys](#4-objects-and-object-keys)
5. [Regions](#5-regions)
6. [Storage Classes](#6-storage-classes)
7. [Versioning](#7-versioning)
8. [Delete Markers](#8-delete-markers)
9. [Lifecycle Rules](#9-lifecycle-rules)
10. [Encryption](#10-encryption)
11. [SSE-S3 vs SSE-KMS](#11-sse-s3-vs-sse-kms)
12. [S3 Security](#12-s3-security)
13. [IAM Policies vs Bucket Policies](#13-iam-policies-vs-bucket-policies)
14. [Block Public Access](#14-block-public-access)
15. [ACLs and Object Ownership](#15-acls-and-object-ownership)
16. [Presigned URLs](#16-presigned-urls)
17. [Static Website Hosting](#17-static-website-hosting)
18. [Access Points](#18-access-points)
19. [Replication](#19-replication)
20. [Object Lock](#20-object-lock)
21. [Multipart Upload](#21-multipart-upload)
22. [Event Notifications](#22-event-notifications)
23. [Transfer Acceleration](#23-transfer-acceleration)
24. [Monitoring and Auditing](#24-monitoring-and-auditing)
25. [Cost Optimization](#25-cost-optimization)
26. [S3 Consistency](#26-s3-consistency)
27. [AWS CLI](#27-aws-cli)
28. [Common Troubleshooting](#28-common-troubleshooting)
29. [Real-World Architecture](#29-real-world-architecture)
30. [Best Practices](#30-best-practices)
31. [Quick Revision](#31-quick-revision)

---

# 1. What is Amazon S3?

**Amazon S3 (Simple Storage Service)** is AWS's object storage service.

It is designed to store and retrieve virtually any amount of data.

Common use cases:

- Images and videos
- Documents and PDFs
- Application assets
- Backups
- Logs
- Static website files
- Data lakes
- Archives
- Software packages

### Mental Model

```text
Application
     |
     v
    S3
     |
     +-- Images
     +-- Documents
     +-- Videos
     +-- Backups
     +-- Logs
```

S3 is **object storage**, not traditional block storage such as EBS.

---

# 2. Object Storage

S3 stores data as **objects**.

Conceptually:

```text
Object
├── Data
├── Key
├── Metadata
└── Version ID
```

A simple example:

```text
Data:
Product image

Key:
products/images/laptop.jpg
```

The key identifies the object inside a bucket.

---

# 3. Buckets

A **bucket** is a top-level container for S3 objects.

Example:

```text
cloudshop-assets/
├── products/
│   ├── laptop.jpg
│   └── keyboard.jpg
├── documents/
│   └── manual.pdf
└── backups/
    └── backup.zip
```

## Bucket Naming

Bucket names must be unique within the applicable S3 namespace.

Example:

```text
cloudshop-assets-2026-12345
```

Avoid putting passwords, API keys, or other sensitive information in bucket names.

---

# 4. Objects and Object Keys

An object key is the complete name used to identify an object.

Example:

```text
products/images/laptop.jpg
```

## Important: S3 Does Not Use Traditional Folders

The S3 console displays folders, but S3 fundamentally stores objects using keys.

For example:

```text
products/laptop.jpg
products/keyboard.jpg
documents/manual.pdf
```

The `/` is part of the key.

You can think of:

```text
products/laptop.jpg
```

as:

```text
Prefix: products/
Object name: laptop.jpg
```

---

# 5. Regions

An S3 bucket is associated with an AWS Region.

Examples:

```text
us-east-1
eu-west-1
ap-southeast-1
```

Region selection can affect:

- Latency
- Data residency
- Compliance
- Integration with other AWS services
- Data transfer considerations
- Availability of specific features

A common architecture is:

```text
EC2
 |
 +---- S3
      |
      +---- Same AWS Region
```

---

# 6. Storage Classes

S3 provides multiple storage classes for different access patterns.

| Storage Class | Typical Use |
|---|---|
| S3 Standard | Frequently accessed data |
| S3 Intelligent-Tiering | Unknown or changing access patterns |
| S3 Standard-IA | Infrequently accessed data |
| S3 One Zone-IA | Infrequently accessed, recreatable data |
| S3 Glacier Instant Retrieval | Archive data needing rapid retrieval |
| S3 Glacier Flexible Retrieval | Archive data with flexible retrieval time |
| S3 Glacier Deep Archive | Long-term, rarely accessed archive |

### Simple Model

```text
Frequently accessed
        |
        v
 S3 Standard
        |
        v
Infrequently accessed
        |
        v
      IA
        |
        v
    Archive
        |
        v
 Glacier classes
        |
        v
 Deep Archive
```

### Choosing a Storage Class

Consider:

- Access frequency
- Retrieval cost
- Retrieval time
- Minimum storage duration
- Object size
- Recovery requirements

The cheapest storage class is not always the cheapest overall option.

---

# 7. Versioning

S3 Versioning keeps multiple versions of an object.

Example:

```text
config.json

Version 1
Version 2
Version 3  <-- Current
```

If an object is overwritten, the previous version can remain available.

## Why Use Versioning?

Versioning helps protect against:

- Accidental overwrites
- Accidental deletion
- Application mistakes
- Data corruption
- Unwanted changes

### Example

```text
Upload:
file.txt -> Version 1

Modify:
file.txt -> Version 2

Modify again:
file.txt -> Version 3
```

---

# 8. Delete Markers

When versioning is enabled, a normal delete operation can create a **delete marker** instead of permanently deleting all versions.

Example:

```text
file.txt

Version 1
Version 2
Delete Marker  <-- Current
```

The object appears deleted through normal access, while previous versions can still exist.

### Important

Removing the delete marker can make the previous version visible again.

To permanently remove a specific version, delete that version using its version ID.

---

# 9. Lifecycle Rules

Lifecycle rules automatically manage objects as they age.

They can:

- Transition objects to cheaper storage
- Expire objects
- Delete noncurrent versions
- Abort incomplete multipart uploads

## Example

```text
Day 0
  |
  v
S3 Standard
  |
  | 30 days
  v
S3 Glacier
  |
  | 365 days
  v
Expiration
```

## Common Lifecycle Actions

### Transition

Move objects to another storage class.

### Expiration

Automatically delete objects after a defined period.

### Noncurrent Version Expiration

Delete old object versions after a defined period.

### Abort Incomplete Multipart Uploads

Clean up multipart uploads that were started but never completed.

---

# 10. Encryption

S3 supports encryption at rest.

Important server-side encryption options:

- **SSE-S3**
- **SSE-KMS**
- **SSE-C**

S3 automatically encrypts new objects at rest by default.

### Server-Side Encryption

```text
Client
  |
  | Upload
  v
 S3
  |
  | Encrypt
  v
Encrypted Object
```

---

# 11. SSE-S3 vs SSE-KMS

## SSE-S3

With SSE-S3:

```text
S3
 |
 +-- Manages encryption keys
 +-- Encrypts objects
 +-- Simple configuration
```

S3 manages the encryption keys.

Use it when you need straightforward server-side encryption without additional KMS key-management requirements.

## SSE-KMS

With SSE-KMS:

```text
S3
 |
 v
AWS KMS
 |
 v
KMS Key
```

KMS provides additional control over:

- Key permissions
- Key policies
- Auditing
- Key lifecycle
- Access control

## Comparison

| Feature | SSE-S3 | SSE-KMS |
|---|---|---|
| Encryption at rest | Yes | Yes |
| Key management | S3 | AWS KMS |
| Detailed key permissions | Limited | Yes |
| KMS audit integration | No | Yes |
| Operational complexity | Lower | Higher |
| KMS request considerations | No | Yes |

> **Important:** SSE-KMS is not simply "more encrypted." Both provide encryption at rest. The main difference is key management, access control, and auditing.

### S3 Bucket Keys

With SSE-KMS, **S3 Bucket Keys** can reduce the number of requests made to AWS KMS and can help reduce KMS-related costs.

---

# 12. S3 Security

S3 security commonly involves several layers:

```text
             S3 Security
                  |
       +----------+----------+
       |          |          |
      IAM       Bucket     Block
     Policies   Policies   Public Access
       |          |          |
       +----------+----------+
                  |
            Object Ownership
```

Important security controls include:

- IAM policies
- Bucket policies
- Block Public Access
- Object Ownership
- Encryption
- KMS
- Access Points
- CloudTrail auditing
- Least privilege

---

# 13. IAM Policies vs Bucket Policies

This distinction is extremely important.

## IAM Identity-Based Policy

An IAM policy is attached to an identity such as:

- IAM user
- IAM group
- IAM role

Example:

```text
IAM Role
   |
   +-- Allow s3:GetObject
   |
   v
S3 Object
```

## Bucket Policy

A bucket policy is attached directly to an S3 bucket.

Example:

```text
S3 Bucket
   |
   +-- Bucket Policy
          |
          +-- Allow / Deny access
```

Bucket policies are resource-based policies.

## Resource ARN vs Object ARN

Bucket ARN:

```text
arn:aws:s3:::my-bucket
```

Object ARN:

```text
arn:aws:s3:::my-bucket/*
```

These are different resources.

### Example

`ListBucket` applies to the bucket:

```text
arn:aws:s3:::my-bucket
```

`GetObject` applies to objects:

```text
arn:aws:s3:::my-bucket/*
```

This distinction is a common source of `AccessDenied` errors.

---

# 14. Block Public Access

S3 provides **Block Public Access** controls to help prevent unintended public access.

The four related settings are:

- Block public ACLs
- Ignore public ACLs
- Block public bucket policies
- Restrict public bucket policies

For most private application buckets:

```text
Block Public Access
        |
        v
      ENABLED
```

Do not make a bucket public just because an application needs to let users download a file.

For temporary access, consider **presigned URLs**.

---

# 15. ACLs and Object Ownership

ACLs are an older S3 access-control mechanism.

Modern S3 configurations commonly use:

```text
Bucket owner enforced
```

With Bucket owner enforced Object Ownership, ACLs are disabled for the bucket.

Access is normally managed through:

- IAM policies
- Bucket policies
- Access Points

### General Rule

For new applications:

```text
Prefer IAM + Bucket Policies
        |
        v
Avoid unnecessary ACL complexity
```

ACLs can still matter for older applications and legacy workflows.

---

# 16. Presigned URLs

A **presigned URL** provides temporary access to a private S3 object.

Example:

```text
User
 |
 | Request file
 v
Application
 |
 | Generate presigned URL
 v
S3
 |
 | Temporary access
 v
User
```

Common use cases:

- Private downloads
- User profile images
- File uploads
- Temporary document sharing
- Large file transfers

A presigned URL has an expiration time.

> A presigned URL does not make the bucket public. It provides temporary signed access to a specific operation.

---

# 17. Static Website Hosting

S3 can host static website files such as:

- HTML
- CSS
- JavaScript
- Images

Example:

```text
S3 Bucket
├── index.html
├── style.css
└── app.js
```

For production architectures, a common pattern is:

```text
User
 |
 v
CloudFront
 |
 v
S3
```

CloudFront can provide:

- CDN caching
- HTTPS
- Global edge delivery
- Better access control

For private S3 origins, CloudFront can use **Origin Access Control (OAC)** instead of making the bucket publicly accessible.

---

# 18. Access Points

S3 Access Points provide dedicated access endpoints for a bucket.

They are useful when different applications or teams need different access rules.

Example:

```text
                 S3 Bucket
                    |
          +---------+---------+
          |                   |
     App Access Point    Analytics Access Point
          |                   |
       App Team           Analytics Team
```

Each access point can have its own policy.

---

# 19. Replication

S3 Replication automatically copies objects between buckets.

## Same-Region Replication (SRR)

```text
Bucket A
   |
   | Replication
   v
Bucket B
Same Region
```

## Cross-Region Replication (CRR)

```text
Region A
Bucket A
   |
   | Replication
   v
Region B
Bucket B
```

Replication can be useful for:

- Disaster recovery
- Compliance requirements
- Geographic separation
- Lower-latency access in another region
- Data duplication

### Common prerequisites

- Versioning enabled on relevant buckets
- Replication configuration
- IAM role for S3
- Appropriate permissions

---

# 20. Object Lock

S3 Object Lock helps protect objects from deletion or modification for a defined retention period.

It supports a **WORM** model:

> Write Once, Read Many

Useful for:

- Compliance
- Financial records
- Audit data
- Backup protection
- Retention requirements

Object Lock supports:

- Retention periods
- Governance mode
- Compliance mode
- Legal holds

### Simple Model

```text
Object
  |
  v
Object Lock
  |
  +-- Protected during retention
```

---

# 21. Multipart Upload

Multipart upload breaks a large object into smaller parts.

```text
Large File
   |
   +-- Part 1
   +-- Part 2
   +-- Part 3
   +-- Part 4
   |
   v
S3
```

Advantages:

- Better handling of large files
- Parallel uploads
- Failed parts can be retried
- Improved upload performance

Incomplete multipart uploads can consume storage.

Lifecycle rules can automatically abort incomplete uploads.

---

# 22. Event Notifications

S3 can generate events when objects change.

```text
Object Uploaded
      |
      v
     S3
      |
      +----> Lambda
      |
      +----> SQS
      |
      +----> SNS
      |
      +----> EventBridge
```

Common event types include:

- Object created
- Object removed
- Object restored
- Replication events

### Example

```text
User uploads image
       |
       v
      S3
       |
       | Event
       v
    Lambda
       |
       v
Resize / Process Image
```

Event filters can target prefixes and suffixes.

Example:

```text
images/
```

or:

```text
.jpg
```

---

# 23. Transfer Acceleration

S3 Transfer Acceleration can help users upload data through AWS edge locations.

```text
User
 |
 v
AWS Edge Location
 |
 v
AWS Network
 |
 v
S3 Bucket
```

It can be useful when users are geographically far from the S3 bucket's region.

It is not automatically necessary for every application.

---

# 24. Monitoring and Auditing

## CloudTrail

CloudTrail records AWS API activity for auditing.

Questions it can help answer:

```text
Who performed the operation?
What operation happened?
When did it happen?
Which resource was involved?
```

## CloudWatch

CloudWatch is useful for:

- Metrics
- Monitoring
- Alarms
- Operational visibility

## S3 Access Logging

S3 server access logging can provide request logs when configured.

## CloudTrail Data Events

For detailed object-level API activity, CloudTrail data events can be configured for S3.

---

# 25. Cost Optimization

S3 costs can come from more than storage.

```text
S3 Cost
 |
 +-- Storage
 +-- Requests
 +-- Data retrieval
 +-- Data transfer
 +-- Replication
 +-- KMS requests
 +-- Optional features
```

## Cost Optimization Techniques

### Lifecycle Policies

Move older objects to cheaper storage classes.

### Intelligent-Tiering

Useful when access patterns are unpredictable.

### Delete Unnecessary Data

Especially:

- Old versions
- Temporary files
- Incomplete multipart uploads

### Review Retrieval Costs

Archive classes can have retrieval charges and different retrieval characteristics.

### S3 Bucket Keys

With SSE-KMS, Bucket Keys can reduce KMS request volume.

---

# 26. S3 Consistency

S3 provides **strong read-after-write consistency** for object operations.

After a successful write, subsequent reads can immediately reflect the new object state.

```text
PUT Object
   |
   v
 S3
   |
   v
GET Object
   |
   v
Latest Object
```

This simplifies many application designs.

---

# 27. AWS CLI

There are two major CLI styles for S3.

## High-Level Commands

```bash
aws s3
```

### List Buckets

```bash
aws s3 ls
```

### List Objects

```bash
aws s3 ls s3://my-bucket
```

### Upload

```bash
aws s3 cp file.txt s3://my-bucket/
```

### Download

```bash
aws s3 cp s3://my-bucket/file.txt .
```

### Delete

```bash
aws s3 rm s3://my-bucket/file.txt
```

### Sync

```bash
aws s3 sync ./website s3://my-bucket/website/
```

---

## Low-Level API Commands

```bash
aws s3api
```

### List Buckets

```bash
aws s3api list-buckets
```

### Inspect Object

```bash
aws s3api head-object   --bucket my-bucket   --key file.txt
```

### Check Versioning

```bash
aws s3api get-bucket-versioning   --bucket my-bucket
```

### Check Encryption

```bash
aws s3api get-bucket-encryption   --bucket my-bucket
```

### List Object Versions

```bash
aws s3api list-object-versions   --bucket my-bucket   --prefix file.txt
```

### High-Level vs Low-Level

```text
aws s3
   |
   +-- Simple common operations

aws s3api
   |
   +-- Detailed API-level operations
```

---

# 28. Common Troubleshooting

## AccessDenied

Possible causes:

- IAM policy does not allow the action
- Bucket policy denies access
- Block Public Access affects the request
- Wrong resource ARN
- Missing `s3:ListBucket`
- Missing `s3:GetObject`
- KMS permissions are missing
- Explicit deny exists

---

## NoSuchBucket

Check:

```bash
aws s3 ls
```

Then verify:

- Bucket name
- AWS account
- Region
- AWS CLI credentials

---

## Cannot List Objects

You may need:

```text
s3:ListBucket
```

on:

```text
arn:aws:s3:::my-bucket
```

---

## Cannot Download an Object

You may need:

```text
s3:GetObject
```

on:

```text
arn:aws:s3:::my-bucket/*
```

If SSE-KMS is used, KMS permissions may also be required.

---

## 403 Forbidden

A 403 can result from several security configurations.

Check:

```text
IAM
Bucket Policy
Block Public Access
Object Ownership
KMS
Resource ARN
```

Do not immediately make the bucket public to solve a 403.

---

# 29. Real-World Architecture

A production-style application might use S3 as its object-storage layer.

```text
                         INTERNET
                             |
                             v
                           ALB
                             |
                 +-----------+-----------+
                 |                       |
              EC2 #1                  EC2 #2
              Docker                  Docker
                 |                       |
                 +-----------+-----------+
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
              RDS PostgreSQL             S3
                                      Private Bucket
                                         |
                          +--------------+--------------+
                          |              |              |
                       Images        Documents       Backups
```

Security model:

```text
Internet
   |
   v
ALB
   |
   v
Application EC2
   |
   +----> RDS
   |
   +----> S3
```

The application should normally use an **IAM role** attached to EC2 rather than storing long-term AWS access keys on the server.

---

# 30. Best Practices

## Security

- Keep sensitive buckets private.
- Keep Block Public Access enabled unless public access is intentionally required.
- Use IAM roles instead of long-term access keys on EC2.
- Follow least privilege.
- Use encryption.
- Use SSE-KMS when centralized key management or additional key-level controls are needed.
- Review bucket policies carefully.
- Avoid unnecessary ACL usage.
- Enable CloudTrail auditing where appropriate.

## Data Protection

- Enable Versioning for important data.
- Use lifecycle policies.
- Consider replication for disaster recovery requirements.
- Use Object Lock where immutability is required.
- Back up important data appropriately.

## Cost

- Choose storage classes based on access patterns.
- Use lifecycle transitions.
- Remove unnecessary versions.
- Abort incomplete multipart uploads.
- Monitor retrieval and data-transfer costs.
- Review KMS request costs when using SSE-KMS.

## Application Design

- Use presigned URLs for temporary private access.
- Use S3 events for event-driven workflows.
- Use CloudFront for global delivery of static content.
- Keep application secrets out of S3 object names and source code.
- Use meaningful prefixes:

```text
users/
products/
uploads/
logs/
backups/
```

---

# 31. Quick Revision

| Concept | Remember |
|---|---|
| S3 | Object storage |
| Bucket | Container for objects |
| Object | Data + key + metadata |
| Key | Object identifier |
| Versioning | Keeps object versions |
| Delete Marker | Marks an object as deleted in a versioned bucket |
| Lifecycle | Automates transition and expiration |
| SSE-S3 | S3-managed encryption |
| SSE-KMS | KMS-managed key control |
| IAM Policy | Identity-based access |
| Bucket Policy | Resource-based access |
| Block Public Access | Helps prevent unintended public access |
| Presigned URL | Temporary signed access |
| Access Point | Dedicated access endpoint/policy |
| Replication | Copies objects to another bucket |
| Object Lock | WORM-style retention |
| Multipart Upload | Uploads large files in parts |
| Event Notification | Triggers downstream services |
| CloudTrail | API auditing |
| CloudWatch | Monitoring and operational visibility |

---

# Practical S3 Learning Project

After completing the theory, build a real project around **Cloud Shop**.

```text
Cloud Shop
    |
    +---- EC2 + Docker
    |
    +---- S3
           |
           +---- Private bucket
           +---- Versioning
           +---- Encryption
           +---- Lifecycle
           +---- IAM role
           +---- Presigned URLs
           +---- Event notifications
```

The purpose of the project is to demonstrate **why** each S3 feature is used, not simply to create AWS resources.

---

# Final Mental Model

Think of S3 as:

```text
                    AMAZON S3
                        |
        +---------------+---------------+
        |               |               |
      Buckets         Objects      Storage Classes
        |               |               |
        |               |          +----+----+
        |               |          |         |
     Policies          Keys      Standard   Glacier
        |
   +----+----+
   |         |
  IAM     Bucket Policy
   |
   v
Security
   |
   +-- Block Public Access
   +-- Encryption
   +-- Object Ownership
   +-- Least Privilege
   |
   v
Data Management
   |
   +-- Versioning
   +-- Lifecycle
   +-- Replication
   +-- Object Lock
   |
   v
Application Integration
   |
   +-- Presigned URLs
   +-- Lambda
   +-- SQS
   +-- SNS
   +-- EventBridge
```

> **S3 = Object Storage + Security + Data Management + Automation**

---


GitHub: [SkyInfra](https://github.com/SkyInfra)
