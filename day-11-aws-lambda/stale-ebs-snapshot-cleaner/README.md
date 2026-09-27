# Day 11 – AWS Lambda

AWS Lambda is a serverless compute service that allows you to run code without managing servers.

In this day, I learned the fundamentals of AWS Lambda and built a practical automation project using Python and Boto3.

---

## What I Learned

- What AWS Lambda is
- Serverless computing
- Lambda functions and handlers
- Lambda runtimes
- IAM permissions and execution roles
- Lambda testing
- CloudWatch Logs
- Event-driven architecture
- EventBridge Scheduler
- Lambda with Boto3
- Cost optimization using Lambda
- Safety mechanisms for automation

---

## 1. What is AWS Lambda?

AWS Lambda is a serverless compute service provided by AWS.

It allows us to run code without provisioning or managing servers.

Instead of manually creating and maintaining a server:

```text
Create EC2 Server
        ↓
Install Operating System
        ↓
Install Runtime
        ↓
Deploy Application
        ↓
Maintain Server
```

Lambda allows us to:

```text
Write Code
    ↓
Deploy Lambda Function
    ↓
AWS Runs the Code
```

AWS manages the underlying infrastructure while we focus mainly on the application code.

---

## 2. Serverless Computing

Serverless does not mean that servers do not exist.

Servers are still used, but AWS manages the infrastructure for us.

```text
Developer
    ↓
Lambda Function
    ↓
AWS Managed Infrastructure
    ↓
Code Execution
```

We do not need to manually manage an EC2 server for the Lambda function.

---

## 3. Lambda Function

A Lambda function is a piece of code that performs a specific task.

Example:

```python
def lambda_handler(event, context):
    print("Hello from AWS Lambda")

    return {
        "statusCode": 200,
        "body": "Hello World"
    }
```

The Lambda function contains a handler that AWS calls when the function is invoked.

---

## 4. Lambda Handler

The handler is the function that AWS Lambda executes.

```python
def lambda_handler(event, context):
    ...
```

### event

The `event` parameter contains information about the event that triggered the Lambda function.

### context

The `context` parameter contains information about the current Lambda execution environment.

---

## 5. Lambda Runtime

The runtime provides the environment required to execute the Lambda code.

For this project, Python was used.

```text
AWS Lambda
    │
    ├── Runtime: Python
    │
    └── Function Code
```

---

## 6. Lambda Architecture

A basic Lambda architecture looks like this:

```text
              Event
                │
                ▼
        ┌───────────────┐
        │ AWS Lambda    │
        │   Function    │
        └───────┬───────┘
                │
                ▼
          Execute Code
                │
                ▼
          AWS Services
```

Lambda can be triggered by services such as:

- EventBridge
- S3
- API Gateway
- SQS
- SNS
- DynamoDB

---

## 7. Lambda + EventBridge Scheduler

For scheduled automation, EventBridge Scheduler can invoke a Lambda function.

```text
EventBridge Scheduler
        │
        │ Every 1 Day
        ▼
AWS Lambda
        │
        ▼
Python / Boto3
        │
        ▼
AWS Resources
```

This allows us to automate tasks without running a server continuously.

---

## 8. IAM and Lambda

Lambda needs permission to interact with AWS resources.

These permissions are provided through an IAM execution role.

```text
Lambda Function
      │
      ▼
IAM Execution Role
      │
      ▼
AWS Permissions
      │
      ▼
AWS Services
```

---

## 9. Lambda Execution Role

For the stale EBS snapshot cleaner project, the Lambda required permissions to:

- Describe EBS snapshots
- Describe EBS volumes
- Delete EBS snapshots

The project used `AmazonEC2ReadOnlyAccess` along with an additional permission for:

```text
ec2:DeleteSnapshot
```

> In production, permissions should be restricted as much as practical instead of granting broad permissions.

---

## 10. Lambda Testing

Before connecting Lambda to an automated trigger, it is useful to test the function manually.

```text
Write Code
    ↓
Deploy Code
    ↓
Create Test Event
    ↓
Invoke Lambda
    ↓
Check Result
    ↓
Check CloudWatch Logs
```

During this project, Lambda was tested several times while adding functionality.

---

## 11. CloudWatch Logs

AWS Lambda automatically sends execution logs to Amazon CloudWatch Logs.

Useful information includes:

- Function execution messages
- Errors
- Debug information
- Execution duration
- Execution results

Example:

```text
Total snapshots found: 1

Checking snapshot: snap-xxxxxxxx
Source volume: vol-xxxxxxxx
Snapshot age: 0 days

ACTIVE: Source volume exists.
```

CloudWatch is useful for troubleshooting and monitoring Lambda functions.

---

## 12. Lambda Timeout

Every Lambda function has a timeout.

If the function does not finish within the configured timeout, Lambda terminates the execution.

During this project, the initial timeout was too short and caused:

```text
Sandbox.Timedout
```

The timeout was increased to:

```text
30 seconds
```

After that, the function completed successfully.

---

# Practical Project

## Stale EBS Snapshot Cleaner

The hands-on project for this day was a serverless AWS cost-optimization automation.

The goal was to identify EBS snapshots whose original source volume no longer exists and determine whether they are safe candidates for deletion.

Project folder:

```text
stale-ebs-snapshot-cleaner/
├── lambda_function.py
└── README.md
```

---

## Project Architecture

```text
                    EventBridge Scheduler
                           │
                           │ Every 1 Day
                           ▼
                  ┌──────────────────┐
                  │   AWS Lambda     │
                  │ Python + Boto3   │
                  └────────┬─────────┘
                           │
                           ▼
                    EC2 / EBS APIs
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       EBS Snapshots              EBS Volumes
              │                         │
              └────────────┬────────────┘
                           ▼
                  Safety Conditions
                           │
                           ▼
                  Eligible Snapshots
```

