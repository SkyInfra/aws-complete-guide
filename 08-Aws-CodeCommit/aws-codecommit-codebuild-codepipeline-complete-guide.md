# AWS CodeCommit, CodeBuild & CodePipeline --- Complete Guide

A beginner-friendly, practical guide to AWS CI/CD using **CodeCommit,
CodeBuild, and CodePipeline**.

## 1. CI/CD Basics

**CI/CD** means automating the process of integrating, building,
testing, and delivering software.

Basic flow:

``` text
Developer
   |
   | git push
   v
Source Repository
   |
   v
Build
   |
   v
Test
   |
   v
Deploy
```

### Continuous Integration

Developers frequently push changes to a shared repository. Automated
builds and tests check those changes.

### Continuous Delivery

Software is automatically built and validated so it is ready to release.

### Continuous Deployment

Successful changes can be automatically deployed to the target
environment.

------------------------------------------------------------------------

## 2. AWS Services

  Service            Main Job
  ------------------ -----------------------------------------
  **CodeCommit**     Store source code in a Git repository
  **CodeBuild**      Build and test source code
  **CodePipeline**   Orchestrate the complete CI/CD workflow

Easy memory trick:

``` text
CodeCommit   = STORE
CodeBuild    = BUILD + TEST
CodePipeline = ORCHESTRATE
```

------------------------------------------------------------------------

# 3. AWS CodeCommit

## What is CodeCommit?

AWS CodeCommit is a managed private Git repository service.

If GitHub stores Git repositories, CodeCommit can also store Git
repositories inside AWS.

Example:

``` text
my-app/
├── app.js
├── package.json
├── Dockerfile
├── buildspec.yml
└── README.md
```

## Main purpose

CodeCommit stores and versions your source code.

Typical commands:

``` bash
git add .
git commit -m "Add login API"
git push
```

The `git push` sends your local commit to CodeCommit.

### Important Git concepts

-   **Repository** --- complete project
-   **Commit** --- saved change
-   **Branch** --- separate line of development
-   **Push** --- send local commits to remote repository
-   **Pull** --- get remote changes

Example:

``` text
Your Mac
   |
   | git push
   v
CodeCommit
```

------------------------------------------------------------------------

# 4. AWS CodeBuild

## What is CodeBuild?

AWS CodeBuild is a managed build service.

It can:

-   Install dependencies
-   Compile applications
-   Run tests
-   Build applications
-   Build Docker images
-   Create build artifacts

Think of CodeBuild as the machine that performs your build instructions.

``` text
Source Code
    |
    v
CodeBuild
    |
    +-- Install
    +-- Build
    +-- Test
    +-- Package
```

## Real example

For a Node.js application:

``` bash
npm install
npm test
npm run build
```

If successful:

``` text
BUILD SUCCESS
```

If a test fails:

``` text
BUILD FAILED
```

------------------------------------------------------------------------

# 5. buildspec.yml

CodeBuild commonly uses a file called:

``` text
buildspec.yml
```

It contains the commands CodeBuild should execute.

Example:

``` yaml
version: 0.2

phases:
  install:
    commands:
      - npm install

  build:
    commands:
      - npm run build
      - npm test

artifacts:
  files:
    - '**/*'
```

Think of it as:

``` text
CodeBuild = Worker
buildspec.yml = Instructions for the Worker
```

------------------------------------------------------------------------

# 6. AWS CodePipeline

## What is CodePipeline?

AWS CodePipeline automates and coordinates stages in a software release
workflow.

Example:

``` text
CodeCommit
    |
    v
CodePipeline
    |
    v
CodeBuild
    |
    v
Deploy
```

CodePipeline is not the same thing as CodeBuild.

**CodeBuild executes build/test commands.**

**CodePipeline controls what happens and in what order.**

Typical stages:

``` text
SOURCE
   |
   v
BUILD
   |
   v
TEST
   |
   v
DEPLOY
```

------------------------------------------------------------------------

# 7. How They Work Together

The easiest architecture to remember:

``` text
                  Developer
                      |
                  git push
                      |
                      v
              +---------------+
              |  CodeCommit   |
              | Source Code   |
              +-------+-------+
                      |
                      v
              +---------------+
              | CodePipeline  |
              | Orchestrator  |
              +-------+-------+
                      |
                      v
              +---------------+
              |   CodeBuild   |
              | Build + Test  |
              +-------+-------+
                      |
                      v
                   Deploy
```

