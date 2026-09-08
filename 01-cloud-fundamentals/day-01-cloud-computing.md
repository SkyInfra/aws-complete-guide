# Day 1 — Cloud Computing Fundamentals ☁️

> **AWS Complete Guide — Day 1 of 30**

## 📚 Topics Covered

* What is Cloud Computing?
* Traditional IT vs Cloud Computing
* What is AWS?
* Why do companies use Cloud Computing?
* On-Demand Resources
* Scalability
* Elasticity
* High Availability
* Fault Tolerance
* Reliability
* AWS Global Infrastructure
* AWS Region
* Availability Zone
* Data Center
* IaaS, PaaS, and SaaS
* Shared Responsibility Model
* CAPEX vs OPEX
* Pay-As-You-Go
* Cloud Computing Real-World Example
* Cloud Computing from a DevOps Perspective

---

# 1. What is Cloud Computing?

**Cloud computing is the delivery of computing resources over the internet instead of buying and managing physical infrastructure yourself.**

Computing resources can include:

* Servers
* Storage
* Databases
* Networking
* Applications
* Security
* Monitoring
* AI/ML services

### Traditional approach

If we want to host an application using our own infrastructure:

```text
Buy Physical Server
       ↓
Install Operating System
       ↓
Configure Network
       ↓
Install Application
       ↓
Maintain Hardware
       ↓
Pay for Electricity
       ↓
Handle Hardware Failures
```

### Cloud approach

With cloud computing:

```text
User
  ↓
Cloud Provider
  ↓
Request Resources
  ↓
Cloud Provider Provides Resources
  ↓
Deploy Application
```

Instead of owning the physical server, we use computing resources provided by a cloud provider.

---

# 2. What is AWS?

**AWS stands for Amazon Web Services.**

AWS is a cloud computing platform provided by Amazon.

AWS provides many different services for building, deploying, securing, and monitoring applications.

Some important AWS services are:

| Service    | Purpose                        |
| ---------- | ------------------------------ |
| EC2        | Virtual servers                |
| S3         | Object storage                 |
| VPC        | Virtual networking             |
| IAM        | Identity and access management |
| RDS        | Managed relational databases   |
| DynamoDB   | NoSQL database                 |
| Lambda     | Serverless computing           |
| CloudWatch | Monitoring                     |
| Route 53   | DNS                            |
| CloudFront | Content delivery/CDN           |
| ECR        | Container image registry       |
| ECS        | Container orchestration        |
| EKS        | Managed Kubernetes             |

We will study these services throughout this 30-day AWS journey.

---

# 3. Traditional IT vs Cloud Computing

## Traditional IT

In traditional IT, a company may need to purchase and manage physical infrastructure.

```text
Company
   ↓
Physical Servers
   ↓
Storage
   ↓
Networking
   ↓
Data Center
   ↓
Application
```

The company may be responsible for:

* Buying hardware
* Installing servers
* Networking
* Electricity
* Cooling
* Hardware maintenance
* Hardware replacement
* Operating systems
* Security
* Scaling

This can require significant time and money.

---

## Cloud Computing

With cloud computing:

```text
Company
   ↓
AWS
   ↓
Cloud Resources
   ↓
Application
```

AWS manages the underlying physical infrastructure.

The customer manages the resources and software they are responsible for.

---

# 4. Why Do Companies Use Cloud Computing?

Cloud computing provides several important benefits.

### Main benefits

* Lower upfront infrastructure costs
* Fast resource provisioning
* Scalability
* Elasticity
* High availability
* Global infrastructure
* Automation
* Flexible resource usage
* Managed services
* Faster application deployment

Instead of waiting weeks or months to purchase and install physical servers, cloud resources can often be created within minutes.

---

# 5. On-Demand Resources

**On-demand means getting computing resources when you need them.**

For example:

```text
Need Server
    ↓
Create EC2 Instance
    ↓
Server Available
    ↓
Deploy Application
```

You don't have to physically purchase a server before starting.

This allows developers and companies to experiment and deploy applications much faster.

---

# 6. Scalability

**Scalability is the ability of a system to handle increased workload by increasing its resources.**

Imagine a website normally receives:

```text
1,000 users/day
```

One server might be enough.

During a large sale:

```text
100,000 users/day
```

The application may need additional computing capacity.

```text
Normal Traffic

Users
  ↓
Server
```

During high traffic:

```text
             Users
               ↓
       ┌───────┼───────┐
       ↓       ↓       ↓
    Server  Server  Server
```

