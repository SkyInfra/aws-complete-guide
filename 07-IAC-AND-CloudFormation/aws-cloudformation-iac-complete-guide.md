# AWS Infrastructure as Code (IaC) with CloudFormation — Complete Hands-On Guide

A practical, beginner-to-intermediate guide to AWS Infrastructure as Code using AWS CloudFormation, with a real project you can deploy, understand, version-control, and publish on GitHub.

> **Goal:** Learn IaC by building AWS infrastructure as code rather than manually creating resources in the AWS Console.

---

## Table of Contents

1. [What is Infrastructure as Code?](#1-what-is-infrastructure-as-code)
2. [Why AWS CloudFormation?](#2-why-aws-cloudformation)
3. [IaC Concepts You Need to Know](#3-iac-concepts-you-need-to-know)
4. [Prerequisites](#4-prerequisites)
5. [AWS Cost and Security Notes](#5-aws-cost-and-security-notes)
6. [CloudFormation Template Anatomy](#6-cloudformation-template-anatomy)
7. [Lab 1 — Create an S3 Bucket](#7-lab-1--create-an-s3-bucket)
8. [Lab 2 — Parameters](#8-lab-2--parameters)
9. [Lab 3 — Outputs](#9-lab-3--outputs)
10. [Lab 4 — Intrinsic Functions](#10-lab-4--intrinsic-functions)
11. [Lab 5 — Build a VPC](#11-lab-5--build-a-vpc)
12. [Lab 6 — Deploy EC2 into Your VPC](#12-lab-6--deploy-ec2-into-your-vpc)
13. [Lab 7 — EC2 UserData and Nginx](#13-lab-7--ec2-userdata-and-nginx)
14. [Final Real-World Project](#14-final-real-world-project)
15. [Understanding the Final Architecture](#15-understanding-the-final-architecture)
16. [Deploying the Project](#16-deploying-the-project)
17. [Updating Infrastructure Safely](#17-updating-infrastructure-safely)
18. [Change Sets and Drift Detection](#18-change-sets-and-drift-detection)
19. [CloudFormation CLI Workflow](#19-cloudformation-cli-workflow)
20. [GitHub Repository Structure](#20-github-repository-structure)
21. [Git Commands](#21-git-commands)
22. [Common Errors](#22-common-errors)
23. [Production Improvements](#23-production-improvements)
24. [CloudFormation vs Terraform](#24-cloudformation-vs-terraform)
25. [What to Learn Next](#25-what-to-learn-next)

---

# 1. What is Infrastructure as Code?

Infrastructure as Code (IaC) means defining infrastructure using code or configuration files instead of creating everything manually through a cloud provider's graphical interface.

### Manual approach

You might manually:

```text
AWS Console
   ↓
Create VPC
   ↓
Create subnet
   ↓
Create route table
   ↓
Create Internet Gateway
   ↓
Create Security Group
   ↓
Create EC2
   ↓
Configure server
```

This works, but it becomes difficult to repeat consistently.

### IaC approach

You describe the desired infrastructure in a template:

```text
CloudFormation template
        ↓
CloudFormation
        ↓
AWS resources
```

For example:

```yaml
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
```

CloudFormation reads the template and creates the S3 bucket.

---

# 2. Why AWS CloudFormation?

AWS CloudFormation is AWS's native Infrastructure as Code service.

It lets you define AWS resources in YAML or JSON.

You can use CloudFormation to create and manage resources such as:

- VPCs
- Subnets
- Route tables
- Internet gateways
- EC2 instances
- Security groups
- IAM roles
- S3 buckets
- RDS databases
- Load balancers
- Auto Scaling groups
- Lambda functions
- CloudWatch resources

### Main benefits

**Repeatability**

The same template can create the same architecture again.

**Version control**

Templates can be stored in Git.

**Automation**

Infrastructure can be deployed through the AWS CLI and CI/CD.

**Consistency**

You reduce manual configuration mistakes.

**Dependency management**

CloudFormation understands relationships between resources.

**Change management**

You can review changes before applying them using Change Sets.

---

# 3. IaC Concepts You Need to Know

Before writing large templates, understand these terms.

## Template

The YAML or JSON file describing your infrastructure.

Example:

```text
network.yaml
```

## Stack

A CloudFormation deployment created from a template.

```text
network.yaml
     ↓
CloudFormation Stack
     ↓
AWS resources
```

## Resource

An AWS object managed by CloudFormation.

Example:

```yaml
MyVPC:
  Type: AWS::EC2::VPC
```

## Parameter

An input supplied when deploying a stack.

Example:

```yaml
Parameters:
  Environment:
    Type: String
    Default: dev
```

## Output

Useful information returned by a stack.

Example:

```yaml
Outputs:
  VpcId:
    Value: !Ref MyVPC
```

## Intrinsic Function

A CloudFormation function used to reference or construct values.

Common examples:

```text
!Ref
!Sub
!GetAtt
!Join
!Select
!GetAZs
!ImportValue
```

## Stack Update

When you modify the template and update the existing stack.

## Change Set

A preview of what CloudFormation plans to change.

## Drift

A difference between what CloudFormation expects and what actually exists in AWS.

---

# 4. Prerequisites

You should have:

- An AWS account
- Basic knowledge of EC2
- Basic knowledge of VPCs
- Basic Linux commands
- Basic YAML
- Git and GitHub
- AWS CLI installed and configured

You should understand concepts such as:

```text
EC2
VPC
Subnet
Security Group
Internet Gateway
Route Table
AMI
```

You do not need to know everything before starting. This guide teaches the CloudFormation side as you build.

---

# 5. AWS Cost and Security Notes

## Cost

CloudFormation itself does not generally charge you simply for having a template or stack. The AWS resources created by the stack can incur charges.

For learning labs, remove resources when finished.

For example:

```bash
aws cloudformation delete-stack \
  --stack-name my-stack \
  --region YOUR_REGION
```

Always verify in the AWS Billing console that no unwanted paid resources remain.

## Security

Do not commit:

```text
AWS access keys
Secret keys
Passwords
Private keys
.env files containing secrets
```

Use:

- IAM roles
- AWS Secrets Manager
- Systems Manager Parameter Store
- GitHub Actions OIDC for CI/CD
- Least-privilege IAM policies

Never put an AWS secret directly in a CloudFormation template.

---

# 6. CloudFormation Template Anatomy

A CloudFormation template can contain several sections:

```yaml
AWSTemplateFormatVersion: '2010-09-09'

Description: My CloudFormation template

Parameters:
  ...

Mappings:
  ...

Conditions:
  ...

Resources:
  ...

Outputs:
  ...
```

The most important sections for beginners are:

```text
Parameters
Resources
Outputs
```

---

## 6.1 Resources

```yaml
Resources:

  MyBucket:
    Type: AWS::S3::Bucket
```

`MyBucket` is the logical ID.

`AWS::S3::Bucket` is the resource type.

Think:

```text
Logical ID
    ↓
MyBucket
    ↓
Resource Type
    ↓
AWS::S3::Bucket
```

---

## 6.2 Properties

```yaml
MyBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: my-example-bucket
```

`Type` tells CloudFormation what to create.

`Properties` configure the resource.

---

# 7. Lab 1 — Create an S3 Bucket

Create:

```text
lab-01-s3.yaml
```

```yaml
AWSTemplateFormatVersion: '2010-09-09'

Description: Create a simple S3 bucket

Resources:

  MyBucket:
    Type: AWS::S3::Bucket
```

Deploy through the AWS Console or CLI.

Using the CLI:

```bash
aws cloudformation deploy \
  --template-file lab-01-s3.yaml \
  --stack-name lab-01-s3 \
  --region YOUR_REGION
```

Check the stack:

```bash
aws cloudformation describe-stacks \
  --stack-name lab-01-s3 \
  --region YOUR_REGION
```

Delete it when finished:

```bash
aws cloudformation delete-stack \
  --stack-name lab-01-s3 \
  --region YOUR_REGION
```

---

# 8. Lab 2 — Parameters

Hardcoded values make templates less reusable.

Instead of:

```yaml
BucketName: my-fixed-name
```

use a parameter.

```yaml
AWSTemplateFormatVersion: '2010-09-09'

Parameters:

  BucketName:
    Type: String
    Description: Enter a globally unique S3 bucket name

Resources:

  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketName
```

Here:

```yaml
!Ref BucketName
```

means:

> Get the value supplied for the `BucketName` parameter.

---

## Allowed values

You can restrict parameters:

```yaml
Parameters:

  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod
```

Now the user can select only:

```text
dev
staging
prod
```

---

## Numeric parameters

Example:

```yaml
Parameters:

  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
```

This becomes useful when deploying EC2.

---

# 9. Lab 3 — Outputs

Outputs expose useful values after deployment.

```yaml
Outputs:

  BucketName:
    Description: S3 bucket name
    Value: !Ref MyBucket
```

After deployment:

```text
CloudFormation
     ↓
Outputs
     ↓
BucketName
     ↓
actual bucket value
```

Outputs become especially useful with:

- VPC IDs
- Subnet IDs
- EC2 instance IDs
- Load balancer DNS names
- Security group IDs

---

# 10. Lab 4 — Intrinsic Functions

Intrinsic functions are one of the most important CloudFormation concepts.

---

## 10.1 `!Ref`

Get the value of a parameter or resource reference.

```yaml
InstanceType: !Ref InstanceType
```

Example:

```yaml
Parameters:
  Environment:
    Type: String
    Default: dev

Outputs:
  EnvironmentOutput:
    Value: !Ref Environment
```

---

## 10.2 `!Sub`

Build strings using variables.

```yaml
Value: !Sub "Environment: ${Environment}"
```

If:

```text
Environment = dev
```

the result is:

```text
Environment: dev
```

Another example:

```yaml
Value: !Sub "http://${MyServer.PublicIp}"
```

This is useful for URLs and names.

---

## 10.3 `!GetAtt`

Get a specific resource attribute.

Example:

```yaml
Value: !GetAtt MySecurityGroup.GroupId
```

Think:

```text
Resource
   ↓
MySecurityGroup
   ↓
Attribute
   ↓
GroupId
```

---

## 10.4 `!Join`

Combine strings.

```yaml
Value: !Join
  - "-"
  - - cloud
    - engineering
    - aws
```

Result:

```text
cloud-engineering-aws
```

---

## 10.5 `!Select` and `!GetAZs`

A common networking pattern:

```yaml
AvailabilityZone: !Select
  - 0
  - !GetAZs ''
```

This selects the first Availability Zone returned for the current region.

---

# 11. Lab 5 — Build a VPC

Now we move to real infrastructure.

Architecture:

```text
Internet
   |
Internet Gateway
   |
VPC: 10.0.0.0/16
   |
Public Subnet: 10.0.1.0/24
   |
Route Table
   |
0.0.0.0/0 -> Internet Gateway
```

Create:

```text
lab-05-vpc.yaml
```

```yaml
AWSTemplateFormatVersion: '2010-09-09'

Description: Basic VPC with a public subnet and internet access

Resources:

  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: CloudFormation-VPC

  MyInternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: CloudFormation-IGW

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref MyVPC
      InternetGatewayId: !Ref MyInternetGateway

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select
        - 0
        - !GetAZs ''
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: Public-Subnet

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MyVPC
      Tags:
        - Key: Name
          Value: Public-Route-Table

  DefaultRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref MyInternetGateway

  PublicRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet
      RouteTableId: !Ref PublicRouteTable

Outputs:

  VpcId:
    Description: VPC ID
    Value: !Ref MyVPC

  PublicSubnetId:
    Description: Public subnet ID
    Value: !Ref PublicSubnet
```

---

## Understand the network

```text
                       Internet
                          |
                          |
                  Internet Gateway
                          |
                    +-----------+
                    |    VPC    |
                    |10.0.0.0/16|
                    +-----------+
                          |
                    Public Subnet
                    10.0.1.0/24
                          |
                     EC2 later
```

The important relationships are:

```text
VPC
 |
 +-- Internet Gateway
 |
 +-- Subnet
 |
 +-- Route Table
       |
       +-- 0.0.0.0/0 -> Internet Gateway
```

---

# 12. Lab 6 — Deploy EC2 into Your VPC

Now we'll put compute inside the network.

## Security Group

A security group acts as a virtual firewall for the EC2 instance.

Example:

```yaml
MySecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Allow HTTP
    VpcId: !Ref MyVPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 80
        ToPort: 80
        CidrIp: 0.0.0.0/0
```

Notice:

```yaml
VpcId: !Ref MyVPC
```

This attaches the security group to our custom VPC.

---

## EC2

An EC2 resource needs an AMI and instance type.

```yaml
MyServer:
  Type: AWS::EC2::Instance
  Properties:
    InstanceType: t3.micro
    ImageId: YOUR_REGION_AMI_ID
    SubnetId: !Ref PublicSubnet
    SecurityGroupIds:
      - !GetAtt MySecurityGroup.GroupId
```

### Important

AMI IDs are region-specific.

Do not copy an AMI ID from a random tutorial without checking that it exists in your AWS region.

---

# 13. Lab 7 — EC2 UserData and Nginx

UserData is a startup script executed when an EC2 instance launches.

Example:

```yaml
UserData:
  Fn::Base64: |
    #!/bin/bash

    dnf update -y
    dnf install -y nginx

    cat > /usr/share/nginx/html/index.html <<'EOF'
    <html>
    <head>
      <title>CloudFormation Demo</title>
    </head>
    <body>
      <h1>Hello from CloudFormation!</h1>
      <p>This EC2 instance was configured automatically.</p>
    </body>
    </html>
    EOF

    systemctl enable nginx
    systemctl start nginx
```

The process becomes:

```text
CloudFormation
      |
      v
Create EC2
      |
      v
EC2 boots
      |
      v
UserData executes
      |
      +-- install Nginx
      |
      +-- create web page
      |
      +-- start Nginx
      |
      v
Website available
```

---

# 14. Final Real-World Project

Now combine the concepts.

## Project

Build a small public web server using CloudFormation.

Architecture:

```text
                         Internet
                            |
                            v
                    Internet Gateway
                            |
                            v
                  +-------------------+
                  |       VPC         |
                  |   10.0.0.0/16     |
                  |                   |
                  | Public Subnet     |
                  |   10.0.1.0/24     |
                  |        |           |
                  |        v           |
                  |      EC2           |
                  |        |           |
                  |      Nginx         |
                  +-------------------+
```

The stack will create:

- VPC
- Internet Gateway
- Public Subnet
- Route Table
- Internet Route
- Security Group
- EC2
- Nginx through UserData
- Outputs

---

# 15. Understanding the Final Architecture

Create:

```text
final-web-stack.yaml
```

Use:

```yaml
AWSTemplateFormatVersion: '2010-09-09'

Description: >
  CloudFormation example that creates a VPC, public subnet,
  internet gateway, route table, security group and EC2 web server.

Parameters:

  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t3.micro
      - t3.small
      - t3.medium
    Description: EC2 instance type

  LatestAmiId:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64

Resources:

  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-VPC"

  MyInternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-IGW"

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref MyVPC
      InternetGatewayId: !Ref MyInternetGateway

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select
        - 0
        - !GetAZs ''
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-PublicSubnet"

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MyVPC
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-PublicRouteTable"

  DefaultRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref MyInternetGateway

  PublicRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet
      RouteTableId: !Ref PublicRouteTable

  WebSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP traffic
      VpcId: !Ref MyVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-WebSG"

  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: !Ref LatestAmiId
      SubnetId: !Ref PublicSubnet
      SecurityGroupIds:
        - !GetAtt WebSecurityGroup.GroupId
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-WebServer"
      UserData:
        Fn::Base64: |
          #!/bin/bash

          dnf update -y
          dnf install -y nginx

          cat > /usr/share/nginx/html/index.html <<'EOF'
          <!DOCTYPE html>
          <html>
          <head>
            <title>AWS CloudFormation</title>
          </head>
          <body>
            <h1>Hello from AWS CloudFormation!</h1>
            <p>This EC2 instance was deployed and configured using Infrastructure as Code.</p>
          </body>
          </html>
          EOF

          systemctl enable nginx
          systemctl start nginx

Outputs:

  VpcId:
    Description: VPC ID
    Value: !Ref MyVPC

  PublicSubnetId:
    Description: Public subnet ID
    Value: !Ref PublicSubnet

  SecurityGroupId:
    Description: Web security group ID
    Value: !GetAtt WebSecurityGroup.GroupId

  InstanceId:
    Description: EC2 instance ID
    Value: !Ref WebServer

  PublicIp:
    Description: EC2 public IP address
    Value: !GetAtt WebServer.PublicIp

  WebsiteURL:
    Description: Website URL
    Value: !Sub "http://${WebServer.PublicIp}"
```

---

# 16. Deploying the Project

## Console

Go to:

```text
AWS Console
   ↓
CloudFormation
   ↓
Create stack
   ↓
Upload template
```

Upload:

```text
final-web-stack.yaml
```

Use a stack name such as:

```text
aws-iac-demo
```

Choose an instance type such as:

```text
t3.micro
```

Create the stack.

Wait for:

```text
CREATE_COMPLETE
```

Then open:

```text
CloudFormation
   ↓
aws-iac-demo
   ↓
Outputs
   ↓
WebsiteURL
```

Open the URL.

You should see:

```text
Hello from AWS CloudFormation!
```

---

# 17. Updating Infrastructure Safely

One of the most important IaC benefits is controlled updates.

Suppose your HTML page currently says:

```html
<h1>Hello from AWS CloudFormation!</h1>
```

Change it to:

```html
<h1>My AWS IaC Project</h1>
```

Then update the CloudFormation stack.

CloudFormation compares the desired template with the existing stack and applies the required changes.

Conceptually:

```text
Old Template
      |
      v
Existing Stack
      ^
      |
New Template
      |
      v
CloudFormation calculates changes
      |
      v
Updated infrastructure
```

---

# 18. Change Sets and Drift Detection

## Change Sets

A Change Set lets you preview changes before executing them.

Concept:

```text
Template change
      |
      v
Change Set
      |
      v
Review
      |
      v
Execute
```

Use Change Sets when infrastructure changes become important or risky.

---

## Drift Detection

Drift happens when someone changes infrastructure manually outside CloudFormation.

Example:

```text
CloudFormation says:

Port 80 allowed
```

Someone manually changes the security group:

```text
Port 80 removed
```

Now:

```text
Template state != Actual AWS state
```

That is drift.

CloudFormation can detect drift for supported resources.

IaC works best when you avoid making manual changes to resources managed by the stack.

---

# 19. CloudFormation CLI Workflow

Once you're comfortable with the Console, move to the CLI.

## Validate

```bash
aws cloudformation validate-template \
  --template-body file://final-web-stack.yaml \
  --region YOUR_REGION
```

## Deploy

```bash
aws cloudformation deploy \
  --template-file final-web-stack.yaml \
  --stack-name aws-iac-demo \
  --region YOUR_REGION
```

If parameters are required:

```bash
aws cloudformation deploy \
  --template-file final-web-stack.yaml \
  --stack-name aws-iac-demo \
  --parameter-overrides InstanceType=t3.micro \
  --region YOUR_REGION
```

## Describe stack

```bash
aws cloudformation describe-stacks \
  --stack-name aws-iac-demo \
  --region YOUR_REGION
```

## List resources

```bash
aws cloudformation list-stack-resources \
  --stack-name aws-iac-demo \
  --region YOUR_REGION
```

## View events

```bash
aws cloudformation describe-stack-events \
  --stack-name aws-iac-demo \
  --region YOUR_REGION
```

This command is particularly useful when a stack fails.

## Delete

```bash
aws cloudformation delete-stack \
  --stack-name aws-iac-demo \
  --region YOUR_REGION
```

---

# 20. GitHub Repository Structure

For a clean GitHub portfolio repository, use something like:

```text
aws-cloudformation-iac/
│
├── README.md
│
├── templates/
│   ├── lab-01-s3.yaml
│   ├── lab-02-parameters.yaml
│   ├── lab-03-outputs.yaml
│   ├── lab-04-intrinsic-functions.yaml
│   ├── lab-05-vpc.yaml
│   ├── lab-06-ec2.yaml
│   ├── lab-07-userdata.yaml
│   └── final-web-stack.yaml
│
├── docs/
│   └── cloudformation-guide.md
│
├── diagrams/
│   └── architecture.md
│
├── scripts/
│   ├── deploy.sh
│   └── destroy.sh
│
└── .gitignore
```

---

# 21. Git Commands

Initialize your repository:

```bash
git init
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Add AWS CloudFormation IaC labs"
```

Connect your GitHub repository:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

Push:

```bash
git branch -M main
git push -u origin main
```

---

# 22. Common Errors

## Error: Template validation failed

Check YAML indentation.

YAML is indentation-sensitive.

Wrong:

```yaml
Resources:
MyBucket:
  Type: AWS::S3::Bucket
```

Correct:

```yaml
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
```

---

## Error: AMI not found

AMI IDs are region-specific.

Check:

```text
AWS Region
+
AMI Region
```

They must match.

The final example avoids hardcoding an AMI by using the AWS Systems Manager public parameter for the latest Amazon Linux 2023 x86_64 AMI.

---

## Error: S3 bucket name already exists

S3 bucket names are globally unique.

Choose another name.

---

## Error: Security group not found

Make sure the security group belongs to the same VPC as the EC2 instance.

Example:

```yaml
VpcId: !Ref MyVPC
```

---

## Error: Stack rollback

CloudFormation may enter:

```text
ROLLBACK_IN_PROGRESS
```

or:

```text
ROLLBACK_COMPLETE
```

Check stack events:

```bash
aws cloudformation describe-stack-events \
  --stack-name YOUR_STACK_NAME \
  --region YOUR_REGION
```

Find the first resource that failed.

Don't just look at the final rollback message.

---

# 23. Production Improvements

The final project is intentionally simple for learning. Real production infrastructure should be improved.

## 23.1 Don't expose SSH to the world

Avoid:

```yaml
CidrIp: 0.0.0.0/0
```

for SSH port 22.

Prefer:

- AWS Systems Manager Session Manager
- restricted source IPs
- private subnets
- bastion alternatives only when justified

---

## 23.2 Use private subnets for application servers

A more realistic architecture:

```text
Internet
   |
   v
Application Load Balancer
   |
   +-------------------+
   |                   |
Public Subnets      Public Subnets
   |
   v
Private Subnets
   |
   +--------+--------+
   |                 |
 EC2/App            EC2/App
```

---

## 23.3 Add multiple Availability Zones

Instead of one subnet:

```text
VPC
 |
 +-- AZ-A
 |    |
 |  Subnet
 |
 +-- AZ-B
      |
    Subnet
```

This improves availability.

---

## 23.4 Add an Application Load Balancer

A more complete architecture:

```text
                    Internet
                       |
                       v
               Application Load
                  Balancer
                 /          \
                /            \
               v              v
           EC2 #1          EC2 #2
           Private         Private
           Subnet          Subnet
                \            /
                 \          /
                    App
```

---

## 23.5 Add Auto Scaling

Instead of manually creating two EC2 instances:

```text
ALB
 |
Target Group
 |
Auto Scaling Group
 |
+----+----+----+
|    |    |    |
EC2  EC2  EC2
```

CloudFormation can define all of this.

---

## 23.6 Add RDS

A typical three-tier architecture:

```text
Internet
   |
  ALB
   |
Application
   |
Private EC2
   |
Private Database
   |
RDS
```

---

## 23.7 Use IAM roles

Avoid embedding AWS credentials in EC2.

Use:

```text
EC2
 |
IAM Instance Role
 |
AWS services
```

This is safer and follows AWS's recommended credential model.

---

# 24. CloudFormation vs Terraform

CloudFormation and Terraform are both Infrastructure as Code tools.

## CloudFormation

```text
AWS
 ↓
CloudFormation
 ↓
AWS resources
```

Advantages:

- AWS-native
- Deep AWS integration
- CloudFormation Stack management
- IAM and AWS services integrate naturally
- No separate infrastructure provider needed

## Terraform

```text
Terraform
   |
   +-- AWS
   +-- Azure
   +-- Google Cloud
   +-- other providers
```

Advantages:

- Multi-cloud
- Large provider ecosystem
- HCL syntax
- Widely used across many cloud environments

### Learning order

For an AWS-focused cloud engineer:

```text
AWS basics
    ↓
CloudFormation
    ↓
Terraform
    ↓
CI/CD
```

Learning CloudFormation first helps you understand IaC concepts before moving to Terraform.

---

# 25. What to Learn Next

After completing this guide, your next path should be:

```text
CloudFormation Fundamentals
        ↓
VPC
        ↓
EC2
        ↓
IAM
        ↓
ALB
        ↓
Auto Scaling
        ↓
RDS
        ↓
Docker
        ↓
ECR
        ↓
ECS
        ↓
CI/CD
        ↓
Terraform
        ↓
Kubernetes
```

For your cloud engineering portfolio, build progressively larger projects.

## Project 1

```text
CloudFormation
     ↓
S3
```

## Project 2

```text
CloudFormation
     ↓
VPC
     ↓
EC2
     ↓
Nginx
```

## Project 3

```text
CloudFormation
       ↓
VPC
       ↓
ALB
       ↓
EC2
       ↓
Docker
```

## Project 4

```text
CloudFormation
       ↓
VPC
       ↓
ALB
       ↓
Auto Scaling
       ↓
EC2
       ↓
RDS
```

## Project 5 — Portfolio Project

```text
                         Internet
                            |
                            v
                     Application ALB
                       /         \
                      /           \
                     v             v
              Private EC2      Private EC2
                  Docker          Docker
                     \             /
                      \           /
                       v         v
                         RDS
                          |
                     Private subnet

                 Infrastructure:
                    CloudFormation
                         +
                      GitHub
                         +
                       CI/CD
```

This is the direction that turns basic CloudFormation knowledge into practical cloud engineering experience.

---

# Final Cheat Sheet

## Core sections

```text
Parameters → inputs
Resources  → infrastructure
Outputs    → useful results
```

## Core functions

```text
!Ref       → reference a value
!Sub       → substitute values into strings
!GetAtt    → get a resource attribute
!Join      → combine strings
!Select    → select an item
!GetAZs    → retrieve Availability Zones
!ImportValue → use an exported stack value
```

## Core workflow

```text
Write YAML
   ↓
Validate
   ↓
Deploy stack
   ↓
CloudFormation creates resources
   ↓
Check Outputs
   ↓
Test infrastructure
   ↓
Modify template
   ↓
Review changes
   ↓
Update stack
```

## Core IaC mindset

```text
Don't manually build everything.

Define desired infrastructure as code.

Version it with Git.

Review changes.

Deploy consistently.

Keep infrastructure reproducible.
```

---

# Portfolio Checklist

After completing this guide, you should be able to explain and demonstrate:

- [ ] What Infrastructure as Code means
- [ ] What CloudFormation is
- [ ] Template vs stack
- [ ] Resources
- [ ] Parameters
- [ ] Outputs
- [ ] `!Ref`
- [ ] `!Sub`
- [ ] `!GetAtt`
- [ ] `!Join`
- [ ] VPC creation
- [ ] Subnets
- [ ] Internet Gateway
- [ ] Route tables
- [ ] Security Groups
- [ ] EC2 deployment
- [ ] UserData
- [ ] Nginx bootstrapping
- [ ] CloudFormation updates
- [ ] Change Sets
- [ ] Drift detection
- [ ] AWS CLI deployment
- [ ] Git/GitHub workflow
- [ ] Basic production architecture

---

## Conclusion

CloudFormation is more than writing YAML.

The real skill is understanding the infrastructure architecture and expressing that architecture as code.

Start small:

```text
S3
 ↓
VPC
 ↓
EC2
 ↓
UserData
```

Then progress toward:

```text
VPC
 ↓
ALB
 ↓
Auto Scaling
 ↓
Docker
 ↓
RDS
 ↓
CI/CD
```

The goal is to reach the point where you can look at an AWS architecture diagram and translate it into reproducible infrastructure code.

That is the core of AWS Infrastructure as Code.