### CodeCommit asks:

> Where is the code?

### CodeBuild asks:

> Can I build and test the code?

### CodePipeline asks:

> What should happen next?

------------------------------------------------------------------------

# 8. Real-World Example

Imagine you work on an online store.

You change the login page and run:

``` bash
git add .
git commit -m "Update login page"
git push
```

### Step 1 --- CodeCommit

The new commit arrives:

``` text
Developer
    |
    | git push
    v
CodeCommit
```

### Step 2 --- CodePipeline

The pipeline detects the source change and starts:

``` text
CodeCommit
    |
    v
CodePipeline
```

### Step 3 --- CodeBuild

CodePipeline invokes CodeBuild:

``` text
CodeBuild
    |
    +-- npm install
    +-- npm test
    +-- npm run build
```

### Step 4 --- Deploy

If the build succeeds, the pipeline can continue to a deployment target
such as:

-   EC2
-   ECS
-   S3
-   Lambda
-   CloudFormation

Complete flow:

``` text
Developer
    |
    | git push
    v
CodeCommit
    |
    v
CodePipeline
    |
    v
CodeBuild
    |
    +-- Build
    +-- Test
    |
    v
Deploy
```

------------------------------------------------------------------------

# 9. Hands-on Project Architecture

We will create a simple web application:

``` text
aws-cicd-demo/
├── index.html
├── buildspec.yml
└── README.md
```

Workflow:

``` text
Mac
 |
 | git push
 v
CodeCommit
 |
 v
CodePipeline
 |
 v
CodeBuild
 |
 +-- Build
 +-- Test
 |
 v
Artifact
 |
 v
Deployment
```

------------------------------------------------------------------------

# 10. Prerequisites

You need:

-   AWS account
-   IAM identity with appropriate permissions
-   Git
-   AWS CLI
-   Basic Git knowledge
-   Basic AWS IAM knowledge

Check Git:

``` bash
git --version
```

Check AWS CLI:

``` bash
aws --version
```

Check AWS identity:

``` bash
aws sts get-caller-identity
```

**Never commit AWS access keys or secret keys to Git.**

------------------------------------------------------------------------

# 11. Hands-on --- Create CodeCommit Repository

Open:

``` text
AWS Console → CodeCommit → Repositories
```

Create:

``` text
aws-cicd-demo
```

Description:

``` text
AWS CI/CD hands-on project
```

Choose your desired AWS Region.

Result:

``` text
CodeCommit
   |
   +-- aws-cicd-demo
```

------------------------------------------------------------------------

# 12. Clone the Repository

Create a workspace:

``` bash
mkdir -p ~/Documents/aws-projects
cd ~/Documents/aws-projects
```

Use the clone URL shown by the CodeCommit console:

``` bash
git clone <YOUR_CODECOMMIT_CLONE_URL>
```

Then:

``` bash
cd aws-cicd-demo
```

Check:

``` bash
git status
```

------------------------------------------------------------------------

# 13. Create the Application

Create:

``` bash
touch index.html
```

Example:

``` html
<!DOCTYPE html>
<html>
<head>
    <title>AWS CI/CD Demo</title>
</head>
<body>
    <h1>My AWS CI/CD Project</h1>
    <p>Deployed through an automated CI/CD workflow.</p>
</body>
</html>
```

------------------------------------------------------------------------

# 14. Create buildspec.yml

Create:

``` bash
touch buildspec.yml
```

Add:

``` yaml
version: 0.2

phases:
  build:
    commands:
      - echo "Build started"
      - echo "Checking application files"
      - test -f index.html
      - echo "Build completed successfully"

artifacts:
  files:
    - index.html
```

The command:

``` bash
test -f index.html
```

checks that the file exists.

If it exists:

``` text
Build SUCCESS
```

If it does not:

``` text
Build FAILED
```

------------------------------------------------------------------------

# 15. Commit and Push

Check:

``` bash
git status
```

Add:

``` bash
git add .
```

Commit:

``` bash
git commit -m "Add CI/CD demo application"
```

Push:

``` bash
git push
```

Now:

``` text
Local Machine
     |
     | git push
     v
CodeCommit
```

------------------------------------------------------------------------

# 16. Create CodeBuild Project

Open:

``` text
AWS Console
→ CodeBuild
→ Build projects
→ Create build project
```