More resources are added to handle the increased workload.

---

# 7. Vertical Scaling

Vertical scaling means increasing the power of an existing server.

For example:

```text
Before:

2 CPU
4 GB RAM

       ↓

After:

8 CPU
32 GB RAM
```

The server itself becomes more powerful.

This is also called:

**Scaling Up**

---

# 8. Horizontal Scaling

Horizontal scaling means adding more servers.

```text
Before:

Server 1


After:

Server 1
Server 2
Server 3
Server 4
```

This is also called:

**Scaling Out**

Horizontal scaling is very important in cloud architecture because applications can distribute traffic across multiple servers.

---

# 9. Elasticity

**Elasticity is the ability to automatically increase or decrease resources according to demand.**

Example:

```text
Normal Traffic
      ↓
2 Servers
```

Traffic increases:

```text
High Traffic
      ↓
10 Servers
```

Traffic decreases:

```text
Low Traffic
      ↓
2 Servers
```

The important idea is:

```text
Increase resources when needed
             +
Decrease resources when no longer needed
```

### Scalability vs Elasticity

| Scalability                          | Elasticity                                 |
| ------------------------------------ | ------------------------------------------ |
| Ability to handle increased workload | Automatically adjusts resources            |
| Can involve adding resources         | Can increase AND decrease resources        |
| May be manual or automatic           | Usually associated with dynamic adjustment |

---

# 10. High Availability

**High Availability (HA) means designing a system so that it remains available even when some components fail.**

Consider a simple application:

```text
Users
  ↓
Server
```

If the server fails:

```text
Users
  X
Server ❌
```

The application becomes unavailable.

A highly available design could use multiple servers:

```text
              Users
                ↓
          Load Balancer
            ↙       ↘
        Server 1   Server 2
           ✅         ✅
```

If Server 1 fails:

```text
              Users
                ↓
          Load Balancer
                ↓
            Server 2
               ✅
```

The application can continue serving users.

---

# 11. Fault Tolerance

**Fault tolerance means a system can continue operating even when one or more components fail.**

Example:

```text
Server 1 ❌
Server 2 ✅
Server 3 ✅
```

The system continues operating because other components are available.

The goal is to prevent a single failure from bringing down the entire system.

---

# 12. Reliability

**Reliability means a system consistently performs correctly and remains dependable over time.**

A reliable application should:

```text
Request
   ↓
Application
   ↓
Correct Response
```

consistently without frequent failures.

Reliability is an important goal when designing cloud systems.

---

# 13. AWS Global Infrastructure

AWS operates infrastructure in many geographical locations around the world.

The main concepts we need to understand are:

```text
AWS Region
     ↓
Availability Zones
     ↓
Data Centers
```

There are also other global infrastructure concepts such as:

* Edge Locations
* Points of Presence

We will study these in detail on **Day 2**.

---

# 14. AWS Region

An **AWS Region** is a geographical area where AWS has infrastructure.

Examples of AWS Regions include:

```text
US East
Europe
Asia Pacific
Middle East
```

Each AWS Region has a unique region code.

Examples:

```text
us-east-1
```

and

```text
ap-south-1
```

The exact services and availability can vary between regions.

---

# 15. Why Are There Multiple Regions?

Multiple regions allow applications and organizations to choose where their infrastructure runs.

Reasons include:

### 1. Lower latency

Deploying closer to users can reduce network latency.

### 2. Data residency

Some organizations need data to remain within a particular geographical area.

### 3. Disaster recovery

Applications can be deployed across different regions to improve disaster recovery capabilities.

### 4. Availability

Using multiple geographical locations can reduce dependence on a single location.

---

# 16. Availability Zone

An **Availability Zone (AZ)** is an isolated location within an AWS Region.

Conceptually:

```text
AWS Region
│
├── Availability Zone A
│
├── Availability Zone B
│
└── Availability Zone C
```

A region can contain multiple Availability Zones.

Availability Zones are designed to provide isolation from failures in other Availability Zones.

This allows applications to be designed for high availability.

---

# 17. Data Center

A **data center** is a physical facility containing computing infrastructure.

It contains things such as:

* Servers
* Storage systems
* Networking equipment
* Power systems
* Cooling systems
* Physical security

Conceptually:

```text
Data Center
│
├── Servers
├── Storage
├── Networking
├── Power
└── Cooling
```

Cloud users normally don't manage the physical data centers themselves.

---

# 18. Region vs Availability Zone

