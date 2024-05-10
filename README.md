
# Infrastrcture as a Service and CDN as a Service

In this digital era where content creation and consumption are rising exponentially, a fast and efficient method for the delivery of content is imperative. The main objective of CDN is to load the content faster and reduce a user's buffer time. This is achieved by creating edge servers on multiple geographical locations. CDN will fetch cache data from the edge servers that are nearest to the user. In this Milestone we have implemented a similar concept on our Linux environment. Our project aims to offer CDN as a Service (CDNaaS) coupled with Infrastructure as a Service (IaaS), providing tenants with a comprehensive platform to manage and deploy their content delivery infrastructure seamlessly. Alongside CDN, our service also enables the users to provide any script to run on the servers they want to deploy, making us a software edge computing provider. With the ability to deploy their desired scripts to run on the edge, the user is not restricted and can deploy custom caching, purging, security, and many more features that they want to bring along with their request. 

## Architectrue

![Architectrue](https://github.com/VibhavDeo/LinuxNetworking_Iaas_Containers/blob/container/architecture.png)

1. ABC.com (CDN Customer) VPC: This VPC consists of a customer which wants to leverage the CDN service. With the help of IaaS, once it sets up its origin server, it can go ahead and request its specified requirements with the CDN service. The CDN fulfills the requirements of the customer by provisioning the necessary PoPs and establishing communication between the edge servers with the origin server. 
2. Public Container: The public container is the fundamental component of the cloud infrastructure. In our CDN service, It is one of the consistent and predefined elements for each tenant. It links the different VPCs with the internet and other VPCs if desired. In the context of CDNaaS, Its primary function is to efficiently direct incoming requests from different VPCs to the nearest location for optimized content delivery.
3. VPC: VPCs segregate a tenant's network from other VPC networks. A single tenant can have multiple VPCs and can enable communication between its VPCs if desired, which can be requested by the tenant using a northbound API. For CDN, We have implemented three distinct location VPCs apart from its own server’s VPC: IND, USA, and UK. When a tenant requests an edge server in a particular location, our system dynamically responds by integrating a corresponding virtual machine (Edge Server) and a unique subnet into the container. If multiple tenants request edge servers in the same geographic location, then all corresponding VMs will be connected to the same location VPC. We have used IP table rules to enforce isolation between different tenant edge servers.
4. Edge Servers: We offer edge servers to the tenants as a compute resource. Tenants have the flexibility to request edge servers at desired positions and of desired specifications such as processing power, memory, and storage capacity. These compute devices host web servers capable of handling incoming requests from users. The web server, running inside the VM, listens for HTTP GET requests and responds by delivering the requested content to the user. It periodically purges its cached data, to fetch fresh data from the origin server upon request from a user. 
5. DNS: This component is a part of our CDN service which is responsible for translating the incoming web addresses to the correct ip and port address. The DNS server is a smart server capable of redirecting the user to the next closest server available by analyzing the performance of the edge servers if the closest server fails to respond. The CDN server uses the country mapping list to provide the closest edge server location depending upon the location from where the request has originated from.
6. Host2: We've replicated our infrastructure across two hosts to bolster resilience and ensure uninterrupted service delivery. This approach enhances availability, increases fault tolerance, and mitigates risks associated with potential downtime on a host. By strategically distributing our resources, we prioritize reliability, providing our users with a seamless experience even in the face of unforeseen challenges. The two of the hosts' infrastructure are connected via a tunnel between them.

## Implementation

We have structured the implementation into two distinct components: Northbound and Southbound.
1. Northbound: The Northbound component serves as the interface through which tenants interact with the cloud infrastructure as well as the CDN service.

1.1. IaaS: The IaaS northbound APIs ease the customers' interaction with the underlying services. Here, tenants provide their specific requirements and specifications using YAML files. These files contain details such as the number of VPCs to be deployed and the subnet details for the infrastructure. The users can then deploy their machines on these subnets by providing the specifications. Users are also allowed to specify a python file if they want to run something on the newly deployed server.

1.2. CDNaaS: The CDNaaS northbound asks the users to provide the application they want to provide the CDN capability for along with the locations at which the user wants to deploy the edge server. This calls the IaaS northbound for the further deployment of infrastructure required for the cDN.

2. Southbound: The Southbound component is responsible for automating the creation of the underlying infrastructure after a tenant requests it using the Northbound API. Upon receiving processed input from the Northbound, the Southbound component initiates multiple Python scripts to execute various tasks required for infrastructure deployment. These scripts leverage Ansible playbooks for the creation of namespaces, containers, subnets, and VMs, ensuring that the cloud infrastructure is set up according to the tenant's requirements.

### Functional Requirements:

1. Data Distribution: One of the main functionalities of our project is to ensure seamless distribution of data across a distributed network of edge servers. This will ensure optimal delivery to end users regardless of their geographic location.

2. Content Delivery: To ensure efficient and reliable distribution of content to the end-users, we have implemented a robust content delivery system. Here the user would receive the content from the closest edge server. It also involves retrieval and transmission of content from the origin server to the edge servers in the absence of said data.

3. Provision points of presence: We provide seamless provisioning of Points of Presence (PoPs) across our network infrastructure. PoPs serve as strategic deployment locations for hosting edge servers and caching resources, allowing us to optimize content delivery by placing resources closer to end-users. By efficiently provisioning PoPs, we enhance the performance, reliability, and scalability of our content delivery network.

### Non-functional

1. Logging and Monitoring: We created a logging system for the customers of CDN where a customer requests for their logs then an API call would return information about their edge server creations ( like the timestamp of creation, location of edge server, and ID of the VM) and the logs would also contain information about the requests made to that server.We also added a feature of logging in our infrastructure such that for a particular customer we would show all the logs related to that customer. These logs would contain information about the creation of customer’s VPC, Subnet, and VMs.
   
2. Fault tolerance and High Availability: We integrated our other Host machine into our infrastructure with each resource having a replica running on this backup host machine. This would be useful in case any of the services/ servers are down in our main host machine then the resources in our backup machine would be used and the services would not be affected. 
Security against attacks: In situations where the nearest edge server may be compromised and unable to respond within a set time, we have enabled the service to fetch data from the next closest edge.

3. DNS: A critical non-functional requirement of our project is the reliable and efficient management of Domain Name System (DNS) services. DNS plays a pivotal role in translating user-friendly domain names into IP addresses, facilitating the resolution of web addresses, and the routing of network traffic. We also added load balancing to the DNS servers by actively distributing the requests among the DNS servers in 2 different host machines. 
Load Balancing: Our project provides load-balancing mechanisms to optimize resource utilization and ensure high availability and performance across our infrastructure.