Project name:

``` text
aws-cicd-demo-build
```

For the source, select CodeCommit and:

``` text
Repository: aws-cicd-demo
```

Select the correct branch.

Use a managed Linux build environment.

Configure CodeBuild to use the `buildspec.yml` file from the source
repository.

When CodeBuild runs:

``` text
Download source
      |
      v
Read buildspec.yml
      |
      v
Run commands
      |
      v
Create artifacts
```

------------------------------------------------------------------------

# 17. Test CodeBuild

Start a build from the CodeBuild console.

You should see commands similar to:

``` text
Build started
Checking application files
Build completed successfully
```

Open the build logs if the build fails.

The logs are one of the most important tools for troubleshooting CI/CD.

------------------------------------------------------------------------

# 18. Create CodePipeline

Open:

``` text
AWS Console
→ CodePipeline
→ Create pipeline
```

Pipeline name:

``` text
aws-cicd-demo-pipeline
```

Create or select an appropriate service role.

## Source Stage

Choose:

``` text
Source provider: AWS CodeCommit
Repository: aws-cicd-demo
Branch: main
```

Flow:

``` text
CodeCommit
    |
    v
Source Stage
```

## Build Stage

Add:

``` text
AWS CodeBuild
```

Select:

``` text
aws-cicd-demo-build
```

Now:

``` text
CodeCommit
    |
    v
CodePipeline
    |
    v
CodeBuild
```

## Deploy Stage

The deployment target depends on your application.

Possible targets:

``` text
S3
EC2
ECS
Lambda
CloudFormation
```

For a first lab, you can begin with Source + Build and then add a
deployment stage.

------------------------------------------------------------------------

# 19. Test Automatic CI/CD

Change:

``` html
<h1>My AWS CI/CD Project</h1>
```

to:

``` html
<h1>My First AWS CI/CD Pipeline</h1>
```

Then:

``` bash
git add .
git commit -m "Update website title"
git push
```

The expected flow is:

``` text
git push
   |
   v
CodeCommit
   |
   v
CodePipeline
   |
   v
CodeBuild
   |
   v
Build/Test
   |
   v
Deploy
```

This is the core CI/CD experience.

------------------------------------------------------------------------

# 20. More Realistic buildspec.yml

For Node.js:

``` yaml
version: 0.2

phases:
  install:
    commands:
      - echo "Installing dependencies"
      - npm install

  pre_build:
    commands:
      - echo "Running tests"
      - npm test

  build:
    commands:
      - echo "Building application"
      - npm run build

  post_build:
    commands:
      - echo "Build completed"

artifacts:
  files:
    - '**/*'
```

For Python:

``` yaml
version: 0.2

phases:
  install:
    commands:
      - pip install -r requirements.txt

  build:
    commands:
      - pytest
```

For Java:

``` yaml
version: 0.2

phases:
  build:
    commands:
      - mvn test
      - mvn package
```

For Docker:

``` yaml
version: 0.2

phases:
  build:
    commands:
      - docker build -t my-app .
```

The exact commands depend on your project.

------------------------------------------------------------------------

# 21. Artifacts

An artifact is output produced by a stage and passed to another stage.

Example:

``` text
CodeCommit
    |
    | Source
    v
CodeBuild
    |
    | Build Artifact
    v
CodePipeline
    |
    v
Deployment
```

Example output:

``` text
build/
├── index.html
├── app.js
└── styles.css
```

The `artifacts` section in `buildspec.yml` tells CodeBuild what output
files should be collected.

------------------------------------------------------------------------

# 22. Environment Variables

CodeBuild can use environment variables.

Example:

``` text
ENVIRONMENT=dev
APP_NAME=my-app
```

Then:

``` yaml
phases:
  build:
    commands:
      - echo "Environment is $ENVIRONMENT"
```

Do not put passwords or long-lived credentials directly into source
files.

For secrets, use appropriate AWS services such as:

-   AWS Secrets Manager
-   AWS Systems Manager Parameter Store

and control access with IAM.

------------------------------------------------------------------------

# 23. Branches and CI/CD

A team can use branches:

``` text
main
 |
 +-- dev
 |
 +-- feature/login
 |
 +-- feature/payment
```

Example workflow:

``` text
feature/login
      |
      v
CodeCommit
      |
      v
Pull Request
      |
      v
main
```