This distinction is very important.

### Region

A geographical area.

```text
Region
```

### Availability Zone

An isolated location within that region.

```text
Region
│
├── AZ 1
├── AZ 2
└── AZ 3
```

Remember:

> **Region = geographical area**

> **Availability Zone = isolated infrastructure location inside a Region**

---

# 19. IaaS, PaaS, and SaaS

Cloud services can be categorized into different service models.

The three important models are:

```text
IaaS
PaaS
SaaS
```

---

# 20. IaaS — Infrastructure as a Service

**IaaS provides infrastructure resources such as virtual machines, storage, and networking.**

Example:

**Amazon EC2**

With EC2, the customer can manage things such as:

* Operating system
* Applications
* Packages
* Configuration
* Security configuration

AWS manages the underlying physical infrastructure.

Conceptually:

```text
You
 ↓
Application
 ↓
Operating System
 ↓
Virtual Machine
 ↓
AWS Infrastructure
```

IaaS gives the customer more control.

---

# 21. PaaS — Platform as a Service

**PaaS provides a platform where developers can focus more on their applications instead of managing the underlying infrastructure.**

Conceptually:

```text
You
 ↓
Application
 ↓
Platform
 ↓
Infrastructure
```

The cloud provider manages more of the underlying environment.

The developer focuses primarily on the application.

---

# 22. SaaS — Software as a Service

**SaaS is software delivered as a service over the internet.**

The user generally doesn't manage the underlying infrastructure.

Conceptually:

```text
User
 ↓
Software
 ↓
Cloud Provider
```

Examples outside AWS include:

* Gmail
* Microsoft 365
* Salesforce

The user mainly uses the software rather than managing servers and operating systems.

---

# 23. IaaS vs PaaS vs SaaS

| Model | Customer Responsibility                | Provider Responsibility      |
| ----- | -------------------------------------- | ---------------------------- |
| IaaS  | More control and management            | Infrastructure               |
| PaaS  | Application and data                   | Platform + infrastructure    |
| SaaS  | Mostly application usage/configuration | Almost everything underneath |

### Simple way to remember

```text
IaaS → You manage more
PaaS → Provider manages more
SaaS → Provider manages almost everything
```

---

# 24. Shared Responsibility Model

The **Shared Responsibility Model** is one of the most important concepts in AWS.

Security responsibilities are shared between:

```text
AWS
 +
Customer
```

A simple way to remember it:

> **AWS is responsible for security OF the cloud.**

> **The customer is responsible for security IN the cloud.**

---

# 25. AWS Responsibility

AWS is responsible for the underlying infrastructure.

Examples include:

* Physical data centers
* Physical servers
* Physical networking
* Physical facilities
* Underlying cloud infrastructure

Conceptually:

```text
AWS
 ↓
Physical Infrastructure
 ↓
Data Centers
 ↓
Networking
```

---

# 26. Customer Responsibility

Depending on the service, customers can be responsible for:

* Data
* Applications
* IAM permissions
* Operating systems
* Network configuration
* Security configuration
* Access control

For example, if you create an EC2 server, you have significant responsibility for the operating system and software running on that server.

---

# 27. CAPEX vs OPEX

These terms are important when discussing traditional infrastructure versus cloud computing.

## CAPEX

**CAPEX = Capital Expenditure**

Money spent on purchasing physical assets.

Example:

```text
Company
 ↓
Buy Server
 ↓
$10,000
```

The company owns the hardware.

---

## OPEX

**OPEX = Operational Expenditure**

Money spent on ongoing operational needs.

Cloud computing can allow organizations to use resources without making the same large upfront hardware investment.

Conceptually:

```text
Use Cloud Resources
        ↓
Pay for Usage
```

---

# 28. Pay-As-You-Go

Many AWS services use usage-based pricing.

The basic idea is:

```text
Use Resources
      ↓
Pay According to Usage
```

Instead of buying a physical server upfront, you can provision cloud resources and pay according to the pricing model of the service.

### Important

Pay-as-you-go does **not** mean everything is free.

You must monitor your resources and understand AWS pricing.

For example, unnecessary resources running for a long time can generate charges.

---

# 29. Real-World Example

Imagine we build an online shopping website.

Users access the website:

```text
Users
  ↓
Website
```

A basic cloud architecture might eventually look like:

```text
                  Users
                    ↓
               Route 53
                  DNS
                    ↓
              CloudFront
                  CDN
                    ↓
             Load Balancer
                ↙      ↘
            EC2 #1    EC2 #2
                ↘      ↙
                  RDS
                Database
                    ↓
                   S3
             Images / Files
```

