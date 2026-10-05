# Terraform with AWS

Hands-on Terraform project for learning Infrastructure as Code (IaC) with Amazon Web Services (AWS).

## What I Learned

* Terraform fundamentals
* Infrastructure as Code (IaC)
* Terraform providers
* AWS provider configuration
* Terraform resources
* Terraform variables
* Terraform outputs
* Terraform workflow
* Terraform plan and apply
* Terraform state basics
* AWS region configuration and troubleshooting

## Project Structure

```text
terraform-aws-project/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── .gitignore
└── README.md
```

## Current AWS Resource

The project is currently configured to manage an Amazon S3 bucket using Terraform.

```text
AWS Region: us-east-2
Resource: Amazon S3 Bucket
```

## Terraform Workflow

```text
terraform init
        ↓
terraform fmt
        ↓
terraform validate
        ↓
terraform plan
        ↓
terraform apply
```

## Key Concept

Instead of manually creating AWS resources through the AWS Console, Terraform allows infrastructure to be defined as code and managed consistently.

## Current Progress

S3 resource configuration, variables, outputs, provider configuration, and Terraform workflow have been completed.

The S3 creation is currently being troubleshooted due to an AWS-side conflicting operation.

## Next Steps

* Complete S3 resource deployment
* Learn Terraform state
* Create EC2 infrastructure
* Learn VPC resources
* Add security groups and networking
* Build a complete AWS infrastructure project
* Learn Terraform modules
* Document the project with screenshots
* Connect Terraform with CI/CD practices

---

**Learning Focus:** Cloud Engineering • DevOps • Infrastructure as Code • AWS • Terraform

