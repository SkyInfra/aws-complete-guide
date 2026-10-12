# Day 18 — AWS Elastic Load Balancing (ELB)

## Overview

AWS Elastic Load Balancing (ELB) automatically distributes incoming traffic across registered targets, such as EC2 instances, IP addresses, and supported container or serverless targets. It provides a common entry point for applications and can improve availability and traffic management when configured correctly.

This guide explains why load balancers are used, the OSI layers relevant to load balancing, the four ELB types, their core components, and how to choose an appropriate type.

> **Learning goal:** Understand the concepts before creating billable AWS resources. The practical ALB lab can be documented separately after it has been completed and verified.

---

## 1. Why do we need a load balancer?

Imagine an online shopping website initially runs on one EC2 instance. As traffic increases, that instance may become overloaded. If it fails, the website may become unavailable.

Adding more instances gives the application more capacity, but clients still need a reliable entry point that directs requests to the right servers. A load balancer provides that entry point and distributes traffic among registered targets according to its configuration.

### Main benefits

- **Traffic distribution:** Spreads incoming requests or connections across targets.
- **Availability:** Health checks help the load balancer avoid routing new requests to unhealthy targets.
- **Scalability:** Can work with Auto Scaling or container orchestration to accommodate changing demand.
- **Common endpoint:** Clients can connect through a load balancer DNS name instead of choosing an individual backend instance.
- **Traffic management:** Depending on the type, it can support TLS termination, request-based routing, static IP addresses, or network security appliance integration.

**Important:** A load balancer does not automatically add EC2 instances or repair a failed application. Auto Scaling, resilient application design, and healthy dependencies are still required.

## 2. Load balancer architecture

A typical web application may use this architecture:

```text
Users / Clients
       |
       v
Load Balancer
       |
       v
Target Group
   /       \
  v         v
EC2-A      EC2-B
Application Application
```

For a highly available design, targets are commonly deployed across multiple Availability Zones. The exact architecture depends on the application and selected load balancer type.

## 3. What does Layer 7 mean?

The OSI model is a conceptual model that divides network communication into seven layers. For AWS load balancing, the most important distinction is between Layer 7 and Layer 4.

| Layer | Name | Simplified responsibility |
|---|---|---|
| 7 | Application | Application protocols and requests, such as HTTP |
| 6 | Presentation | Data representation and encoding concepts |
| 5 | Session | Communication session concepts |
| 4 | Transport | TCP/UDP transport, ports, and connections |
| 3 | Network | IP addressing and packet routing |
| 2 | Data Link | Frames and MAC addressing |
| 1 | Physical | Signals and physical transmission |

Implementations do not always map perfectly to one layer, but this model is useful for understanding load balancers.

### Layer 7 — Application layer

An Application Load Balancer (ALB) can use HTTP/HTTPS request information to make routing decisions. Depending on listener rules, this can include:

- Hostname, such as `shop.example.com`
- URL path, such as `/products/*`
- HTTP headers
- Query strings
- HTTP methods and other supported rule conditions

For example, rules could send `/products/*` to a products target group and `/users/*` to a users target group.

### Layer 4 — Transport layer

A Network Load Balancer (NLB) distributes connections using network and transport information, including IP addresses and ports. It supports TCP, UDP, and TLS listener configurations.

For example, an NLB can distribute TCP connections to a fleet of backend servers without using URL paths such as `/products` to choose a target.

**Key difference:** ALB makes application-aware routing decisions; NLB is designed for Layer 4 connection and traffic distribution.

---

## 4. The four types of AWS load balancers

### 4.1 Application Load Balancer (ALB)

**Layer:** 7  
**Best suited for:** HTTP/HTTPS applications and APIs

ALB understands HTTP/HTTPS requests and supports routing based on conditions such as hostnames and URL paths.

**Common use cases:**

- E-commerce websites
- REST APIs
- Microservices
- Web applications running on EC2
- Applications running on Amazon ECS or Amazon EKS

**Example:** Route `/products/*` to a product service and `/orders/*` to an order service.

**Why choose ALB?** Choose it when you need application-aware routing for web traffic.

### 4.2 Network Load Balancer (NLB)

**Layer:** 4  
**Best suited for:** High-performance network traffic and TCP/UDP services

NLB supports TCP, UDP, and TLS listener configurations. It is designed for high throughput and low latency and supports static IP addresses per enabled Availability Zone.

**Common use cases:**

- TCP-based services
- UDP-based applications
- Real-time or latency-sensitive services
- Workloads that need static IP addresses for allowlisting

**Example:** Distribute TCP connections on port `9000` across multiple backend servers.

**Why choose NLB?** Choose it when network-level traffic handling, performance, or static IP support is a key requirement.

### 4.3 Gateway Load Balancer (GWLB)

**Purpose:** Distribute traffic across virtual network appliances

GWLB is designed for deploying and scaling appliances such as virtual firewalls and intrusion detection/prevention systems. It uses GENEVE encapsulation to communicate with supported appliances.

**Common use cases:**

- Centralized network inspection
- Virtual firewall fleets
- Network security appliances
- Scaling traffic inspection without relying on a single appliance

**Example:** Distribute traffic across multiple virtual firewalls for inspection.

**Why choose GWLB?** Choose it when you need to deploy and scale network security appliances.

### 4.4 Classic Load Balancer (CLB)

**Generation:** Previous generation  
**Best suited for:** Existing legacy applications

CLB supports basic Layer 4 and Layer 7 load-balancing capabilities. For most new designs, evaluate ALB or NLB based on the application requirements.

**Common use case:** An older application that already relies on CLB configuration.

**Why know about CLB?** DevOps engineers may encounter it in existing infrastructure and need to understand or migrate it.