Each AWS service solves a different problem.

### Route 53

Handles DNS.

### CloudFront

Delivers content closer to users.

### Load Balancer

Distributes traffic between servers.

### EC2

Runs the application.

### RDS

Provides a managed relational database.

### S3

Stores objects such as images and files.

We will learn these services individually throughout the 30-day course.

---

# 30. Cloud Computing from a DevOps Perspective

For a Cloud/DevOps engineer, AWS should not be learned as a list of service names.

Instead, think about the problems infrastructure needs to solve.

```text
Application
     ↓
Compute
     ↓
Networking
     ↓
Storage
     ↓
Database
     ↓
Security
     ↓
Monitoring
     ↓
Automation
     ↓
Deployment
```

For example:

### Compute

```text
EC2
ECS
EKS
Lambda
```

### Networking

```text
VPC
Subnet
Route Table
Internet Gateway
NAT Gateway
Load Balancer
Route 53
```

### Storage

```text
S3
EBS
EFS
```

### Database

```text
RDS
DynamoDB
```

### Security

```text
IAM
Security Groups
KMS
Secrets Manager
```

### Monitoring

```text
CloudWatch
CloudTrail
```

---

# 31. Important Terminology

| Term              | Meaning                                            |
| ----------------- | -------------------------------------------------- |
| Cloud Computing   | Computing resources delivered over a network       |
| AWS               | Amazon Web Services                                |
| Region            | Geographical AWS infrastructure area               |
| Availability Zone | Isolated location within a Region                  |
| Data Center       | Physical facility containing infrastructure        |
| Scalability       | Ability to handle increased workload               |
| Elasticity        | Ability to dynamically increase/decrease resources |
| High Availability | Designing systems to remain available              |
| Fault Tolerance   | Continuing operation despite failures              |
| Reliability       | Consistent and dependable operation                |
| IaaS              | Infrastructure as a Service                        |
| PaaS              | Platform as a Service                              |
| SaaS              | Software as a Service                              |
| CAPEX             | Capital expenditure                                |
| OPEX              | Operational expenditure                            |
| Pay-as-you-go     | Usage-based cloud pricing concept                  |

---

# 32. Key Concepts to Remember

### Cloud Computing

```text
Use computing resources without owning all the physical infrastructure.
```

### AWS

```text
Amazon's cloud computing platform.
```

### Region

```text
Geographical AWS location.
```

### Availability Zone

```text
Isolated location inside a Region.
```

### Scalability

```text
Ability to handle more workload.
```

### Elasticity

```text
Automatically increase/decrease resources according to demand.
```

### High Availability

```text
Keep the application available despite component failures.
```

### Fault Tolerance

```text
Continue operating when components fail.
```

### Shared Responsibility

```text
AWS + Customer share security responsibilities.
```

---

# 33. Day 1 Quick Revision

Before moving to Day 2, make sure you can answer these questions:

1. What is cloud computing?
2. What is AWS?
3. Why do companies use cloud computing?
4. What is scalability?
5. What is vertical scaling?
6. What is horizontal scaling?
7. What is elasticity?
8. What is high availability?
9. What is fault tolerance?
10. What is reliability?
11. What is an AWS Region?
12. What is an Availability Zone?
13. What is a Data Center?
14. What is the difference between Region and Availability Zone?
15. What is IaaS?
16. What is PaaS?
17. What is SaaS?
18. What is the Shared Responsibility Model?
19. What is CAPEX?
20. What is OPEX?
21. What does Pay-As-You-Go mean?

---

# 34. Day 1 Summary

The most important mental model from Day 1 is:

```text
                    CLOUD
                      │
                     AWS
                      │
       ┌──────────────┼──────────────┐
       │              │              │
    Compute        Storage        Network
       │              │              │
      EC2             S3             VPC
       │              │              │
       └──────────────┼──────────────┘
                      │
                   Database
                      │
                     RDS
```

And remember:

```text
Region
  ↓
Availability Zones
  ↓
Physical Infrastructure
```

Cloud computing allows organizations to obtain computing resources more quickly and flexibly without having to own and operate all of the underlying physical infrastructure themselves.

---

## ✅ Day 1 Completed

**Topic:** Cloud Computing Fundamentals

**Progress:** `1 / 30`

**Next:** Day 2 — AWS Global Infrastructure