---

## Project Logic

The Lambda function follows these steps:

```text
1. Get all owned EBS snapshots
            ↓
2. Check the source volume
            ↓
3. Does the source volume exist?
       ┌────┴────┐
      YES        NO
       │          │
       ▼          ▼
    Keep       Check Age
                  │
                  ▼
        Is Snapshot >= 30 Days?
             ┌────┴────┐
            NO         YES
             │           │
             ▼           ▼
           Keep      Check Tag
                         │
                         ▼
                 Retention=Keep?
                    ┌────┴────┐
                   YES        NO
                    │          │
                    ▼          ▼
                  Keep       Eligible
```

---

## Safety Mechanisms

Deleting cloud resources automatically can be dangerous.

Therefore, the project includes multiple safety checks.

### 1. Dry Run

```python
DRY_RUN = True
```

When dry run is enabled, the function reports what it would delete without actually deleting the snapshot.

Example:

```text
DRY RUN: Would delete snapshot snap-xxxxxxxx
```

### 2. Age Threshold

A snapshot must be at least 30 days old before it becomes eligible.

```python
MAX_AGE_DAYS = 30
```

### 3. Retention Protection Tag

Snapshots can be protected using:

```text
Retention=Keep
```

If the tag exists, the Lambda skips the snapshot.

---

## Testing the Project

The project was tested using a temporary EBS volume and snapshot.

```text
Create EBS Volume
        ↓
Create Snapshot
        ↓
Run Lambda
        ↓
Check Source Volume
        ↓
Delete Source Volume
        ↓
Run Lambda Again
        ↓
Identify Stale Snapshot
```

The Lambda successfully detected when the source volume no longer existed.

---

## Example Output

```text
Total snapshots found: 1

Checking snapshot: snap-xxxxxxxx
Source volume: vol-xxxxxxxx
Snapshot age: 0 days

PROTECTED: Snapshot has Retention=Keep

========== SUMMARY ==========
Total snapshots: 1
Stale snapshots: 0
Protected snapshots: 1
Eligible snapshots: 0
Dry run: True
```

Another test identified a stale snapshot:

```text
STALE: Source volume vol-xxxxxxxx no longer exists.

ELIGIBLE: Snapshot is older than 30 days.

DRY RUN: Would delete snapshot snap-xxxxxxxx
```

---

## EventBridge Scheduler

The Lambda function was connected to an EventBridge Scheduler.

Schedule:

```text
Every 1 Day
```

Scheduler:

```text
stale-ebs-snapshot-cleaner-daily
```

Target:

```text
AWS Lambda
    ↓
stale-ebs-snapshot-cleaner
```

This allows the cleanup process to run automatically on a schedule.

---

## Monitoring

Lambda execution can be monitored through the AWS Lambda monitoring page and CloudWatch.

Useful metrics include:

- Invocations
- Errors
- Duration
- Throttles
- Concurrent executions

CloudWatch Logs can be used to inspect individual executions.

---

## Cost Optimization

Lambda can help automate cloud cost optimization tasks.

```text
Unused Resources
       ↓
Identify Automatically
       ↓
Apply Safety Conditions
       ↓
Remove Eligible Resources
       ↓
Reduce Unnecessary Costs
```

In this project, stale EBS snapshots were the target resource.

> A snapshot being stale does not automatically mean it should be deleted. Retention policies, backups, compliance requirements, and other dependencies should be considered in a production environment.

---

## Production Considerations

Before using automated deletion in a production AWS account, consider:

- AWS Backup managed resources
- EBS Data Lifecycle Manager (DLM)
- Required retention policies
- Compliance requirements
- Disaster recovery requirements
- Snapshot dependencies
- Resource tagging standards
- IAM least privilege
- Logging and alerting
- Dry-run testing

---

## IAM Least Privilege

The project used convenient permissions during development.

A production implementation should ideally use only the required actions, such as:

```text
ec2:DescribeSnapshots
ec2:DescribeVolumes
ec2:DeleteSnapshot
```

and restrict permissions as much as practical.

---

## Project Structure

```text
projects/
└── day-11-aws-lambda/
    ├── README.md
    │
    └── stale-ebs-snapshot-cleaner/
        ├── lambda_function.py
        └── README.md
```

---

## Key Takeaways

After completing this project, I learned how to:

- Create an AWS Lambda function
- Write Lambda functions using Python
- Use Boto3 with AWS services
- Configure Lambda IAM permissions
- Test Lambda functions
- Troubleshoot Lambda timeout issues
- Read Lambda logs through CloudWatch
- Use EventBridge Scheduler
- Automate AWS resource checks
- Implement dry-run protection
- Use resource tags for protection
- Add age-based conditions
- Build a serverless cost-optimization workflow

---

## What I Built

```text
AWS Lambda
     │
     ├── Python
     ├── Boto3
     ├── IAM
     ├── CloudWatch
     ├── EventBridge Scheduler
     │
     ▼
Stale EBS Snapshot Cleaner
     │
     ├── Source Volume Check
     ├── 30-Day Age Protection
     ├── Retention=Keep Protection
     └── Dry-Run Safety
```

This project gave me practical experience with serverless automation and AWS resource management.

---

## Next Topics

- API Gateway + Lambda
- Lambda + S3
- Lambda environment variables
- Lambda layers
- Lambda concurrency
- Lambda performance optimization
- Infrastructure as Code for Lambda
- CI/CD deployment for Lambda
