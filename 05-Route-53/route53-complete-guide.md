# Day 5 — Amazon Route 53 🌐

> **AWS Complete Guide — Day 5 of 30**

---

## 📚 Topics Covered

- DNS and Route 53
- Domain Names and IP Addresses
- Hosted Zones
- Public vs Private Hosted Zones
- DNS Records
- A, AAAA, CNAME, MX, TXT, NS, SOA
- Alias Records
- CNAME vs Alias
- TTL
- DNS Resolution
- Routing Policies
- Simple, Weighted, Failover, Latency, Geolocation
- Health Checks
- Route 53 + EC2
- Route 53 + Load Balancer
- Route 53 + CloudFront
- Route 53 + VPC
- Real-World Cloud Shop Architecture
- DevOps Perspective
- Quick Revision

---

# 1. What is DNS?

**DNS (Domain Name System)** translates human-friendly names into information computers can use.

```text
www.cloudshop.com
        ↓
   DNS lookup
        ↓
   98.81.69.67
```

### 💡 Real-Life Analogy

DNS is like your phone's contact list.

You remember:

```text
Ali
```

instead of remembering:

```text
0300-1234567
```

Similarly, users remember:

```text
cloudshop.com
```

instead of:

```text
98.81.69.67
```

> **Remember: DNS connects a name with a destination.**

---

# 2. What is Amazon Route 53?

**Amazon Route 53 is AWS's managed DNS service.**

It can:

- Register domains
- Host DNS zones
- Create DNS records
- Route DNS requests
- Perform health checks
- Support routing policies
- Provide public and private DNS

### Cloud Shop Example

Suppose our Cloud Shop runs on:

```text
EC2 Public IP: 98.81.69.67
```

Without DNS:

```text
User
  ↓
98.81.69.67:3000
  ↓
EC2
  ↓
Cloud Shop
```

With Route 53:

```text
User
  ↓
www.cloudshop.com
  ↓
Route 53
  ↓
98.81.69.67
  ↓
EC2
  ↓
Cloud Shop
```

> **Route 53 helps users find the application. It does not run the application.**

---

# 3. Route 53 vs Other AWS Services

| Service | Main Job |
|---|---|
| Route 53 | DNS |
| VPC | Networking |
| EC2 | Virtual server |
| ALB | Distribute application traffic |
| CloudFront | CDN |
| S3 | Object storage |
| RDS | Managed relational database |

Think:

```text
Route 53 → Where should the name resolve?
VPC      → How does network traffic move?
EC2      → Where does the application run?
ALB      → Which server receives application traffic?
```

---

# 4. Domain Name vs IP Address

An IP address identifies a network destination:

```text
98.81.69.67
```

A domain is a human-friendly name:

```text
www.cloudshop.com
```

DNS connects them:

```text
www.cloudshop.com
        ↓
98.81.69.67
```

### Why this matters

If the server's IP changes:

```text
Old IP → 98.81.69.67
New IP → 10.20.30.40
```

users can still use:

```text
www.cloudshop.com
```

You update DNS instead of asking users to remember a new IP.

---

# 5. How DNS Resolution Works

A simplified request looks like:

```text
Browser
   ↓
DNS Resolver
   ↓
Route 53
   ↓
DNS Record
   ↓
Destination
   ↓
Application
```

Example:

```text
www.cloudshop.com
        ↓
     Route 53
        ↓
     A Record
        ↓
   98.81.69.67
        ↓
       EC2
```

DNS finds the destination. The browser then connects to that destination.

---

# 6. Hosted Zone

A **Hosted Zone** is a container for DNS records for a domain.

Example:

```text
cloudshop.com
│
├── A
├── CNAME
├── MX
├── TXT
├── NS
└── SOA
```

### 💡 Analogy

Think of a Hosted Zone as a **DNS folder for a domain**.

```text
Domain
  ↓
Hosted Zone
  ↓
DNS Records
```

---

# 7. Public Hosted Zone

A **Public Hosted Zone** contains DNS records intended to be resolved through public DNS.

Example:

```text
www.cloudshop.com
        ↓
Public Hosted Zone
        ↓
98.81.69.67
```

Common uses:

- Public websites
- Public APIs
- Internet-facing applications

---

# 8. Private Hosted Zone

A **Private Hosted Zone** is used for DNS names inside associated VPCs.

Example:

```text
database.internal
        ↓
10.0.2.14
```

Architecture:

```text
VPC: 10.0.0.0/16
│
├── Public Subnet
│   └── Web Server
│
└── Private Subnet
    └── Database
        10.0.2.14
```

Instead of configuring:

```text
10.0.2.14
```

an application can use:

```text
database.internal
```

### Public vs Private

| Public Hosted Zone | Private Hosted Zone |
|---|---|
| Public DNS | Internal DNS |
| Internet-facing names | VPC resources |
| `www.cloudshop.com` | `database.internal` |

---

# 9. DNS Records

A DNS record tells DNS what information to return for a name.

| Record | Purpose |
|---|---|
| **A** | Name → IPv4 |
| **AAAA** | Name → IPv6 |
| **CNAME** | Name → another hostname |
| **MX** | Mail servers |
| **TXT** | Text / verification |
| **NS** | Authoritative name servers |
| **SOA** | Zone authority information |

---

# 10. A Record

An **A record** maps a name to an IPv4 address.

```text
www.cloudshop.com → 98.81.69.67
```

Example:

```text
Type: A
Name: www
Value: 98.81.69.67
```

Flow:

```text
www.cloudshop.com
        ↓
      A Record
        ↓
   98.81.69.67
        ↓
       EC2
```

> **A = IPv4**

---

# 11. AAAA Record

An **AAAA record** maps a name to an IPv6 address.

```text
www.cloudshop.com
        ↓
    AAAA Record
        ↓
     IPv6 address
```

Remember:

```text
A     → IPv4
AAAA  → IPv6
```

---

# 12. CNAME Record

A **CNAME** maps one hostname to another hostname.

Example:

```text
www.cloudshop.com
        ↓
      CNAME
        ↓
cloudshop.com
```

CNAME points to a **hostname**, not an IP address.

> **CNAME = Name → Another Name**

---

# 13. MX Record

**MX = Mail Exchange**

MX records specify mail servers for a domain.

```text
cloudshop.com
      ↓
   MX Record
      ↓
 Mail Server
```

They are used for email delivery.

---

# 14. TXT Record

TXT records store text associated with a domain.

Common uses:

- Domain verification
- Email security
- Service verification

Example:

```text
cloudshop.com
      ↓
    TXT
      ↓
Verification value
```

---

# 15. NS Record

**NS = Name Server**

NS records identify the authoritative name servers for a DNS zone.

Conceptually:

```text
cloudshop.com
      ↓
   NS Records
      ↓
Route 53 Name Servers
```

When a domain is registered with another registrar but DNS is hosted in Route 53, the domain is delegated to the Route 53 name servers.

---

# 16. SOA Record

**SOA = Start of Authority**

The SOA record contains important information about the DNS zone, such as:

- Primary name server
- Zone serial information
- DNS timing information

For beginner Route 53 work, you normally don't need to modify it.

---

# 17. Alias Record

An **Alias record** is a Route 53 feature that can point a DNS name to supported AWS resources.

Examples:

```text
Route 53
   ↓
Application Load Balancer
```

```text
Route 53
   ↓
CloudFront
```

```text
Route 53
   ↓
S3 website endpoint
```

### Cloud Shop Example

```text
www.cloudshop.com
        ↓
      Alias
        ↓
       ALB
        ↓
    EC2 instances
```

---

# 18. CNAME vs Alias

| CNAME | Alias |
|---|---|
| Name → hostname | Name → supported AWS resource |
| Standard DNS record | Route 53-specific |
| Useful for hostname-to-hostname | Useful for AWS services |
| Normal CNAME cannot be used at zone apex | Alias can be used at zone apex for supported targets |

Example:

```text
CNAME:
www.cloudshop.com → another.example.com
```

```text
Alias:
cloudshop.com → CloudFront
```

---

# 19. Zone Apex

The **zone apex** is the root of the domain.

For:

```text
cloudshop.com
```

the zone apex is:

```text
cloudshop.com
```

A normal CNAME cannot be used at the zone apex.

For supported AWS targets, Route 53 Alias records can be used instead.

---

# 20. TTL

**TTL = Time To Live**

TTL tells DNS resolvers how long they may cache a DNS answer.

Example:

```text
www.cloudshop.com
        ↓
98.81.69.67
        ↓
TTL = 300 seconds
```

That is:

```text
300 seconds = 5 minutes
```

### What happens if the IP changes?

Old:

```text
cloudshop.com → 98.81.69.67
```

New:

```text
cloudshop.com → 98.81.70.50
```

Resolvers that still have the old answer cached may continue using it until the cached TTL expires.

