<p align="center">
  <img src="https://img.shields.io/badge/Microsoft-Fabric-0078D4?style=for-the-badge&logo=microsoft&logoColor=white" alt="Microsoft Fabric"/>
  <img src="https://img.shields.io/badge/Real--Time-Intelligence-00BCF2?style=for-the-badge" alt="Real-Time Intelligence"/>
  <img src="https://img.shields.io/badge/Azure-Event%20Hubs-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white" alt="Azure Event Hubs"/>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
</p>

<h1 align="center">Real-Time Insurance Claims Intelligence Platform</h1>

<p align="center">
  <strong>Microsoft Fabric Hackathon 2025 | Real-Time Intelligence Category</strong>
</p>

<p align="center">
  A production-ready streaming solution that transforms insurance claims processing through<br/>
  Microsoft Fabric's Real-Time Intelligence capabilities — enabling fraud detection,<br/>
  live monitoring, and data-driven decisions with sub-second latency.
</p>

---

## The Problem

Insurance companies process **millions of claims annually**, yet most operate with batch processing systems:

| Challenge | Business Impact |
|:----------|:----------------|
| **Delayed Fraud Detection** | $80B+ annual losses from undetected fraud |
| **Manual Processing** | 15-45 day average settlement time |
| **No Real-Time Visibility** | Decisions based on stale data |
| **Seasonal Blindness** | Systems overwhelmed during peak periods |

> **$308.6 billion** — Annual cost of insurance fraud to U.S. consumers

---

## The Solution

End-to-end streaming analytics using **Microsoft Fabric Real-Time Intelligence**:

```
┌──────────────┐     ┌─────────────────────────────────────────────────────────────┐
│              │     │                    MICROSOFT FABRIC                         │
│   Python     │     │                                                             │
│   Simulator  │────▶│   Event Hub  ───▶  Eventstream  ───▶  Eventhouse (KQL)     │
│              │     │                                             │               │
│  1,000+/sec  │     │                                             ▼               │
│              │     │                    Real-Time Dashboard ◄────┘               │
└──────────────┘     │                           │                                 │
                     │                           ▼                                 │
                     │                      Activator (Alerts)                     │
                     └─────────────────────────────────────────────────────────────┘
```

---

## Documentation

| Guide | Description |
|:------|:------------|
| [**01-FABRIC-FUNDAMENTALS.md**](docs/01-FABRIC-FUNDAMENTALS.md) | Workspace, Lakehouse, OneLake, Data Factory setup |
| [**02-RTI-SETUP.md**](docs/02-RTI-SETUP.md) | Eventstream, Eventhouse, Dashboard, Activator setup |
| [**03-AZURE-EVENTHUBS.md**](docs/03-AZURE-EVENTHUBS.md) | Event Hub namespace, credentials, Data Lake config |

---

## Quick Start

### Prerequisites

- Python 3.9+
- Azure subscription with Event Hubs
- Microsoft Fabric capacity (F4+ SKU)

### 1. Clone & Install

```bash
git clone https://github.com/mandelbulbtech-partners/fabric-hackathon-rti.git
cd fabric-hackathon-rti
pip install azure-eventhub
```

### 2. Configure & Run Simulator

```bash
# Set environment variables
set EVENTHUB_CONNECTION_STRING=Endpoint=sb://YOUR_NAMESPACE.servicebus.windows.net/;...
set EVENTHUB_NAME=claims-stream

# Run simulator
python src/simulator.py
```

```
============================================================
Insurance Claims Real-Time Simulator
Microsoft Fabric Hackathon 2025 - RTI Category
============================================================

Configuration:
  Event Hub: claims-stream
  Target Rate: 1,000 events/sec

Streaming CLAIM events @ ~1000/sec
Press Ctrl+C to stop
```

---

## Project Structure

```
fabric-hackathon-rti/
│
├── README.md                      # This file
├── LICENSE                        # MIT License
├── SETUP.md                       # Quick setup reference
│
├── docs/                          # Documentation
│   ├── 01-FABRIC-FUNDAMENTALS.md  # Fabric basics setup
│   ├── 02-RTI-SETUP.md            # Real-Time Intelligence setup
│   └── 03-AZURE-EVENTHUBS.md      # Azure Event Hubs setup
│
├── src/                           # Source code
│   ├── simulator.py               # Python event simulator
│   └── kql/                       # KQL query library
│       ├── claims-overview.kql
│       ├── fraud-detection.kql
│       └── hospital-analytics.kql
│
└── config/                        # Configuration templates
    └── datalake.json.example      # Data Lake shortcut credentials
```