You can design different pipelines/environments for development and
production.

Example:

``` text
dev
 |
 v
Build + Test
 |
 v
Development Environment
```

and:

``` text
main
 |
 v
Build + Test
 |
 v
Approval
 |
 v
Production
```

------------------------------------------------------------------------

# 24. Production-Style CI/CD

A more realistic workflow:

``` text
Developer
    |
    v
Feature Branch
    |
    v
Pull Request
    |
    v
main
    |
    v
CodePipeline
    |
    v
CodeBuild
    |
    +-- Unit Tests
    +-- Build
    +-- Security Checks
    |
    v
Approval
    |
    v
Production
```

Possible environments:

``` text
Development
     |
     v
Staging
     |
     v
Production
```

------------------------------------------------------------------------

# 25. CodeCommit vs GitHub

  Feature                  CodeCommit   GitHub
  ------------------------ ------------ --------------------------------
  Git repositories         Yes          Yes
  Branches                 Yes          Yes
  Commits                  Yes          Yes
  Pull requests            Yes          Yes
  AWS-native integration   Strong       Available through integrations
  Open-source ecosystem    Smaller      Very large

Learning CodeCommit is useful for understanding AWS-native workflows,
while GitHub remains an important general-purpose Git platform.

------------------------------------------------------------------------

# 26. CodeBuild vs CodePipeline

This distinction is extremely important.

### CodeBuild

Actually executes commands:

``` text
CodeBuild
   |
   +-- npm install
   +-- npm test
   +-- npm run build
```

### CodePipeline

Controls the workflow:

``` text
CodePipeline
   |
   +-- Source
   +-- Build
   +-- Approval
   +-- Deploy
```

Easy memory trick:

``` text
CodeBuild = Worker
CodePipeline = Manager
```

------------------------------------------------------------------------

# 27. Common Errors

## AccessDenied

Possible causes:

-   IAM permissions
-   CodeBuild service role
-   CodePipeline service role
-   CodeCommit permissions

Check IAM policies and service roles.

## buildspec.yml not found

Make sure:

``` text
repository/
└── buildspec.yml
```

and that it has been committed:

``` bash
git add buildspec.yml
git commit -m "Add buildspec"
git push
```

## Build failed

Open CodeBuild logs.

Find the command that failed, for example:

``` text
npm test
```

## Pipeline does not start

Check:

-   Repository
-   Branch
-   Source configuration
-   Pipeline status
-   IAM permissions
-   AWS Region
-   Whether a new commit was pushed

## Artifact missing

Check the `artifacts` section:

``` yaml
artifacts:
  files:
    - '**/*'
```

Make sure the expected files are actually produced.

------------------------------------------------------------------------

# 28. Security Best Practices

## Never commit credentials

Do not put this in Git:

``` text
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

## Use IAM roles

Let AWS services assume IAM roles instead of hard-coding credentials.

## Least privilege

Give each service only the permissions it needs.

## Protect production

Use controlled branches, reviews, and approvals for production
deployment.

## Store secrets securely

Use Secrets Manager or Parameter Store when appropriate.

## Monitor

Use AWS logging and monitoring tools to investigate failures and
unexpected activity.

------------------------------------------------------------------------

# 29. Useful AWS CLI Commands

Check your identity:

``` bash
aws sts get-caller-identity
```

List CodeCommit repositories:

``` bash
aws codecommit list-repositories
```

Get repository information:

``` bash
aws codecommit get-repository   --repository-name aws-cicd-demo
```

List CodeBuild projects:

``` bash
aws codebuild list-projects
```

Start a CodeBuild build:

``` bash
aws codebuild start-build   --project-name aws-cicd-demo-build
```

List pipelines:

``` bash
aws codepipeline list-pipelines
```

Get pipeline state:

``` bash
aws codepipeline get-pipeline-state   --name aws-cicd-demo-pipeline
```

------------------------------------------------------------------------

# 30. Portfolio Repository Structure

A strong portfolio project could look like:

``` text
aws-cicd-project/
│
├── README.md
│
├── app/
│   ├── index.html
│   └── ...
│
├── buildspec.yml
│
├── cloudformation/
│   ├── pipeline.yaml
│   ├── codebuild.yaml
│   └── infrastructure.yaml
│
├── docs/
│   ├── architecture.md
│   └── troubleshooting.md
│
└── diagrams/
    └── architecture.png
