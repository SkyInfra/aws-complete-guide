# AWS Day 19 — AWS Cloud Migration

## 1. Introduction

AWS Cloud Migration is the process of moving applications, servers, databases, files, and other IT resources from an existing environment to Amazon Web Services (AWS).

An organization may migrate from:
- On-premises data centers
- Physical servers
- Virtual machines
- Another cloud provider
- Existing self-managed infrastructure

The main goal is to improve scalability, availability, security, operational efficiency, and flexibility while managing costs.

### Real-World Scenario

Imagine an e-commerce company running its Node.js application and database on a single EC2 instance. When traffic increases during a sale, the application becomes slow. If the instance fails, the entire website may become unavailable.

The company decides to migrate toward a more reliable AWS architecture using services such as Amazon EC2, Amazon RDS, Amazon S3, Elastic Load Balancing, and Amazon CloudWatch.

The migration must be carefully planned so that customer data is preserved and downtime is minimized.

---

## 2. Why Do Organizations Migrate to AWS?

### Scalability
AWS allows organizations to increase or decrease computing resources according to demand.

### High Availability
Applications can be distributed across multiple Availability Zones to reduce the impact of individual infrastructure failures.

### Cost Management
Organizations can select appropriate resource sizes and pay for many services according to their usage.

### Security
AWS provides services for identity management, encryption, logging, monitoring, and security assessment.

### Disaster Recovery
Applications and data can be backed up or replicated to support recovery from failures.

### Faster Deployment
Infrastructure can be provisioned using automation and Infrastructure as Code rather than manual configuration.

**Important:** Migrating to AWS does not automatically make an application secure, highly available, or inexpensive. These outcomes depend on architecture, configuration, monitoring, and ongoing management.

---

## 3. The AWS Migration Strategies: The 7 Rs

The 7 Rs describe common approaches organizations use to decide what to do with each application or workload.

### 3.1 Rehost — Lift and Shift

Move an application to AWS with minimal changes.

**Example:** Move an existing application server from an on-premises virtual machine to Amazon EC2.

**Suitable when:**
- Migration needs to happen quickly.
- The application cannot be changed immediately.
- The organization wants to leave its existing data center.

**Trade-off:** Existing operational and architectural problems may remain.

### 3.2 Replatform — Lift, Tinker, and Shift

Make limited improvements during migration without completely redesigning the application.

**Example:** Move an application to EC2 but migrate its self-managed database to Amazon RDS.

**Suitable when:**
- Some managed AWS services can reduce maintenance.
- The application does not require a complete rewrite.

### 3.3 Refactor or Re-architect

Redesign or modify an application to take advantage of cloud-native capabilities.

**Example:** Break a monolithic application into services, introduce automated scaling, and use managed messaging or database services.

**Suitable when:**
- The existing architecture limits scalability.
- The business requires greater agility or resilience.

**Trade-off:** Usually requires more time, testing, development effort, and budget.

### 3.4 Repurchase

Replace an existing application with a different product, often a SaaS solution.

**Example:** Replace a self-hosted business email system with a managed email platform.

### 3.5 Retire

Remove applications or resources that are no longer needed.

**Example:** Decommission an obsolete reporting server after confirming that no business process depends on it.

### 3.6 Retain

Keep an application in its current environment for now.

**Example:** Retain a legacy application that depends on specialized hardware or has regulatory constraints.

### 3.7 Relocate

Move an existing infrastructure environment to AWS with minimal architectural changes, often using a supported virtualization or migration approach.

**Example:** Move a compatible VMware workload environment to an AWS-supported VMware environment.

### Strategy Comparison

| Strategy | Main idea | Example |
|---|---|---|
| Rehost | Move with minimal changes | Existing server to EC2 |
| Replatform | Make limited improvements | Database to RDS |
| Refactor | Redesign the application | Adopt cloud-native architecture |
| Repurchase | Replace the product | Adopt a SaaS solution |
| Retire | Remove unnecessary workloads | Decommission unused server |
| Retain | Keep the workload where it is | Keep a constrained legacy system |
| Relocate | Move an existing environment | Move a compatible VMware environment |

---

## 4. Important AWS Migration Tools

### 4.1 AWS Application Migration Service (AWS MGN)

AWS MGN helps migrate compatible source servers to AWS with a block-level replication approach. It is commonly used for rehosting servers.