---

## Microsoft Fabric Features

| Feature | Purpose | Documentation |
|:--------|:--------|:--------------|
| **Real-Time Hub** | Central discovery for streams | [Docs →](https://learn.microsoft.com/en-us/fabric/real-time-hub/real-time-hub-overview) |
| **Eventstream** | No-code stream ingestion | [Docs →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview) |
| **Eventhouse** | KQL database for time-series | [Docs →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse) |
| **Real-Time Dashboard** | Live visualizations | [Docs →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/dashboard-real-time-create) |
| **Activator** | Event-driven alerts | [Docs →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-introduction) |
| **Lakehouse** | Unified data storage | [Docs →](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview) |
| **Data Factory** | Pipeline orchestration | [Docs →](https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-overview) |

---

## Data Model

### Claims Event Schema

```json
{
  "claim_id": "CLM8A3F2B1C09",
  "policy_id": "POL000042",
  "hospital_id": "HSP000157",
  "claim_date": "2025-01-15T10:30:00Z",
  "settlement_date": "2025-01-30T14:00:00Z",
  "diagnosis_code": "A45",
  "claim_type": "Cashless",
  "total_amount": 45000,
  "admissible_amount": 38250,
  "settlement_status": "Settled",
  "denial_reason": null,
  "processing_days": 15,
  "event_time": "2025-02-04T08:15:30Z"
}
```

### Business Logic

| Parameter | Values |
|:----------|:-------|
| **Seasonality** | Winter: 1.4x · Monsoon: 1.6x |
| **Status** | Settled: 82% · Pending: 13% · Denied: 5% |
| **Types** | Cashless: 65% · Reimbursement: 35% |
| **Fraud Signals** | High amount + Low admissibility |

---

## Sample KQL Queries

### Real-Time Overview

```kql
ClaimsRaw
| where event_time > ago(1h)
| summarize TotalClaims = count(), TotalAmount = sum(total_amount)
```

### Fraud Detection

```kql
ClaimsRaw
| where event_time > ago(1h)
| where claim_type == "Reimbursement"
| where total_amount > 100000
| where (admissible_amount * 1.0 / total_amount) < 0.7
| project claim_id, policy_id, total_amount
| order by total_amount desc
```

> See [`src/kql/`](src/kql/) for complete query library.

---

## Impact & Business Value

| Metric | Before | After | Improvement |
|:-------|:-------|:------|:------------|
| Fraud Detection | 15-30 days | < 1 minute | **99.9% faster** |
| Dashboard Refresh | Daily | 10 seconds | **Real-time** |
| Anomaly Response | Manual | Automated | **Instant** |

---

## Configuration Reference

### Event Hub (Environment Variables)
```bash
EVENTHUB_CONNECTION_STRING=Endpoint=sb://NAMESPACE.servicebus.windows.net/;...
EVENTHUB_NAME=claims-stream
SIMULATOR_RATE=1000  # Optional, default 1000 events/sec
```

### Data Lake Shortcut Credentials
```json
{
  "datalake": {
    "url": "https://ACCOUNT.dfs.core.windows.net/",
    "sas_token": "sv=2024-11-04&ss=bf&...",
    "account_key": "YOUR_ACCOUNT_KEY"
  }
}
```

> Use these credentials to create a [OneLake shortcut](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts) to your Data Lake.

---

## References

**Microsoft Fabric:**
- [Real-Time Intelligence](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview)
- [Eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview)
- [Eventhouse](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse)
- [Activator](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-introduction)
- [OneLake](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview)

**Azure:**
- [Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/)
- [Python SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/eventhub-readme)

**Training:**
- [Real-Time Analytics Learning Path](https://learn.microsoft.com/en-us/training/paths/explore-real-time-analytics-microsoft-fabric/)

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built for Microsoft Fabric Hackathon 2025</strong><br/>
  <sub>Real-Time Intelligence Category</sub>
</p>
