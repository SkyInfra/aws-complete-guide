# AWS VPC Guide

Amazon Virtual Private Cloud (VPC) allows you to create a logically isolated network in AWS where you can launch and control AWS resources.

VPC is one of the most important AWS services for Cloud and DevOps because services such as EC2, RDS, and Load Balancers commonly run inside a VPC.

---

## What is a VPC?

A **VPC (Virtual Private Cloud)** is a private network that you create inside AWS.

Think of a VPC like your own network inside AWS.

In a traditional network, you may have:

- Network
- Subnets
- Routers
- Firewalls
- Public and private networks

AWS provides similar networking components through VPC.

### Simple Example

```text
AWS
│
└── VPC
    │
    ├── Public Subnet
    │   └── Web Server
    │
    └── Private Subnet
        └── Database
VPC Components

The main VPC components are:

VPC
CIDR Block
Subnets
Availability Zones
Route Tables
Internet Gateway
NAT Gateway
Security Groups
Network ACLs
VPC Endpoints
DNS
1. CIDR Block

CIDR defines the IP address range of a VPC or subnet.

For example:

10.0.0.0/16

This can provide a large private IP address range for the VPC.

A VPC CIDR should be planned carefully because changing the primary CIDR later can be difficult.

Common Private IP Ranges

AWS VPCs commonly use private IP ranges such as:

10.0.0.0/8
172.16.0.0/12
192.168.0.0/16

Example:

VPC
10.0.0.0/16

The VPC can then be divided into smaller subnet ranges.

2. Subnet

A subnet is a smaller network inside a VPC.

For example:

VPC
10.0.0.0/16

├── Public Subnet
│   └── 10.0.1.0/24
│
└── Private Subnet
    └── 10.0.2.0/24

A subnet belongs to one Availability Zone.

A subnet cannot span multiple Availability Zones.

3. Public Subnet

A public subnet is a subnet that has a route to an Internet Gateway.

Example:

Internet
    │
    ▼
Internet Gateway
    │
    ▼
Public Subnet
    │
    ▼
EC2

A resource in a public subnet can communicate with the internet if:

Its subnet route table has a route to the Internet Gateway.
The resource has a public IPv4 address or another appropriate public connectivity mechanism.
Security Group rules allow the traffic.
Network ACL rules allow the traffic.
4. Private Subnet

A private subnet does not have a direct route to an Internet Gateway.

Example:

Internet
    X
    │
Private Subnet
    │
    └── Database

Private subnets are commonly used for resources that should not be directly accessible from the internet.

Examples:

Databases
Internal APIs
Backend services
Internal applications
5. Availability Zone

An Availability Zone (AZ) is an isolated location inside an AWS Region.

For example:

Region
│
├── AZ-1
│   ├── Public Subnet
│   └── Private Subnet
│
└── AZ-2
    ├── Public Subnet
    └── Private Subnet

For high availability, applications can use multiple Availability Zones.

6. Route Table

A route table controls where network traffic goes.

Example:

Destination       Target

10.0.0.0/16       local
0.0.0.0/0         Internet Gateway

Meaning:

10.0.0.0/16
     ↓
Stay inside the VPC

and:

0.0.0.0/0
     ↓
Send other traffic to the Internet Gateway
Important

A subnet is associated with a route table.

The route table determines how traffic from that subnet is routed.

7. Local Route

When a VPC is created, AWS automatically creates a local route.

Example:

Destination: 10.0.0.0/16
Target: local

This allows communication between resources using addresses inside the VPC CIDR.

For example:

EC2
10.0.1.10
   │
   │ VPC local routing
   ▼
EC2
10.0.2.10
8. Internet Gateway

An Internet Gateway (IGW) allows communication between a VPC and the internet.

Example:

Internet
    │
    ▼
Internet Gateway
    │
    ▼
VPC

For a subnet to be public, its route table normally contains:

0.0.0.0/0 → Internet Gateway
Important

Creating an Internet Gateway alone does not make a subnet public.

You also need the correct route table configuration.

9. NAT Gateway

A NAT Gateway allows resources in a private subnet to initiate connections to the internet without allowing unsolicited inbound internet connections directly to those resources.

Example:

Private EC2
    │
    ▼
NAT Gateway
    │
    ▼
Internet Gateway
    │
    ▼
Internet

A common architecture is:

Public Subnet
    │
    └── NAT Gateway
           │
           ▼
Private Subnet
    │
    └── Application Server

The private subnet route table can contain:

0.0.0.0/0 → NAT Gateway
NAT Gateway vs Internet Gateway
Internet Gateway	NAT Gateway
Provides internet connectivity for VPC resources	Provides outbound internet access for private resources
Used by public subnet routing	Commonly used by private subnet routing
Horizontally scaled by AWS	Managed AWS service
No hourly NAT processing charge	Has hourly and data-processing charges
10. Security Group

A Security Group acts as a virtual firewall for AWS resources such as EC2.

Security Groups control traffic at the resource level.

Example:

Internet
   │
   ▼
Security Group
   │
   ▼
EC2

Example inbound rules:

SSH
Port: 22
Source: My IP

HTTP
Port: 80
Source: 0.0.0.0/0
Important Security Group Characteristics
Stateful
Controls inbound traffic
Controls outbound traffic
Rules can allow traffic
No explicit deny rules
Return traffic is automatically allowed
11. Network ACL

A Network ACL (NACL) is another layer of network traffic control.

Unlike Security Groups, NACLs operate at the subnet level.

Example:

VPC
│
└── Subnet
    │
    └── NACL
        │
        └── EC2

NACLs contain:

Inbound rules
Outbound rules
Allow rules
Deny rules

NACL rules are evaluated according to their rule number.

12. Security Group vs NACL
Security Group	Network ACL
Resource level	Subnet level
Stateful	Stateless
Allow rules	Allow and deny rules
No rule ordering	Rules evaluated by number
Applied to resources such as EC2	Applied to subnets
Easy Way to Remember
Security Group
      ↓
"Can this resource receive the traffic?"

NACL
      ↓
"Can this subnet allow the traffic?"

Both can affect whether network traffic works.

13. Public vs Private Subnet

The main difference is the route to the Internet Gateway.

Public Subnet
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Public Route Table
   │
   ▼
Public Subnet

Route:

0.0.0.0/0 → Internet Gateway
Private Subnet
Private Route Table
       │
       ▼
Private Subnet

No direct route:

0.0.0.0/0 → Internet Gateway

A private subnet may use a NAT Gateway for outbound internet access.

14. VPC and EC2

When launching an EC2 instance, you can choose:

VPC
Subnet
Security Group
Private IP
Public IP configuration

Example:

VPC
10.0.0.0/16
│
└── Public Subnet
    10.0.1.0/24
        │
        └── EC2
            Private IP: 10.0.1.10
            Public IP: assigned if configured
15. Private IP vs Public IP
Private IP

Used for communication inside private networks such as the VPC.

Example:

10.0.1.10
Public IP

Used for communication over the public internet.

Example:

3.x.x.x

An EC2 instance can have both:

EC2
├── Private IP
└── Public IPv4

The private IP remains associated with the network interface, while a public IPv4 can be assigned for internet connectivity.

16. DNS in VPC

AWS VPC provides DNS functionality that allows resources to resolve domain names.

For example:

EC2
 │
 └── DNS
      │
      └── example.com

VPC DNS settings include:

DNS resolution
DNS hostnames

These are important for AWS services and applications that communicate using DNS names.

17. VPC Endpoints

A VPC Endpoint allows private connectivity from a VPC to supported AWS services without requiring traffic to travel through the public internet.

Example:

Private EC2
    │
    ▼
VPC Endpoint
    │
    ▼
AWS Service

For example, an EC2 instance in a private subnet can access S3 through an S3 VPC endpoint.

This can improve security and reduce the need for internet/NAT connectivity for supported services.

18. VPC Peering

VPC Peering allows two VPCs to communicate privately.

Example:

VPC A
10.0.0.0/16
    │
    │ VPC Peering
    │
    ▼
VPC B
10.1.0.0/16

The VPC CIDR ranges must not overlap for normal VPC peering connectivity.

Routes must also be configured correctly.

19. Transit Gateway

AWS Transit Gateway can connect multiple VPCs and networks through a central networking hub.

Example:

              Transit Gateway
             /       |       \
            /        |        \
         VPC A      VPC B      VPC C

This is useful when an organization has many VPCs and needs centralized network connectivity.

20. Typical AWS VPC Architecture

A common production-style architecture looks like this:

                         Internet
                            │
                            ▼
                    Internet Gateway
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Public Subnet                Public Subnet
           AZ-1                         AZ-2
              │                           │
          Load Balancer              Load Balancer
              │                           │
              └─────────────┬─────────────┘
                            │
                    Private Subnets
                       /         \
                      /           \
              Application       Application
                 Server            Server
                    \              /
                     \            /
                       Database

The exact architecture depends on the application.

21. Traffic Flow

Understanding traffic flow is very important for troubleshooting AWS networking.

For example, when connecting to a public EC2 instance:

Your Computer
      │
      ▼
Internet
      │
      ▼
Internet Gateway
      │
      ▼
Route Table
      │
      ▼
Subnet
      │
      ▼
NACL
      │
      ▼
Security Group
      │
      ▼
EC2

If the connection fails, any of these layers may be responsible.

22. Common VPC Troubleshooting Checklist

When an EC2 instance cannot be reached, check the following:

1. Correct VPC

Make sure the resource is inside the expected VPC.

2. Correct Subnet

Verify the EC2 instance is inside the intended subnet.

3. Route Table

Check whether the subnet is associated with the correct route table.

For a public subnet:

0.0.0.0/0 → Internet Gateway
4. Internet Gateway

Verify that the Internet Gateway is attached to the VPC.

5. Public IP

For direct internet access, verify the EC2 instance has an appropriate public IPv4 address.

6. Security Group

Check:

Port
Protocol
Source
Outbound rules
7. NACL

Check:

Inbound rules
Outbound rules
Rule numbers
Deny rules
8. Operating System Firewall

The AWS network configuration can be correct while the operating system firewall still blocks the connection.

23. Important VPC Concepts
VPC

Your isolated AWS network.

Subnet

A smaller network inside a VPC.

Route Table

Controls where traffic goes.

Internet Gateway

Provides internet connectivity for appropriate VPC routing.

NAT Gateway

Allows private resources to initiate outbound internet connections.

Security Group

Stateful firewall at the resource level.

NACL

Stateless firewall at the subnet level.

Availability Zone

An isolated location within an AWS Region.

VPC Endpoint

Private connectivity from a VPC to supported AWS services.

24. VPC Design Example

Suppose we create:

VPC
10.0.0.0/16

We can divide it into:

10.0.1.0/24 → Public Subnet AZ-1
10.0.2.0/24 → Private Subnet AZ-1
10.0.3.0/24 → Public Subnet AZ-2
10.0.4.0/24 → Private Subnet AZ-2

Architecture:

VPC: 10.0.0.0/16

AZ-1
├── Public:  10.0.1.0/24
└── Private: 10.0.2.0/24

AZ-2
├── Public:  10.0.3.0/24
└── Private: 10.0.4.0/24

This design provides separate public and private networks across multiple Availability Zones.

25. Key Takeaways
VPC is the foundation of AWS networking.
A VPC is defined using a CIDR block.
Subnets divide a VPC into smaller networks.
Each subnet belongs to one Availability Zone.
Public subnets normally have a route to an Internet Gateway.
Private subnets do not have a direct route to an Internet Gateway.
NAT Gateway is commonly used for outbound internet access from private subnets.
Route tables control network traffic paths.
Security Groups protect resources.
NACLs control traffic at the subnet level.
VPC Endpoints provide private access to supported AWS services.
Multiple Availability Zones can improve availability.
Understanding traffic flow is essential for Cloud and DevOps troubleshooting.
VPC Mental Model

The easiest way to remember VPC is:

VPC
 │
 ├── CIDR
 │
 ├── Subnets
 │    ├── Public
 │    └── Private
 │
 ├── Route Tables
 │
 ├── Internet Gateway
 │
 ├── NAT Gateway
 │
 ├── Security Groups
 │
 ├── NACLs
 │
 └── VPC Endpoints

Think of it as:

VPC = Your AWS Network

Subnet = Smaller network

Route Table = Where traffic goes

Internet Gateway = Internet connection

NAT Gateway = Private subnet → Internet

Security Group = Resource firewall

NACL = Subnet firewall
What I Learned

Through VPC learning, I understood how AWS networking is structured and how different networking components work together.

The most important concept is that network connectivity is not controlled by a single setting. Route tables, gateways, subnets, Security Groups, NACLs, IP addresses, and operating-system firewalls can all affect connectivity.

This foundation is important for working with EC2, Load Balancers, RDS, containers, Kubernetes, and production Cloud/DevOps environments.