**Use case:** An organization wants to migrate a supported application server to EC2 without manually rebuilding the entire operating system environment.

**Typical workflow:**
1. Prepare the source server and AWS permissions.
2. Install and configure the required replication agent.
3. Replicate source-server data to AWS.
4. Launch test instances.
5. Validate the application.
6. Perform the planned cutover.

### 4.2 AWS Database Migration Service (AWS DMS)

AWS DMS helps migrate data between supported databases. Depending on the source, target, and configuration, it can support a one-time migration and ongoing change replication.

**Use case:** Move a self-managed PostgreSQL database to a supported managed database target.

**Important:** Database schema conversion may require separate preparation, such as AWS Schema Conversion Tool functionality or other compatible schema-conversion methods.

### 4.3 AWS DataSync

AWS DataSync automates and accelerates data transfers between supported storage locations.

**Use case:** Transfer large directories of product images and documents from a file server to Amazon S3.

### 4.4 AWS Snow Family

AWS Snow Family devices support physical data transfer and certain edge-computing use cases. Their availability and product options should be checked for the intended location and workload.

**Use case:** Transfer a very large dataset when network bandwidth or transfer time makes an online migration impractical.

### 4.5 Discovery and Assessment Tools

Discovery and assessment help teams understand existing servers, dependencies, utilization, and migration requirements before moving workloads.

**Use case:** Identify which applications depend on a particular database or server before planning a migration.

---

## 5. The AWS Migration Process

A successful migration follows a structured process.

### Step 1: Discovery and Assessment

Understand the existing environment before moving anything.

Identify:
- Application servers and operating systems
- CPU, memory, and storage utilization
- Databases and data volumes
- Application dependencies
- Network requirements
- Security and compliance needs
- Business-critical workloads
- Recovery requirements and acceptable downtime

**Example:** Discover that an e-commerce application requires Node.js, a PostgreSQL database, product images, environment variables, and an external payment API.

**Deliverable:** An inventory of workloads, dependencies, and migration risks.

### Step 2: Migration Planning

Choose a migration strategy for each workload.

Define:
- Target AWS services
- Target AWS Region
- Network and security architecture
- Migration order
- Expected downtime
- Data migration method
- Testing criteria
- Rollback procedure
- Budget and resource ownership

**Example:** Rehost a legacy application server initially, migrate the database to RDS after compatibility checks, and move static images to S3.

**Deliverable:** A migration plan with responsibilities, milestones, and rollback conditions.

### Step 3: Prepare the AWS Environment

Build and secure the target environment before migrating production workloads.

Typical tasks include:
1. Select the AWS account and Region.
2. Design the VPC and subnets.
3. Configure routing and security groups.
4. Configure IAM roles and least-privilege permissions.
5. Configure encryption and secure secret storage.
6. Set up logging, monitoring, and budget alerts.
7. Prepare backups and infrastructure automation.

**Example architecture:**

Internet → Application Load Balancer → EC2 application instances → Amazon RDS

Amazon S3 stores static assets, while Amazon CloudWatch collects logs and metrics.

The exact architecture depends on application requirements.

### Step 4: Migrate Applications and Data

Move the application, database, and files using an appropriate method.

| Component | Possible migration method |
|---|---|
| Existing server | AWS MGN or a fresh application deployment |
| Database | AWS DMS or a compatible database-native migration method |
| Files and directories | AWS DataSync |
| Static website assets | Amazon S3 upload or an appropriate transfer tool |
| Application configuration | Securely recreate configuration and move secrets to a suitable secrets service |

Do not assume that copying application files alone completes a migration. Dependencies, permissions, environment variables, data consistency, and network connectivity must also be addressed.

### Step 5: Test and Validate

Before sending real customer traffic to the migrated system, verify that it works correctly.

**Functional testing**
- Does the website load?
- Can users sign in?
- Can products be viewed?
- Can orders be placed?
- Do required integrations work?

**Database testing**
- Are records present?
- Are important tables and relationships correct?
- Do application queries work?
- Is the final migrated data consistent?

**Infrastructure testing**
- Are health checks passing?
- Can the application connect to its database?
- Are security groups restrictive enough?
- Are logs and monitoring working?

**Performance testing**
- Does the application handle expected traffic?
- Are response times acceptable?
- Are CPU, memory, and database resources appropriately sized?

### Step 6: Cutover to AWS