---

## 5. Compare the four types

| Feature | ALB | NLB | GWLB | CLB |
|---|---|---|---|---|
| Main purpose | HTTP-aware routing | Network traffic distribution | Virtual network appliances | Legacy load balancing |
| Main layer / model | Layer 7 | Layer 4 | Gateway and flow-based appliance integration | Layer 4 and Layer 7 capabilities |
| URL path routing | Yes | No ALB-style path rules | No | No ALB-style path rules |
| Static IP per enabled AZ | Not its standard model | Yes | Supported through its gateway-style integration | No |
| Typical use | Websites and APIs | TCP/UDP, high performance | Firewalls and traffic inspection | Existing legacy applications |

*Feature support varies by load balancer type and configuration. Consult AWS documentation before making production design decisions.*

## 6. Important ALB components

When learning ALB, understand these terms:

### Listener

A listener checks for connection requests using a configured protocol and port. Common examples are HTTP on port `80` and HTTPS on port `443`.

### Listener rules

Rules define conditions and actions. For example, a rule can forward requests matching `/api/*` to an API target group.

### Target group

A target group defines the registered destinations that receive forwarded requests. Depending on the target type and configuration, targets can include EC2 instances, IP addresses, or Lambda functions.

### Health checks

Health checks periodically test registered targets. A Node.js web application might expose a health endpoint such as `/health` on port `3000`.

If a target fails health checks, the load balancer can stop sending it new requests. This does not automatically repair the target or guarantee zero downtime.

### Security groups

For an ALB deployment, a common pattern is to allow intended client traffic to the ALB and allow backend application traffic to EC2 only from the ALB's security group. Configure rules according to the actual application and security requirements.

## 7. Real-world example: Node.js application

Suppose a Node.js application listens on port `3000` and runs on two EC2 instances.

```text
Users
  |
  v
Internet-facing ALB
Listener: HTTP :80 (or HTTPS :443)
  |
  v
Target Group: application port 3000
  |                         |
  v                         v
EC2-A                     EC2-B
Node.js app               Node.js app
/health                   /health
```

A possible request flow:

1. The client connects to the ALB DNS name.
2. The listener receives the request.
3. Listener rules select a forwarding action.
4. The target group provides the registered backend targets.
5. The ALB forwards the request to an eligible healthy target.
6. The application responds through the load balancer.

For production, prefer HTTPS where appropriate, restrict backend access to the load balancer, use multiple Availability Zones, and consider Auto Scaling and monitoring.

## 8. How to choose the right load balancer

### Scenario 1: E-commerce website

**Requirement:** Route `/products` and `/orders` to different services.  
**Choice:** ALB — supports HTTP path-based routing.

### Scenario 2: TCP service with static IP requirements

**Requirement:** Distribute TCP connections and provide static IP addresses per enabled Availability Zone.  
**Choice:** NLB.

### Scenario 3: Virtual firewalls

**Requirement:** Distribute traffic across a fleet of security appliances for inspection.  
**Choice:** GWLB.

### Scenario 4: Existing older application

**Requirement:** Maintain an application already built around Classic Load Balancer.  
**Choice:** CLB may remain in place while its migration options are evaluated.

---

## 9. Interview revision

1. **What is a load balancer?** A service that distributes incoming requests or connections across registered targets.
2. **Why do we use one?** To distribute traffic, improve availability, and provide a common endpoint.
3. **What does Layer 7 mean?** Application-layer processing; ALB can use HTTP request details for routing.
4. **What is Layer 4?** Transport-level handling; NLB distributes traffic using connection and network information.
5. **What is the difference between ALB and NLB?** ALB supports HTTP-aware rules; NLB focuses on Layer 4 traffic distribution.
6. **What is a target group?** A configured group of destinations that can receive forwarded traffic.
7. **What is a listener?** A configured entry point that accepts connections on a protocol and port.
8. **What do health checks do?** Help identify healthy targets so the load balancer can avoid routing new requests to unhealthy ones.
9. **What is GWLB used for?** Distributing traffic across virtual network appliances.
10. **Does a load balancer automatically add EC2 instances?** No. Auto Scaling or another scaling mechanism must provide additional capacity.

## 10. Hands-on lab plan

The next step is a separate practical lab using an Application Load Balancer.

- [ ] Check the AWS region and existing EC2 resources.
- [ ] Prepare two application targets in separate Availability Zones.
- [ ] Verify the application is running on port `3000`.
- [ ] Create a target group and configure the health check path.
- [ ] Create an ALB and configure its listener.
- [ ] Register the targets and wait for healthy status.
- [ ] Open the ALB DNS name and verify the application response.
- [ ] Test target health behavior safely.
- [ ] Capture screenshots as evidence.
- [ ] Delete lab resources when finished to avoid ongoing charges.

**Cost reminder:** An ALB incurs charges while provisioned. Review current regional pricing and clean up resources after the lab.

## 11. Official AWS references

- [Elastic Load Balancing overview](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
- [Application Load Balancer introduction](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
- [Network Load Balancer introduction](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)
- [Gateway Load Balancer introduction](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html)
- [Classic Load Balancer guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/introduction.html)

---

## Summary

- **ALB:** Layer 7; web applications, HTTP/HTTPS, path- and host-based routing.
- **NLB:** Layer 4; TCP/UDP/TLS listener use cases, high performance, static IP support.
- **GWLB:** Distributes traffic across virtual network and security appliances.
- **CLB:** Previous-generation load balancer, mainly relevant to legacy systems.

**Next:** Complete the ALB hands-on lab and add verified screenshots to the repository. Do not mark lab steps as completed until you have tested them.