```

Your README should explain:

-   Project objective
-   Architecture
-   AWS services used
-   CI/CD flow
-   How to deploy
-   How to test
-   Problems encountered
-   Lessons learned

------------------------------------------------------------------------

# 31. Connecting CI/CD With CloudFormation

This is especially useful for a Cloud Engineer.

CloudFormation can define infrastructure such as:

``` text
CloudFormation
    |
    +-- VPC
    +-- Subnets
    +-- IAM
    +-- ECR
    +-- ECS
    +-- ALB
    +-- CodeBuild
    +-- CodePipeline
```

Then your complete workflow can become:

``` text
Git
 |
 v
CodeCommit
 |
 v
CodePipeline
 |
 +----------------+
 |                |
 v                v
CodeBuild     CloudFormation
 |                |
 v                v
Application     AWS Infrastructure
 |
 v
ECS / EC2 / S3
```

This combines your **IaC learning** with your **CI/CD learning**.

------------------------------------------------------------------------

# 32. Recommended Next Project

After this basic project, build:

``` text
Developer
    |
    | git push
    v
CodeCommit
    |
    v
CodePipeline
    |
    v
CodeBuild
    |
    | Docker build
    v
Amazon ECR
    |
    v
ECS
    |
    v
Application Load Balancer
    |
    v
Users
```

Then use CloudFormation to create the infrastructure.

This gives you an end-to-end AWS Cloud/DevOps portfolio project.

------------------------------------------------------------------------

# 33. Final Cheat Sheet

## CodeCommit

``` text
Purpose:
Store source code

Technology:
Git

Example:
git push
```

**Remember: CodeCommit = Source Repository**

## CodeBuild

``` text
Purpose:
Build + Test

Configuration:
buildspec.yml

Examples:
npm install
npm test
npm run build
```

**Remember: CodeBuild = Build/Test Worker**

## CodePipeline

``` text
Purpose:
Automate the release workflow

Typical stages:
Source → Build → Test → Deploy
```

**Remember: CodePipeline = Workflow Orchestrator**

------------------------------------------------------------------------

# Final Architecture

``` text
                         Developer
                             |
                             | git push
                             v
                      +-------------+
                      | CodeCommit  |
                      |    SOURCE   |
                      +------+------+
                             |
                             v
                      +-------------+
                      | CodePipeline|
                      | ORCHESTRATE |
                      +------+------+
                             |
                             v
                      +-------------+
                      |  CodeBuild  |
                      | BUILD/TEST  |
                      +------+------+
                             |
                             v
                          Artifact
                             |
                             v
                          Deploy
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
             EC2            ECS            S3
```

## The three words to remember

``` text
CodeCommit   → STORE
CodeBuild    → BUILD + TEST
CodePipeline → AUTOMATE
```

## Complete CI/CD idea

``` text
Write Code
    ↓
Git Commit
    ↓
Git Push
    ↓
CodeCommit
    ↓
CodePipeline
    ↓
CodeBuild
    ↓
Test
    ↓
Artifact
    ↓
Deploy
    ↓
AWS
```

------------------------------------------------------------------------

# Hands-on Checklist

-   [ ] Create CodeCommit repository
-   [ ] Clone repository
-   [ ] Create application
-   [ ] Create `buildspec.yml`
-   [ ] Commit code
-   [ ] Push to CodeCommit
-   [ ] Create CodeBuild project
-   [ ] Run first build
-   [ ] Read CodeBuild logs
-   [ ] Create CodePipeline
-   [ ] Connect CodeCommit source
-   [ ] Connect CodeBuild
-   [ ] Add deployment stage
-   [ ] Push a new change
-   [ ] Watch the pipeline execute automatically
-   [ ] Troubleshoot a failed build
-   [ ] Connect the pipeline to a real AWS deployment
-   [ ] Later, define the CI/CD infrastructure using CloudFormation

------------------------------------------------------------------------

# Key Takeaway

Do not focus only on memorizing AWS console buttons.

Understand the flow:

``` text
                SOURCE
                   ↓
              CodeCommit
                   ↓
              CodePipeline
                   ↓
                BUILD
                   ↓
              CodeBuild
                   ↓
                TEST
                   ↓
              ARTIFACT
                   ↓
                DEPLOY
```

Once this flow is clear, the hands-on implementation becomes much
easier.