Cutover is the controlled process of directing production traffic to the migrated environment.

A typical sequence is:

1. Announce the maintenance window if needed.
2. Pause or control writes to the old system when required.
3. Complete the final data synchronization.
4. Verify the target application's health and data consistency.
5. Switch traffic using the planned DNS, load balancer, or routing method.
6. Run production smoke tests.
7. Monitor errors, latency, and resource usage.
8. Execute the rollback plan if critical acceptance criteria fail.

**Important:** A running EC2 instance does not prove that migration is complete. The application, database, network, security, and customer-facing workflows must all be validated.

### Step 7: Monitor, Optimize, and Decommission

After cutover:
- Monitor application and infrastructure metrics with Amazon CloudWatch.
- Review application and system logs.
- Confirm backups and recovery procedures.
- Right-size resources based on observed utilization.
- Review costs and remove unnecessary resources.
- Update architecture diagrams and operational documentation.
- Retire the old environment only after acceptance and rollback requirements are satisfied.

**Deliverable:** A documented, monitored, and operational AWS environment.

---

## 6. Migration Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Data loss | Backups, replication checks, and data validation |
| Extended downtime | Plan cutover, test migration, and reduce final synchronization time |
| Application incompatibility | Assess dependencies and test in advance |
| Unexpected AWS costs | Estimate costs, configure budgets, and monitor usage |
| Security exposure | Apply least privilege, encryption, and restrictive network rules |
| Performance problems | Load-test and right-size resources |
| Failed cutover | Define rollback conditions and preserve the old environment until acceptance |

---

## 7. Practical Example: Migrating an E-Commerce Application

### Existing environment

A company currently runs:
- Node.js/Express application
- Database hosted on the same server
- Product images stored on the server's disk
- Manual deployments
- Limited monitoring
- Configuration stored in local files

### Possible target environment

- **Amazon EC2:** Run the application.
- **Application Load Balancer:** Distribute incoming HTTP/HTTPS traffic across configured targets.
- **Amazon RDS:** Host a supported relational database engine.
- **Amazon S3:** Store product images and other suitable static assets.
- **AWS Secrets Manager or Systems Manager Parameter Store:** Store appropriate secrets and configuration.
- **Amazon CloudWatch:** Collect metrics, logs, and alarms.
- **IAM:** Control access to AWS resources.
- **Amazon VPC:** Provide network isolation and routing.

These are target-state options, not a requirement to create every service immediately. The architecture should match the project's security, availability, recovery, and budget requirements.

### Migration mapping

| Existing component | Target approach |
|---|---|
| Application server | Rehost or deploy the application on EC2 |
| Self-managed database | Migrate to RDS after compatibility assessment |
| Product images | Transfer to S3 and update application references |
| Local configuration files | Recreate configuration securely |
| Manual deployment | Introduce a tested deployment pipeline |
| Limited monitoring | Configure CloudWatch metrics, logs, and alarms |

### Success criteria

The migration is successful when:
- The website is reachable through its intended endpoint.
- Application health checks pass.
- Database records are correct.
- Core customer workflows work.
- Security controls are verified.
- Logs, alarms, and backups are operational.
- Costs and ongoing operational responsibilities are understood.
- A recovery and rollback plan is documented.

---

## 8. Key Takeaways

- AWS migration is a planned process, not simply copying files to EC2.
- The 7 Rs help teams choose the right strategy for each workload.
- AWS MGN supports server rehosting; AWS DMS supports database migration; AWS DataSync supports data transfer.
- Assessment and planning should happen before production changes.
- Testing and data validation are essential before cutover.
- Monitoring, cost optimization, security, and recovery planning continue after migration.
- A successful migration must satisfy business and technical acceptance criteria.

## 9. Further Reading

- AWS Cloud Adoption Framework: https://aws.amazon.com/cloud-adoption-framework/
- AWS Migration Hub: https://aws.amazon.com/migration-hub/
- AWS Application Migration Service: https://aws.amazon.com/application-migration-service/
- AWS Database Migration Service: https://aws.amazon.com/dms/
- AWS DataSync: https://aws.amazon.com/datasync/
- AWS Snow Family: https://aws.amazon.com/snow/

---

**Day 19 Complete — AWS Cloud Migration**

Next, practice designing a migration plan for a real application, including its source architecture, target AWS services, data migration, testing, cutover, rollback, and cost controls.
