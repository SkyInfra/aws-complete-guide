# AWS CloudWatch Deep Dive

A hands-on AWS monitoring project focused on understanding **Amazon CloudWatch** through practical EC2 monitoring, CPU utilization metrics, visualization, and CloudWatch alarms.

The goal of this project was not only to learn CloudWatch concepts, but also to understand how monitoring works in a real **Cloud & DevOps** environment.

---

## 🚀 Project Overview

In this project, I created an Amazon EC2 instance and used **Amazon CloudWatch** to monitor its CPU utilization.

I then generated an intentional CPU workload using Python and observed the change in CPU utilization through CloudWatch.

Finally, I created a CloudWatch alarm with a **50% CPU utilization threshold** to demonstrate how AWS can detect abnormal resource usage.

### Monitoring Flow

```text
                    Amazon EC2
                        │
                        │
                CPU workload
                        │
                        ▼
               CPUUtilization
                        │
                        ▼
                Amazon CloudWatch
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
           Metrics              Alarm
              │                   │
              ▼                   ▼
        Visualization        CPU > 50%
                                  │
                                  ▼
                              ALARM State
```

---

## 🎯 Objectives

The main objectives of this project were to understand:

* What Amazon CloudWatch is
* How CloudWatch metrics work
* EC2 CPU monitoring
* CloudWatch namespaces
* Dimensions
* Statistics
* Periods and monitoring resolution
* CloudWatch alarms
* Alarm states
* CloudWatch Logs
* CloudWatch Agent
* Logs Insights
* Metric Filters
* SNS notifications
* CloudWatch Dashboards
* EventBridge and automation

---

## 🛠️ Technologies Used

* **Amazon Web Services (AWS)**
* **Amazon EC2**
* **Amazon CloudWatch**
* **Python**
* **Linux / Ubuntu**
* **AWS Management Console**

---

# 🧪 Hands-On Experiment

## 1. Created an EC2 Instance

I created a dedicated EC2 instance for the CloudWatch experiment.

Instance name:

```text
cloudwatch-lab-server
```

The instance was used as the monitored infrastructure resource.

---

## 2. Generated CPU Workload

To create a CPU-intensive workload, I wrote a Python script that performs repeated arithmetic operations.

```python
import time


def simulate_cpu_spike(duration=30, cpu_percent=80):
    print(f"Simulating CPU spike at {cpu_percent}%...")
    start_time = time.time()

    target_percent = cpu_percent / 100
    total_iterations = int(target_percent * 5_000_000)

    for _ in range(total_iterations):
        result = 0
        for i in range(1, 1001):
            result += i

    elapsed_time = time.time() - start_time
    remaining_time = max(0, duration - elapsed_time)
    time.sleep(remaining_time)

    print("CPU spike simulation completed.")


if __name__ == "__main__":
    simulate_cpu_spike(duration=30, cpu_percent=80)
```

The script was executed on the EC2 instance to generate CPU activity.

> **Note:** `cpu_percent=80` is a workload parameter and does not guarantee that CloudWatch will report exactly 80% CPU utilization. Actual utilization depends on the instance, workload, operating system, and monitoring interval.

---

# 📊 CloudWatch CPU Monitoring

The EC2 CPU metric was viewed through:

```text
CloudWatch
    ↓
Metrics
    ↓
EC2
    ↓
Per-Instance Metrics
    ↓
CPUUtilization
```

The metric used was:

```text
Namespace: AWS/EC2
Metric: CPUUtilization
Dimension: InstanceId
```

This allowed me to visualize the CPU utilization of the specific EC2 instance.

---

# 🚨 CloudWatch Alarm

After monitoring the CPU utilization, I created a CloudWatch alarm.

### Alarm configuration

```text
Metric:
CPUUtilization

Statistic:
Average

Threshold:
50%

Condition:
CPUUtilization > 50%
```

The alarm evaluates the CPU metric and changes state when the configured threshold is breached according to the alarm's evaluation settings.

### Alarm logic

```text
CPUUtilization
       │
       ▼
Is CPU > 50%?
       │
   ┌───┴───┐
   │       │
  NO      YES
   │       │
   ▼       ▼
  OK      ALARM
```

This demonstrates how CloudWatch can detect resource conditions automatically instead of requiring an engineer to continuously watch the server.

---

# 📸 Screenshots

## EC2 Instance

![EC2 Instance](screenshots/01-ec2-instance.png)

## CloudWatch CPU Metric

![CloudWatch CPU Metric](screenshots/02-cloudwatch-cpu-metric.png)

## CPU Spike

![CPU Spike](screenshots/03-cpu-spike.png)

## CloudWatch Alarm

![CloudWatch Alarm](screenshots/04-cpu-alarm.png)

## Alarm State

![Alarm State](screenshots/05-alarm-state.png)

---

# 📚 CloudWatch Concepts Covered

| Concept          | What I learned                                             |
| ---------------- | ---------------------------------------------------------- |
| Metrics          | Numerical measurements collected over time                 |
| Namespace        | Logical grouping of metrics                                |
| Dimensions       | Identify the resource/context of a metric                  |
| Statistics       | Aggregate metric data such as Average, Minimum and Maximum |
| Period           | Time interval represented by a metric datapoint/statistic  |
| EC2 Monitoring   | Monitoring infrastructure metrics                          |
| CloudWatch Agent | Collecting additional system-level metrics and logs        |
| CloudWatch Logs  | Storing and analyzing log events                           |
| Log Groups       | Organizing related logs                                    |
| Log Streams      | Sequences of log events from a source                      |
| Logs Insights    | Querying CloudWatch logs                                   |
| Metric Filters   | Creating metrics from matching log patterns                |
| Alarms           | Detecting conditions from metrics                          |
| SNS              | Sending notifications                                      |
| Dashboards       | Visualizing monitoring information                         |
| EventBridge      | Event-driven automation                                    |

---

# 🏗️ Repository Structure

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
│   ├── 02-cloudwatch-cpu-metric.png
│   ├── 03-cpu-spike.png
│   ├── 04-cpu-alarm.png
│   └── 05-alarm-state.png
│
└── docs/
    └── cloudwatch-complete-guide.md
```

---

# 🔍 What I Learned

This hands-on helped me understand the difference between simply running an AWS resource and actually **monitoring it**.

The main monitoring workflow I practiced was:

```text
Infrastructure
      ↓
Metrics
      ↓
Visualization
      ↓
Threshold
      ↓
Alarm
      ↓
Response
```

I also learned that monitoring is more than CPU graphs. A production monitoring system can combine:

```text
Metrics
+
Logs
+
Alarms
+
Dashboards
+
Notifications
+
Automation
```

This forms an important foundation for Cloud and DevOps engineering.

---

# 📖 Complete Guide

A detailed CloudWatch learning guide is available here:

[CloudWatch Complete Guide](docs/cloudwatch-complete-guide.md)

The guide covers CloudWatch concepts from fundamentals through metrics, logs, alarms, dashboards, SNS, EventBridge, and practical monitoring architecture.

---

# 🔗 Useful AWS Documentation

* [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
* [CloudWatch Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html)
* [EC2 CloudWatch Metrics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html)
* [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
* [CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)

---

# 👨‍💻 Author

**Haseeb Akhtar**

BS Software Engineering Student

### Focus

```text
Cloud | DevOps | AWS | Docker | Linux | SRE
```

---

> This project was created as a hands-on learning exercise to understand AWS CloudWatch monitoring and apply Cloud/DevOps concepts using a real EC2 environment.
