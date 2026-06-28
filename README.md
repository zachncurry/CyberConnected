# CyberConnected

## Enterprise grade, high-throughput Cybersecurity Connection Suite designed to unify fragmented security telemetry.
   - **Goal:** Bridge the visibility gap in modern security operations. By providing a standardized, ultra-low-latency API connector suite, the project orchestrates the ingestion of continuous threat feeds, identity contexts, and infrastructure logs. It eliminates data silos by streaming concurrent telemetry into a unified data fabric, enabling security teams to query complex, multi-vector relationships at scale.
   - **Client Benefits:**
     - Unified Security Topology: Aggregates disjointed alerts from dozens of security tools into a single GraphQL endpoint, providing an immediate, panoramic view of the enterprise attack surface.
     - Proactive Blast Radius Mapping: By combining time-series event data with graph-based asset relationships, clients can visually trace lateral movement pathways before an actual breach occurs.
     - Zero System Degredation: Powered by Go microservices and Apache Kafka, the ingestion framework scales elastically to handle high-volume event storms (e.g., DDoS or massive log spikes) without dropping packets or delaying SOC visibility.
     - Vendor-Agnostic Extensibility: Simplifies compliance and reporting workflows by decoupling ingestion logic from the storage layer, allowing seamless integration with existing SIEM, SOAR, or EDR platforms.
   - **Tools:** [Go](https://go.dev/), [Python](https://www.python.org/), [Apache Kafka](https://kafka.apache.org/), [AWS Neptune/ Graph Database](https://aws.amazon.com/neptune/), [TimescaleDB](https://timescaledb.org/), [Mongo RelationalDB](https://www.mongodb.com/), [API Gateway Layer GraphQL](https://graphql-api-gateway.com/graphql-api-gateway-overview/what-is-a-graphql-api-gateway)
   - **Key Features:**
     - Real-Time Event Streaming: Fault-tolerant Kafka topics handle backpressure effortlessly during high-concurrency log events.
     - Multi-Model Data Correlation: Automatically splits incoming API payloads—routing temporal data to TimescaleDB and structural relationship modifications to AWS Neptune.
     - Declarative Querying: A unified GraphQL schema allows analysts to fetch tailored datasets without the over-fetching liabilities of traditional REST architectures.
     - Cloud-Native Elasticity: Designed from the ground up to be containerized, micro-segmented, and deployed natively within cloud ecosystems.
   - **High Level Architecture**
     - Ingestion Tier: High-performance Go daemons stream telemetry directly from upstream third-party security APIs, passing raw payloads to Python workers for structure normalization and MITRE ATT&CK framework enrichment.
     - Data Pipeline Layer: Normalized events are pushed onto optimized Kafka topics. Dedicated consumers subscribe to these topics and distribute the data downstream to the appropriate storage arrays based on the data type.
     - Unified Access Interface: The consumption layer exposes a robust GraphQL gateway. When an analyst queries an incident, the gateway intelligently queries the Time-Series layer for when it happened, the Graph layer for what else is impacted, and the Relational layer for who owns the asset—stitching it into a single response payload.



## Planning my approach
- Take inventory of cybersecurtiy appliances such as Switches, Routers, Firewalls, SIEMS, & SOARS
- Take inventory of cybsercurity platforms such as SIEMs, SOARs, VPNs, Intelligence Feeds
- Take inventory of Companies supporting the Cybersecuity Ecosystem such as Cisco, AWS, Azure, Google, IBM, Crowdstrike, Palo Alto, DataDog
- Select one company to focus efforts such as Cisco to then outline which APIs are needed to be built
- Develop unit tests for each API
- Develop 3 APIs
- Develop the infrastructure to aggregate/receive the API data
- Deploy foundational framework to support future build out to encompass additional appliances, software, and companies
- Potentially transition this project into an open source project for others to contibute additional API integrations

## Open Questions
- Should this have a UI or be kept as the back end only?
- How should keys be added? Is this part of the UI component?
- How should keys be managed/ stored?
- Should this be open sourced to enable others to contribute additional APIs?

## Company Selected
Cisco because this aligns with my study of Cisco DevNet.

## Appliances Selected
- Switches: Stream operational state, port statistics, and packet info using YANG-based RESTCONF/NETCONF or gRPC streaming telemetry.
   - Relational DB Data: Configurations
   - Telemetry DB Data: Syslogs    
- Routers: Send data using Model-Driven Telemetry (MDT) over gRPC, TCP, or UDP. They push continuous, real-time performance and routing data based on structured YANG data models.
   - Relational DB Data: Configurations
   - Telemetry DB Data: Syslogs  
- Firewalls: Export security events, connection logs, and threat intelligence using eStreamer APIs (Event Streamer) or secure REST API webhooks.
   - Relational DB Data: Configurations, Firewall Rules
   - Telemetry DB Data: Syslogs, Snort Logs (if available)  

_For the purposes of this project we will use the standard _syslog_ from all three appliances. However, Cisco does provide a unified view from their Firepower Management System._
_Additionally, while we are most interested in the Snort Logs generated by the Firewall Appliance we still want to ingest data directly from the Switches & Routers to correlate data as much as possible though it is not necessary. If we were to expand this project to layer an AI Agent to provide configuration changes this would be a required input. It is IMPORTANT to note there are many architecture/ implementation patterns that could be accomplished however, the end state of this project is to provide as many direct connections as possible as a library for others to use, enabling their desired pattern._

### Additional Snort Information
When Cisco bought Sourcefire (the creators of Snort), they integrated the Snort enginge directly into their next-gen firewall software.
A classic Cisco firewall does not have Snort enabled and must be managed by the an FMC, or another Add On Service like Snort, that generates the required files to detect Malware, Intrusion, MITRE ATT&CK Mapping Indicators.

### Process to Generate Outbound Data on Cisco Firepower Management Center (FMC) 
Only applicable for Cisco FMC - If you manage a Cisco firewall locally without an FMC, eStreamer is not available; you must use standard Syslog
1. Log into your Cisco FMC UI
2. Navigate to System > Integration > eStreamer
3. Client Create Client
4. Enter the IP Address of your log storage server or SIEM collector (Where we are hosting the API Infrascture)
5. Provide a strong Password (this is used later to decrupt the downloaded certificate)
6. Check all the security log types you want to stream under **Event Configuration** (eg Intrusion Events, Malware Events, Connection Events)
7. Click **Save**
8. Find your new client in the list and click the **Download Icon** to sve the .pkcs12 certificate file. (We will use this later in our infrastructure to decrypt what we receive from the appliance.)