### Easy Rule

```text
Low TTL
   ↓
Faster DNS changes
   ↓
More frequent DNS queries

High TTL
   ↓
Longer caching
   ↓
Changes may take longer to appear
```

> **TTL is DNS cache duration, not server lifetime.**

---

# 21. Route 53 Routing Policies

Routing policies determine how Route 53 responds to DNS queries.

Important policies:

```text
Simple
Weighted
Failover
Latency-based
Geolocation
```

---

# 22. Simple Routing

Simple routing is the basic case.

One domain points to one destination.

```text
www.cloudshop.com
        ↓
     Route 53
        ↓
      EC2
98.81.69.67
```

Use this when the application has a simple DNS setup.

---

# 23. Weighted Routing

Weighted routing distributes DNS responses according to assigned weights.

Suppose we have:

```text
Cloud Shop v1 → Server 1
Cloud Shop v2 → Server 2
```

Weights:

```text
v1 → 90
v2 → 10
```

Conceptually:

```text
                 Route 53
                    |
              ┌─────┴─────┐
              ↓           ↓
            90%          10%
              ↓           ↓
           v1 Server    v2 Server
```

Useful for:

- Gradual releases
- Testing new versions
- Canary-style traffic shifting

Example:

```text
90% → old version
10% → new version
```

Then gradually:

```text
70% → old
30% → new

50% → old
50% → new

0% → old
100% → new
```

---

# 24. Failover Routing

Failover routing uses a primary and backup destination.

```text
                 Route 53
                    |
              Health Check
                    |
             ┌──────┴──────┐
             ↓             ↓
          Primary        Backup
             ↓             ↓
           EC2 #1        EC2 #2
```

Normal:

```text
User → Primary
```

Primary unhealthy:

```text
User → Backup
```

### Cloud Shop Example

```text
Primary EC2 → 98.81.69.67
Backup EC2  → 98.81.70.50
```

If the primary fails:

```text
Route 53
   ↓
Primary ❌
   ↓
Backup ✅
```

---

# 25. Latency-Based Routing

Latency-based routing chooses a destination based on network latency from the user.

Example:

```text
          Route 53
         /                ↓          ↓
   US Region    Singapore
       ↓            ↓
    Server         Server
```

A user may be sent to the destination that provides lower latency.

Example:

```text
Pakistan User
      ↓
   Route 53
      ↓
Singapore Server
```

> **Latency routing focuses on network performance.**

---

# 26. Geolocation Routing

Geolocation routing uses the geographic location of the user.

Example:

```text
Pakistan users
      ↓
Asia endpoint

US users
      ↓
US endpoint

Europe users
      ↓
Europe endpoint
```

### Latency vs Geolocation

| Latency | Geolocation |
|---|---|
| Based on network latency | Based on user location |
| Goal: lowest latency | Goal: geographic control |

---

# 27. Health Checks

A Route 53 health check checks whether an endpoint is healthy.

Conceptually:

```text
Route 53
   |
   | "Are you healthy?"
   ↓
Endpoint
   |
   ↓
HTTP / HTTPS / TCP
```

Result:

```text
Healthy ✅
```

or:

```text
Unhealthy ❌
```

Health checks are especially useful with failover routing.

---

# 28. Health Check + Failover

These concepts work together.

### Health Check

> **Is the endpoint healthy?**

### Failover Routing

> **Which endpoint should receive DNS responses?**

Example:

```text
                    Route 53
                       |
                  Health Check
                       |
              ┌────────┴────────┐
              ↓                 ↓
          Primary             Backup
              |
         Healthy?
          /             YES      NO
         ↓        ↓
      Primary   Backup
```

---

# 29. Route 53 + EC2

Basic architecture:

```text
Internet
   |
   ↓
Route 53
   |
   ↓
EC2
   |
   ↓
Application
```

Cloud Shop:

```text
www.cloudshop.com
        ↓
     Route 53
        ↓
98.81.69.67
        ↓
       EC2
        ↓
   Cloud Shop
```

---

# 30. Important: DNS Does Not Map the Application Port

Suppose Cloud Shop runs on:

```text
Port 3000
```

You might currently access:

```text
http://98.81.69.67:3000
```

DNS can resolve:

```text
www.cloudshop.com
        ↓
98.81.69.67
```

But DNS does not make the A record:

```text
98.81.69.67:3000
```

The port is handled by the connection/application layer.

A production setup commonly looks like:

```text
www.cloudshop.com
        ↓
Route 53
        ↓
Load Balancer
        ↓
EC2
        ↓
Application :3000
```

The public load balancer can listen on:

```text
80  → HTTP
443 → HTTPS
```

while the application can run internally on port `3000`.

---

# 31. Route 53 + Load Balancer

A production-style architecture:

```text
                    Users
                      |
                      ↓
                  Route 53
                      |
                    Alias
                      |
                      ↓
                    ALB
                 /                        ↓          ↓
             EC2 #1     EC2 #2
                \          /
                 \        /
                  Application
```

Route 53 does DNS.

The ALB distributes application traffic.

EC2 runs the application.

---

# 32. Route 53 + CloudFront

Route 53 can direct users to CloudFront.

```text
User
  |
  ↓
Route 53
  |
  ↓
CloudFront
  |
  ↓
Origin
```

The origin could be an application or storage service.

Example:

```text
www.cloudshop.com
        ↓
     Route 53
        ↓
    CloudFront
        ↓
Application / Static Content
```

---

# 33. Route 53 + VPC

Route 53 and VPC have different responsibilities.

### Route 53

```text
Where should this DNS name resolve?
```

### VPC

```text
How does network traffic move through AWS?
```

Example:

```text
Route 53
   |
   ↓
Destination
   |
   ↓
VPC
   |
   ↓
Subnet
   |
   ↓
EC2
```

---

# 34. Real-World Cloud Shop Example

Current Cloud Shop:

```text
Internet
   |
   ↓
EC2
98.81.69.67
   |
   ↓
Port 3000
   |
   ↓
Cloud Shop
```

Users have to remember:

```text
http://98.81.69.67:3000
```

With DNS:

```text
Internet
   |
   ↓
www.cloudshop.com
   |
   ↓
Route 53
   |
   ↓
98.81.69.67
   |
   ↓
EC2
   |
   ↓
Cloud Shop
```

### Production Version

```text
                    Users
                      |
                      ↓
                  Route 53
                      |
                      ↓
                  CloudFront
                      |
                      ↓
                 Load Balancer
                  /                          ↓           ↓
              EC2 #1       EC2 #2
                 \           /
                  \         /
                     RDS
                      |
                     S3
```

Possible responsibilities:

| Service | Job |
|---|---|
| Route 53 | DNS |
| CloudFront | CDN |
| ALB | Traffic distribution |
| EC2 | Application |
| RDS | Database |
| S3 | Files / objects |

---

# 35. Example: Development and Production

Route 53 can provide different names for different environments.

```text
Route 53
│
├── dev.cloudshop.com
│       ↓
│     Dev
│
└── www.cloudshop.com
        ↓
    Production
```

This is easier than remembering different IP addresses.

---

# 36. Example: Blue/Green Deployment

Suppose we have:

```text
Blue
 ↓
Cloud Shop v1

Green
 ↓
Cloud Shop v2
```

Route 53 can be part of a traffic-shifting strategy.

```text
             Route 53
                 |
          ┌──────┴──────┐
          ↓             ↓
        Blue          Green
         v1             v2
```

Weighted routing can be used to gradually move traffic to the new version.

---

# 37. Example: Disaster Recovery

A disaster recovery architecture may have:

```text
Primary Region
      ↓
 Primary Application

Backup Region
      ↓
 Backup Application
```

Route 53 failover can be part of the DNS layer:

```text
                 Route 53
                    |
              Health Check
                    |
          ┌─────────┴─────────┐
          ↓                   ↓
       Primary              Backup
       Region               Region
```

If the primary becomes unhealthy, DNS can return the backup endpoint according to the configured failover setup.

---

# 38. Route 53 Routing Policies — Quick Comparison

| Policy | Main Idea | Example |
|---|---|---|
| **Simple** | One destination | One EC2 |
| **Weighted** | Split traffic | 90% v1 / 10% v2 |
| **Failover** | Primary + backup | Primary EC2 / Backup EC2 |
| **Latency** | Lowest-latency destination | US vs Singapore |
| **Geolocation** | User location | Pakistan → Asia |

### Easy Memory Trick

```text
Simple
   ↓
One

Weighted
   ↓
Percentage

Failover
   ↓
Primary / Backup

Latency
   ↓
Fastest network path

Geolocation
   ↓
User location
```

---

# 39. Route 53 vs VPC vs EC2

This is a common beginner confusion.

```text
              Application Architecture

User
 ↓
Route 53
 ↓
VPC
 ↓
Subnet
 ↓
EC2
 ↓
Application
```

