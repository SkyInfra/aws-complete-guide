# Amazon CloudWatch — Complete Hands-On Guide

> A practical AWS CloudWatch monitoring lab using Amazon EC2, CPU utilization, CloudWatch Metrics, and a CPU alarm.

![AWS](https://img.shields.io/badge/AWS-CloudWatch-orange)
![EC2](https://img.shields.io/badge/AWS-EC2-blue)
![Monitoring](https://img.shields.io/badge/Focus-Monitoring-green)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-purple)

---

## Table of Contents

1. [What is Amazon CloudWatch?](#1-what-is-amazon-cloudwatch)
2. [Why CloudWatch is Important in Cloud & DevOps](#2-why-cloudwatch-is-important-in-cloud--devops)
3. [CloudWatch Core Architecture](#3-cloudwatch-core-architecture)
4. [CloudWatch Metrics](#4-cloudwatch-metrics)
5. [Namespaces](#5-namespaces)
6. [Metrics and Dimensions](#6-metrics-and-dimensions)
7. [Statistics](#7-statistics)
8. [Periods and Resolution](#8-periods-and-resolution)
9. [EC2 Metrics](#9-ec2-metrics)
10. [Basic vs Detailed Monitoring](#10-basic-vs-detailed-monitoring)
11. [CloudWatch Agent](#11-cloudwatch-agent)
12. [CloudWatch Logs](#12-cloudwatch-logs)
13. [Log Groups and Log Streams](#13-log-groups-and-log-streams)
14. [CloudWatch Logs Insights](#14-cloudwatch-logs-insights)
15. [Metric Filters](#15-metric-filters)
16. [CloudWatch Alarms](#16-cloudwatch-alarms)
17. [Alarm States](#17-alarm-states)
18. [SNS Notifications](#18-sns-notifications)
19. [CloudWatch Dashboards](#19-cloudwatch-dashboards)
20. [EventBridge and Automation](#20-eventbridge-and-automation)
21. [Custom Metrics](#21-custom-metrics)
22. [CloudWatch vs CloudTrail](#22-cloudwatch-vs-cloudtrail)
23. [Hands-On Project](#23-hands-on-project)
24. [CPU Spike Simulation](#24-cpu-spike-simulation)
25. [Creating a CPU Alarm](#25-creating-a-cpu-alarm)
26. [Screenshots for the Portfolio](#26-screenshots-for-the-portfolio)
27. [Troubleshooting](#27-troubleshooting)
28. [DevOps Monitoring Workflow](#28-devops-monitoring-workflow)
29. [Best Practices](#29-best-practices)
30. [Cost and Cleanup](#30-cost-and-cleanup)
31. [Key Takeaways](#31-key-takeaways)
32. [Further Learning](#32-further-learning)

---

# 1. What is Amazon CloudWatch?

**Amazon CloudWatch** is AWS's monitoring and observability service.

It collects and provides access to telemetry such as:

- Metrics
- Logs
- Alarms
- Dashboards
- Events
- Application and infrastructure monitoring data

The simplest way to understand CloudWatch is:

> **CloudWatch helps you understand what is happening inside your AWS environment.**

For example, suppose an application is running on an EC2 instance.

Without monitoring:

```text
EC2 Server
   |
   |  Something becomes slow
   |
   └── We do not know why
```

With CloudWatch:

```text
EC2 Server
   |
   ├── CPUUtilization
   ├── Network traffic
   ├── Disk activity
   ├── Application logs
   └── Status checks
            |
            v
       CloudWatch
            |
       ┌────┴────┐
       v         v
    Dashboard   Alarm
                  |
                  v
                 SNS
                  |
                  v
                Email
```

CloudWatch is therefore a major part of AWS monitoring and observability.

---

# 2. Why CloudWatch is Important in Cloud & DevOps

Cloud/DevOps engineers need to answer questions such as:

- Is the server healthy?
- Is CPU usage too high?
- Is memory being exhausted?
- Is disk space running out?
- Is the application generating errors?
- When did the problem begin?
- How frequently is the problem occurring?
- Should an engineer be notified?
- Can the problem trigger an automated action?

CloudWatch provides building blocks for answering these questions.

A typical production monitoring flow is:

```text
Application
     |
     v
Infrastructure
     |
     +------------------+
     |                  |
     v                  v
   Metrics             Logs
     |                  |
     +--------+---------+
              |
              v
         CloudWatch
              |
      +-------+-------+
      |               |
      v               v
   Dashboard        Alarm
                       |
                       v
                      SNS
                       |
                       v
                    Engineer
```

---

# 3. CloudWatch Core Architecture

The most important CloudWatch components are:

| Component | Purpose |
|---|---|
| Metrics | Numerical measurements over time |
| Namespace | Logical grouping of metrics |
| Dimensions | Identify/filter the resource or context |
| Statistics | Explain how metric data is aggregated |
| Period | Time interval represented by a datapoint |
| Logs | Detailed event records |
| Log Group | Collection/category of logs |
| Log Stream | Sequence of log events from one source |
| Alarm | Rule that evaluates a metric |
| Dashboard | Visual monitoring screen |
| CloudWatch Agent | Collects additional host metrics and logs |
| Logs Insights | Query and analyze logs |
| Metric Filter | Convert matching log events into metrics |
| SNS | Send notifications |
| EventBridge | Respond to events and automate actions |

---

# 4. CloudWatch Metrics

A **metric** is a numerical measurement collected over time.

Examples:

```text
CPUUtilization = 72%
NetworkIn = 150000 bytes
NetworkOut = 80000 bytes
DiskReadOps = 120
StatusCheckFailed = 0
```

A metric normally answers:

> **What are we measuring?**

For EC2:

```text
CPUUtilization
```

means:

> How much CPU is being used by the EC2 instance.

### Example

Imagine an EC2 server:

```text
10:00 → 5% CPU
10:05 → 8% CPU
10:10 → 12% CPU
10:15 → 76% CPU
10:20 → 82% CPU
```

CloudWatch can graph these values.

This allows an engineer to identify changes and trends instead of checking the server manually.

---

# 5. Namespaces

A **namespace** groups related metrics.

For EC2, the namespace is:

```text
AWS/EC2
```

Examples of AWS namespaces include:

```text
AWS/EC2
AWS/Lambda
AWS/RDS
AWS/S3
AWS/ECS
AWS/ELB
AWS/ApiGateway
```

Think of a namespace like a folder:

```text
CloudWatch
│
├── AWS/EC2
│     ├── CPUUtilization
│     ├── NetworkIn
│     └── NetworkOut
│
├── AWS/Lambda
│     ├── Invocations
│     └── Errors
│
└── AWS/RDS
      ├── CPUUtilization
      └── DatabaseConnections
```

### In this project

The EC2 CPU metric belongs to:

```text
Namespace: AWS/EC2
Metric:    CPUUtilization
```

---

# 6. Metrics and Dimensions

A **dimension** identifies or filters the context of a metric.

For an EC2 metric, an important dimension is:

```text
InstanceId
```

Example:

```text
Metric:
CPUUtilization

Dimension:
InstanceId = i-xxxxxxxxxxxxxxxxx
```

This means:

> Show CPU utilization for this specific EC2 instance.

Without the dimension, you could have difficulty distinguishing one EC2 instance from another.

### Example

Suppose there are three servers:

```text
web-server
api-server
database-server
```

Each can have:

```text
CPUUtilization
```

CloudWatch distinguishes them using dimensions such as:

```text
InstanceId = i-111111
InstanceId = i-222222
InstanceId = i-333333
```

### Important idea

A useful mental model is:

```text
Namespace
    +
Metric Name
    +
Dimensions
    =
Specific metric identity
```

AWS documentation notes that each unique dimension combination is treated as a separate metric.

---

# 7. Statistics

CloudWatch statistics summarize metric datapoints over a selected period.

Common statistics are:

- Average
- Minimum
- Maximum
- Sum
- SampleCount
- Percentiles such as p95

## Average

Average gives the mean value during the selected period.

Example:

```text
10%
20%
30%
40%
50%
```

Average:

```text
30%
```

Formula:

```text
Average = Sum / SampleCount
```

## Minimum

The lowest observed value.

```text
10%
20%
30%
```

Minimum:

```text
10%
```

## Maximum

The highest observed value.

```text
10%
20%
30%
```

Maximum:

```text
30%
```

## Sum

Adds the values together.

```text
10 + 20 + 30 = 60
```

## SampleCount

Number of samples used for the statistic.

If five datapoints were used:

```text
SampleCount = 5
```

## Percentiles

A percentile describes the relative position of values in a dataset.

A common example is:

```text
p95
```

It helps answer:

> What value did 95% of observations stay below?

Percentiles are particularly useful for latency and performance analysis.

### CloudWatch statistics example

Suppose CPU data during a period is:

```text
20%
30%
40%
80%
90%
```

Then conceptually:

```text
Minimum = 20%
Maximum = 90%
Average = 52%
```

The statistic you choose should match the question you are asking.

---

# 8. Periods and Resolution

A **Period** defines the time interval represented by a CloudWatch datapoint.

Examples:

```text
1 minute
5 minutes
10 minutes
1 hour
```

Suppose CPU measurements are available every minute:

```text
12:00 → 10%
12:01 → 15%
12:02 → 20%
12:03 → 80%
12:04 → 70%
```

With a 1-minute period, you can see the individual minute-level values.

With a 5-minute period, CloudWatch can aggregate the available datapoints into a 5-minute statistic.

### Important distinction

Changing the graph period does **not automatically create higher-resolution source data**.

For standard EC2 instance metrics, EC2 normally publishes datapoints at 5-minute intervals. Enabling EC2 Detailed Monitoring provides 1-minute instance metric data.

Therefore:

```text
Basic Monitoring
      |
      v
5-minute EC2 metric data
```

while:

```text
Detailed Monitoring
      |
      v
1-minute EC2 metric data
```

This distinction is important when investigating short CPU spikes.

---

# 9. EC2 Metrics

Amazon EC2 automatically publishes several metrics to CloudWatch.

Common examples include:

### CPUUtilization

Measures EC2 CPU utilization.

```text
CPUUtilization = 75%
```

### NetworkIn

Network traffic received by the instance.

### NetworkOut

Network traffic sent by the instance.

### DiskReadOps

Number of completed read operations.

### DiskWriteOps

Number of completed write operations.

### StatusCheckFailed

Indicates whether EC2 status checks have failed.

For the hands-on project, the main metric is:

```text
AWS/EC2
    |
    └── CPUUtilization
```

AWS notes that the value shown by CloudWatch can differ from CPU utilization reported by operating-system tools because they measure from different perspectives.

---

# 10. Basic vs Detailed Monitoring

EC2 monitoring has an important distinction.

## Basic Monitoring

For standard EC2 instance metrics, AWS normally provides 5-minute datapoints.

```text
EC2
 |
 | CPUUtilization
 v
CloudWatch
 |
 +---- datapoint every ~5 minutes
```

## Detailed Monitoring

Detailed Monitoring enables 1-minute instance metric data.

```text
EC2
 |
 | CPUUtilization
 v
CloudWatch
 |
 +---- datapoint every minute
```

Detailed Monitoring is useful when:

- You need faster visibility.
- You are investigating short spikes.
- You need more frequent alarm evaluation.
- You are monitoring latency-sensitive infrastructure.

Detailed Monitoring can have additional charges, so it should be enabled intentionally.

---

# 11. CloudWatch Agent

EC2's default CloudWatch metrics do not provide every operating-system-level metric you may want.

For example, you may want:

```text
Memory utilization
Disk space
Disk usage
Swap
Processes
Log files
Application logs
```

The **CloudWatch Agent** can collect additional system-level metrics and logs.

Conceptually:

```text
EC2
│
├── CPU
├── Memory
├── Disk
├── Processes
└── Log files
       |
       v
CloudWatch Agent
       |
       +----------+
       |          |
       v          v
    Metrics      Logs
       |          |
       v          v
  CloudWatch   CloudWatch Logs
```

The agent can collect metrics from EC2 and other servers and can send logs to CloudWatch Logs.

A common default namespace for metrics collected by the agent is:

```text
CWAgent
```

### Why this matters for DevOps

Default EC2 monitoring might tell you:

```text
CPU = 80%
```

But the agent can help you investigate:

```text
Memory = 92%
Disk = 88%
```

That gives you more information for troubleshooting.

---

# 12. CloudWatch Logs

Metrics tell you **what is happening numerically**.

Logs tell you **what happened in detail**.

Example metric:

```text
CPUUtilization = 92%
```

Possible logs:

```text
2026-09-25 08:20 Application request started
2026-09-25 08:20 Database connection opened
2026-09-25 08:21 ERROR database timeout
```

This gives you the context behind a problem.

### Metrics vs Logs

| Metrics | Logs |
|---|---|
| Numerical | Text/event data |
| Good for trends | Good for detailed investigation |
| Easy to graph | Good for searching |
| Good for alarms | Good for debugging |

---

# 13. Log Groups and Log Streams

CloudWatch Logs uses a hierarchy.

```text
CloudWatch Logs
       |
       v
   Log Group
       |
   +---+---+
   |       |
   v       v
Stream  Stream
```

## Log Group

A **Log Group** is a logical collection of related logs.

Example:

```text
/aws/ec2/cloudwatch-lab
```

## Log Stream

A **Log Stream** is a sequence of log events from a particular source.

For example:

```text
Log Group:
    /aws/ec2/cloudwatch-lab

Streams:
    server-01
    server-02
```

A good naming strategy makes logs much easier to manage in production.

---

# 14. CloudWatch Logs Insights

**CloudWatch Logs Insights** allows you to query and analyze log data.

Instead of manually opening thousands of log events, you can query them.

A simple example:

```sql
fields @timestamp, @message
| sort @timestamp desc
| limit 20
```

This means:

- Show timestamp
- Show log message
- Sort newest first
- Return 20 results

Another useful pattern:

```sql
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50
```

This searches for log messages containing:

```text
ERROR
```

### DevOps use case

If an application suddenly reports a high error rate:

```text
CloudWatch Alarm
       |
       v
Engineer investigates
       |
       v
Logs Insights
       |
       v
Search ERROR messages
       |
       v
Find root cause
```

---

# 15. Metric Filters

A **Metric Filter** can look for patterns in CloudWatch Logs and turn matching events into numerical metrics.

Example:

```text
Application log
      |
      v
"ERROR database timeout"
      |
      v
Metric Filter
      |
      v
ApplicationErrors = 1
```

Then the resulting metric can be graphed or used in an alarm.

This creates a powerful pipeline:

```text
Application
    |
    v
Logs
    |
    v
Metric Filter
    |
    v
Custom Metric
    |
    v
Alarm
    |
    v
Notification
```

This is useful for application monitoring.

For example, instead of only monitoring:

```text
CPU > 80%
```

you can monitor:

```text
ApplicationErrors >= 5
```

---

# 16. CloudWatch Alarms

A **CloudWatch Alarm** watches a metric and evaluates it against a configured condition.

Example:

```text
CPUUtilization > 50%
```

The alarm can then change state and optionally perform an action.

Typical flow:

```text
CPUUtilization
      |
      v
CloudWatch Alarm
      |
      | CPU > 50%
      v
   ALARM state
      |
      v
     SNS
      |
      v
   Email
```

An alarm usually includes:

- Metric
- Statistic
- Period
- Threshold
- Comparison operator
- Evaluation periods
- Missing-data behavior
- Optional actions

### Example configuration

```text
Metric:
CPUUtilization

Statistic:
Average

Period:
5 minutes

Threshold:
50%

Condition:
Greater than 50%

Evaluation:
1 out of 1 datapoints
```

The exact configuration depends on the monitoring requirement.

---

# 17. Alarm States

CloudWatch alarms have three main states:

## OK

The metric is within the configured condition.

```text
CPU = 20%
Threshold = 50%

State = OK
```

## ALARM

The configured threshold condition has been met for the required evaluation period(s).

```text
CPU = 80%
Threshold = 50%

State = ALARM
```

## INSUFFICIENT_DATA

CloudWatch does not have enough data to determine the alarm state.

This can happen when:

- The resource is new.
- Metric data is delayed.
- The metric is not being published.
- The selected period contains insufficient data.

### Important

An alarm is not simply:

> "CPU is high."

It is a rule about a metric over time.

For example:

```text
IF
Average CPU > 50%
FOR
1 evaluation period
THEN
change alarm state
```

---

# 18. SNS Notifications

Amazon SNS can be used to send notifications when an alarm changes state.

Example:

```text
CPUUtilization
      |
      v
CloudWatch Alarm
      |
      v
     SNS
      |
      v
    Email
```

This means the monitoring system can notify an engineer without the engineer continuously watching the CloudWatch console.

A common production pattern is:

```text
Alarm
  |
  v
SNS Topic
  |
  +---- Email
  +---- Lambda
  +---- Other subscribers
```

---

# 19. CloudWatch Dashboards

A CloudWatch Dashboard is a visual monitoring page.

A dashboard can contain:

- CPU graphs
- Network graphs
- Alarms
- Custom metrics
- Logs-related widgets
- Other CloudWatch widgets

Example:

```text
+--------------------------------------+
|       Production Dashboard           |
+--------------------------------------+
| CPU                 | Memory         |
|  ███████            | █████████      |
|  72%                | 84%            |
+---------------------+----------------+
| Network             | Alarms         |
|  ████               | CPU: OK        |
|                     | Errors: ALARM  |
+---------------------+----------------+
```

Dashboards are useful because engineers can get an overview without opening every metric individually.

---

# 20. EventBridge and Automation

CloudWatch is closely related to **Amazon EventBridge**.

EventBridge is useful for event-driven automation.

Example:

```text
EC2 state change
      |
      v
EventBridge Rule
      |
      v
Target
      |
      +---- Lambda
      +---- SNS
      +---- SSM
      +---- Other AWS service
```

For example:

```text
IF EC2 instance enters STOPPED state
THEN
send notification
```

This is different from a metric alarm.

### Alarm

Usually evaluates:

```text
Metric → Threshold → Alarm
```

### EventBridge

Usually evaluates:

```text
Event → Pattern → Target
```

---

# 21. Custom Metrics

AWS services publish many built-in metrics, but you can also publish your own metrics.

For example, an application might publish:

```text
OrdersProcessed
ActiveUsers
PaymentFailures
QueueDepth
JobsCompleted
```

Conceptually:

```text
Application
     |
     | PutMetricData / OpenTelemetry / EMF
     v
CloudWatch
     |
     v
Custom Metric
     |
     +---- Dashboard
     |
     +---- Alarm
```

Example AWS CLI pattern:

```bash
aws cloudwatch put-metric-data \
  --namespace MyApplication \
  --metric-name OrdersProcessed \
  --value 25
```

You can add dimensions when you need to distinguish contexts.

Example:

```text
Application = Shop
Environment = Production
```

Custom metrics are useful when built-in AWS metrics do not represent an application's business or operational behavior.

---

# 22. CloudWatch vs CloudTrail

These services are commonly confused.

## CloudWatch

Primarily answers:

> **How is my infrastructure/application behaving?**

Examples:

```text
CPU = 80%
Memory = 90%
Errors = 15
Requests = 1000
```

## CloudTrail

Primarily answers:

> **Who made an AWS API call, what action was performed, and when?**

Example:

```text
User: admin
Action: DeleteBucket
Resource: example-bucket
Time: 08:32 UTC
```

### Simple comparison

| Service | Main purpose |
|---|---|
| CloudWatch | Monitoring and observability |
| CloudTrail | API activity and auditing |

They complement each other.

---

# 23. Hands-On Project

## Project Goal

The objective of this lab was to monitor an EC2 instance using Amazon CloudWatch.

The practical workflow was:

```text
EC2 Instance
     |
     v
Generate CPU workload
     |
     v
CPUUtilization metric
     |
     v
CloudWatch graph
     |
     v
CloudWatch Alarm
     |
     v
Threshold = 50%
```

### Lab resources

```text
EC2 Instance
Name: cloudwatch-lab-server

CloudWatch Namespace:
AWS/EC2

Metric:
CPUUtilization

Alarm threshold:
50%
```

---

# 24. CPU Spike Simulation

A Python script was used to generate CPU workload.

## Python script

```python
import time


def simulate_cpu_spike(duration=30, cpu_percent=80):
    print(f"Simulating CPU spike at {cpu_percent}%...")
    start_time = time.time()

    # Calculate the number of iterations needed to create
    # a CPU-intensive workload.
    target_percent = cpu_percent / 100
    total_iterations = int(target_percent * 5_000_000)

    # Perform simple arithmetic operations to consume CPU.
    for _ in range(total_iterations):
        result = 0
        for i in range(1, 1001):
            result += i

    # Wait for the remaining time.
    elapsed_time = time.time() - start_time
    remaining_time = max(0, duration - elapsed_time)
    time.sleep(remaining_time)

    print("CPU spike simulation completed.")


if __name__ == "__main__":
    simulate_cpu_spike(duration=30, cpu_percent=80)
```

## What the script does

The script intentionally performs CPU-intensive arithmetic operations.

The flow is:

```text
Python script
     |
     v
CPU-intensive loop
     |
     v
EC2 CPU usage increases
     |
     v
EC2 publishes CPUUtilization
     |
     v
CloudWatch receives metric
     |
     v
Graph shows CPU activity
```

### Important technical note

The `cpu_percent=80` value in this script is a **workload parameter**, not a precise guarantee that CloudWatch will report exactly 80%.

Actual CloudWatch CPU utilization depends on:

- EC2 instance type
- Number of vCPUs
- Operating-system scheduling
- Workload duration
- CloudWatch collection interval
- Monitoring configuration
- Other processes on the instance

Therefore, treat the script as a **CPU workload generator**, not a precision CPU benchmark.

---

# 25. Creating a CPU Alarm

After visualizing CPU utilization, a CloudWatch alarm was created.

## Alarm configuration used

```text
Metric:
CPUUtilization

Namespace:
AWS/EC2

Resource:
cloudwatch-lab-server

Statistic:
Average

Threshold:
50%

Condition:
CPUUtilization > 50%
```

The basic logic was:

```text
CPUUtilization
      |
      v
Is CPU > 50%?
      |
   +--+--+
   |     |
  No    Yes
   |     |
   v     v
  OK    ALARM
```

## Why 50%?

For this lab, 50% was chosen as an easy-to-observe threshold.

In production, thresholds should be selected based on:

- Application behavior
- Normal baseline
- Capacity
- Performance requirements
- Error rates
- Business impact

A threshold should not automatically be considered correct simply because it is a round number.

---

# 26. Screenshots for the Portfolio

Screenshots make the GitHub project easier to understand and provide evidence that the lab was actually performed.

Recommended structure:

```text
screenshots/
├── 01-ec2-instance.png
├── 02-cloudwatch-metric.png
├── 03-cpu-spike.png
├── 04-cloudwatch-alarm.png
└── 05-alarm-state.png
```

## Screenshot 1 — EC2 Instance

Show:

- EC2 instance name
- Running state
- Instance ID
- Status checks

Suggested filename:

```text
01-ec2-instance.png
```

## Screenshot 2 — CloudWatch Metric

Show:

- `AWS/EC2`
- `CPUUtilization`
- Correct EC2 instance
- Graph

Suggested filename:

```text
02-cloudwatch-metric.png
```

## Screenshot 3 — CPU Spike

Show the CPU utilization increase generated by the Python workload.

Suggested filename:

```text
03-cpu-spike.png
```

## Screenshot 4 — Alarm Configuration

Show:

- Alarm name
- CPUUtilization
- Threshold
- Statistic
- Period

Suggested filename:

```text
04-cloudwatch-alarm.png
```

## Screenshot 5 — Alarm State

If the workload caused the alarm to enter `ALARM`, capture that state.

Suggested filename:

```text
05-alarm-state.png
```

### Recommended GitHub layout

```text
AWS-CloudWatch-Deep-Dive/
│
├── README.md
│
├── scripts/
│   └── cpu_spike.py
│
├── screenshots/
│   ├── 01-ec2-instance.png
│   ├── 02-cloudwatch-metric.png
│   ├── 03-cpu-spike.png
│   ├── 04-cloudwatch-alarm.png
│   └── 05-alarm-state.png
│
└── docs/
    └── cloudwatch-guide.md
```

---

# 27. Troubleshooting

## Problem: CPU is high in Linux but CloudWatch graph looks low

Do not assume CloudWatch is broken.

Possible reasons include:

- CloudWatch and `top` measure from different perspectives.
- EC2 metrics may be published at 5-minute intervals under basic monitoring.
- The CPU workload may have started after the beginning of the CloudWatch period.
- You may be looking at an older datapoint.
- The selected metric may belong to a different instance.
- The AWS Console may need to refresh.
- Detailed Monitoring may not be enabled when minute-level data is expected.

### Verify the instance

```bash
hostname
```

and confirm the instance in the AWS console is the same EC2 server.

### Check CPU locally

```bash
top
```

### Check CPU count

```bash
nproc
```

### Check memory

```bash
free -h
```

### Check disk

```bash
df -h
```

---

## Problem: 1-minute period does not show a new datapoint

Selecting:

```text
Period = 1 minute
```

does not create one-minute EC2 source data.

For standard EC2 instance metrics, enable **Detailed Monitoring** if minute-level instance metric data is required.

---

## Problem: Alarm stays in INSUFFICIENT_DATA

Check:

1. Correct metric selected.
2. Correct instance selected.
3. Correct AWS region.
4. Metric is actively publishing.
5. Period matches available data.
6. Evaluation settings are reasonable.
7. The instance is running.

---

## Problem: Alarm does not immediately enter ALARM

CloudWatch alarms evaluate metric data according to the configured period and evaluation periods.

For example:

```text
Period = 5 minutes
Evaluation periods = 1
```

does not mean the alarm evaluates every second.

It means CloudWatch evaluates the configured metric statistic for the specified period.

---

# 28. DevOps Monitoring Workflow

A real DevOps monitoring system usually goes beyond one CPU graph.

A more complete architecture looks like this:

```text
                         AWS Environment
                                |
             +------------------+------------------+
             |                  |                  |
             v                  v                  v
            EC2               RDS              Application
             |                  |                  |
             +------------------+------------------+
                                |
                                v
                         CloudWatch
                    +-----------+-----------+
                    |                       |
                    v                       v
                 Metrics                  Logs
                    |                       |
                    |                  Logs Insights
                    |
              +-----+-----+
              |           |
              v           v
          Dashboard     Alarms
                          |
                          v
                         SNS
                          |
                          v
                       Engineer
```

A more automated environment can add EventBridge:

```text
CloudWatch / AWS Event
          |
          v
     EventBridge
          |
          v
     Automation
          |
     +----+----+
     |         |
   Lambda     SSM
```

---

# 29. Best Practices

## 1. Monitor what matters

Do not collect metrics simply because they exist.

Monitor signals that help answer operational questions.

Examples:

```text
CPU
Memory
Disk
Network
Errors
Latency
Request count
Availability
```

---

## 2. Use meaningful alarm thresholds

Do not blindly use:

```text
CPU > 80%
```

Instead, understand normal behavior first.

For example:

```text
Normal CPU:
20–40%

Warning:
>60%

Critical:
>80%
```

The actual thresholds should depend on the application.

---

## 3. Use multiple signals

CPU alone rarely explains an incident.

Combine:

```text
CPU
+
Memory
+
Disk
+
Network
+
Application Errors
+
Latency
```

---

## 4. Avoid alert fatigue

Too many alarms can become useless.

A good monitoring system should help engineers identify important conditions instead of generating unnecessary notifications.

---

## 5. Use dashboards for visibility

Dashboards are useful for:

- Operations
- Incident response
- Infrastructure reviews
- Capacity planning

---

## 6. Use Logs Insights for investigation

Metrics can tell you:

```text
Something is wrong.
```

Logs can help tell you:

```text
Why it is wrong.
```

---

## 7. Protect sensitive information

Do not put:

- Passwords
- Access keys
- Tokens
- API keys
- Private credentials

into GitHub screenshots or documentation.

Before publishing screenshots, inspect them for sensitive data.

---

## 8. Follow least privilege

IAM permissions used by CloudWatch agents and automation should provide only the permissions required for the task.

Avoid using highly privileged credentials unnecessarily.

---

# 30. Cost and Cleanup

CloudWatch has multiple billable components depending on what you use, including metrics, logs, alarms, dashboards, and other features.

Some AWS service metrics are provided without an additional custom-metric charge, while additional monitoring and custom telemetry can have costs.

Before leaving a lab running:

```text
Check:
✓ EC2 instance
✓ Detailed Monitoring
✓ CloudWatch alarms
✓ CloudWatch dashboards
✓ Log groups
✓ Custom metrics
✓ SNS subscriptions
```

## Lab cleanup

When the project is finished, consider:

```text
1. Stop or terminate the EC2 instance.
2. Disable Detailed Monitoring if it is no longer needed.
3. Remove unnecessary CloudWatch alarms.
4. Remove unnecessary dashboards.
5. Review CloudWatch log groups.
6. Review SNS topics/subscriptions.
7. Review any custom metrics.
```

Always verify that deleting a resource will not affect another project.

---

# 31. Key Takeaways

After completing this project, the main CloudWatch concepts are:

### Metrics

Numerical measurements over time.

```text
CPUUtilization = 72%
```

### Namespace

Groups related metrics.

```text
AWS/EC2
```

### Dimensions

Identify the resource/context.

```text
InstanceId = i-xxxxxxxx
```

### Statistics

Describe how metric data is aggregated.

```text
Average
Minimum
Maximum
Sum
SampleCount
Percentiles
```

### Period

Defines the time interval used for each datapoint/statistic.

```text
1 minute
5 minutes
10 minutes
```

### Logs

Detailed event information.

### Log Groups

Collections of related log streams.

### Log Streams

Sequences of log events from a source.

### Logs Insights

Query and analyze logs.

### Metric Filters

Turn matching log events into metrics.

### Alarms

Evaluate metrics against conditions.

### SNS

Send notifications.

### Dashboards

Visualize monitoring information.

### CloudWatch Agent

Collect additional system metrics and logs.

### EventBridge

React to events and automate actions.

---

# 32. Further Learning

The natural next steps after this lab are:

```text
CloudWatch Basics
       |
       v
EC2 Metrics
       |
       v
CloudWatch Agent
       |
       v
Memory + Disk Metrics
       |
       v
CloudWatch Logs
       |
       v
Logs Insights
       |
       v
Metric Filters
       |
       v
Alarms
       |
       v
SNS Notifications
       |
       v
Dashboards
       |
       v
EventBridge
       |
       v
Automation
       |
       v
Production Monitoring Architecture
```

Recommended hands-on progression:

1. Monitor EC2 CPU.
2. Add memory monitoring with CloudWatch Agent.
3. Add disk monitoring.
4. Send application logs to CloudWatch Logs.
5. Query logs with Logs Insights.
6. Create an application error metric using a Metric Filter.
7. Create alarms for CPU and application errors.
8. Send alarm notifications through SNS.
9. Build a CloudWatch Dashboard.
10. Use EventBridge for event-driven automation.
11. Connect monitoring with Auto Scaling.
12. Build a complete production-style observability project.

---

# Project Summary

This hands-on project demonstrated how AWS CloudWatch can monitor an EC2 instance.

The practical workflow was:

```text
              EC2
               |
               | CPU workload
               v
        CPUUtilization
               |
               v
        CloudWatch Metrics
               |
               v
             Graph
               |
               v
       CloudWatch Alarm
               |
         CPU > 50%
               |
               v
            ALARM
```

The project demonstrates an important DevOps principle:

> **Don't wait for users to report that a system is unhealthy. Monitor the system and detect problems proactively.**

---

## Official AWS Documentation

- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [CloudWatch Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html)
- [View CloudWatch Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/viewing_metrics_with_cloudwatch.html)
- [EC2 CloudWatch Metrics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html)
- [EC2 Monitoring](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-cloudwatch.html)
- [CloudWatch Statistics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html)
- [CloudWatch Agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)
- [CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
- [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)

---

## Author

**Haseeb Akhtar**

BS Software Engineering Student  
Cloud & DevOps Learner

Focus:

```text
AWS | Docker | Linux | Cloud | DevOps | SRE
```

---

> This repository is a learning and hands-on implementation project created to understand AWS CloudWatch monitoring concepts through practical experimentation.