But each has a different role:

```text
Route 53 → DNS
VPC      → Network
Subnet   → Network segment
EC2      → Server
App      → Your software
```

---

# 40. Route 53 from a DevOps Perspective

DNS becomes important when managing real deployments.

A typical flow can look like:

```text
Developer
    |
    ↓
  GitHub
    |
    ↓
 CI/CD Pipeline
    |
    ↓
Docker Image
    |
    ↓
EC2 / ECS / EKS
    |
    ↓
Load Balancer
    |
    ↓
Route 53
    |
    ↓
Users
```

DevOps engineers commonly work with DNS for:

- Application deployments
- Multiple environments
- Load balancers
- Disaster recovery
- Multi-region systems
- Blue/green deployments
- Canary releases
- Domain management
- Service discovery

---

# 41. Important Terminology

| Term | Meaning |
|---|---|
| DNS | Domain Name System |
| Route 53 | AWS managed DNS service |
| Hosted Zone | Container for DNS records |
| Public Hosted Zone | Public DNS records |
| Private Hosted Zone | Internal VPC DNS |
| A | IPv4 record |
| AAAA | IPv6 record |
| CNAME | Hostname → hostname |
| MX | Mail server record |
| TXT | Text / verification |
| NS | Name server |
| SOA | Zone authority information |
| Alias | Route 53 record for supported AWS targets |
| TTL | DNS cache duration |
| Health Check | Endpoint health monitoring |
| Routing Policy | Controls DNS response routing |

---

# 42. Key Concepts to Remember

### DNS

```text
Domain Name
     ↓
DNS
     ↓
Destination
```

### Route 53

```text
AWS Managed DNS
```

### Hosted Zone

```text
DNS container for a domain
```

### A Record

```text
Name → IPv4
```

### AAAA Record

```text
Name → IPv6
```

### CNAME

```text
Hostname → Hostname
```

### Alias

```text
Name → Supported AWS Resource
```

### TTL

```text
DNS cache duration
```

### Health Check

```text
Is the endpoint healthy?
```

### Routing Policy

```text
How should Route 53 respond to DNS requests?
```

---

# 43. Quick Revision

Before moving to the next topic, make sure you can answer:

1. What is DNS?
2. What is Route 53?
3. Why is Route 53 called Route 53?
4. What is a Hosted Zone?
5. What is a Public Hosted Zone?
6. What is a Private Hosted Zone?
7. What is an A record?
8. What is an AAAA record?
9. What is a CNAME record?
10. What is an MX record?
11. What is a TXT record?
12. What is an NS record?
13. What is an SOA record?
14. What is an Alias record?
15. CNAME vs Alias?
16. What is a zone apex?
17. What is TTL?
18. What is Simple Routing?
19. What is Weighted Routing?
20. What is Failover Routing?
21. What is Latency-Based Routing?
22. What is Geolocation Routing?
23. What is a Health Check?
24. How does Route 53 work with EC2?
25. How does Route 53 work with a Load Balancer?
26. How does Route 53 work with CloudFront?
27. What is the difference between Route 53 and VPC?
28. How could Route 53 be used in a Cloud Shop architecture?

---

# 44. Day 5 Summary

The main mental model is:

```text
                   USER
                     |
                     ↓
              cloudshop.com
                     |
                     ↓
                 Route 53
                     |
                DNS Record
                     |
                     ↓
                Destination
                     |
                     ↓
             Application Layer
```

Basic Cloud Shop:

```text
www.cloudshop.com
        ↓
     Route 53
        ↓
      EC2
        ↓
   Cloud Shop
```

Production-style Cloud Shop:

```text
Users
  |
  ↓
Route 53
  |
  ↓
CloudFront
  |
  ↓
Load Balancer
  |
  ├───────────┐
  ↓           ↓
EC2 #1      EC2 #2
  \           /
   \         /
      RDS
       |
      S3
```

> **Route 53 = DNS**

> **Hosted Zone = DNS container**

> **A = IPv4**

> **AAAA = IPv6**

> **CNAME = Hostname → Hostname**

> **Alias = Name → Supported AWS resource**

> **TTL = DNS cache duration**

> **Routing Policy = How Route 53 responds**

> **Health Check = Is the endpoint healthy?**

---

## ✅ Day 5 Completed

**Topic:** Amazon Route 53

**Progress:** `5 / 30`

**Next:** Day 6 — Amazon S3
