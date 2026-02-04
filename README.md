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

Insurance companies process **millions of claims annually**, yet most operate with batch processing systems that introduce critical delays:

| Challenge | Business Impact |
|:----------|:----------------|
| **Delayed Fraud Detection** | Fraudulent claims processed before patterns identified — costing insurers **$80B+ annually** |
| **Manual Processing Bottlenecks** | 15-45 day average claim settlement time |
| **Lack of Real-Time Visibility** | Executives make decisions on day-old data |
| **Seasonal Surge Blindness** | Monsoon/winter claim spikes overwhelm systems |

> **$308.6 billion** — Annual cost of insurance fraud to U.S. consumers
> *Source: Coalition Against Insurance Fraud*

---

## The Solution

This platform leverages **Microsoft Fabric Real-Time Intelligence** to create an end-to-end streaming analytics solution:

```
┌──────────────┐     ┌─────────────────────────────────────────────────────────────┐
│              │     │                    MICROSOFT FABRIC                         │
│   Python     │     │                                                             │
│   Simulator  │────▶│   Event Hub  ───▶  Eventstream  ───▶  Eventhouse (KQL)     │
│              │     │       │                                      │              │
│  1,000+/sec  │     │       │                                      ▼              │
│              │     │       │         ┌─────────────────────────────────────┐     │
└──────────────┘     │       │         │     Real-Time Dashboard            │     │
                     │       │         │     • Live Claims Metrics          │     │
                     │       │         │     • Fraud Detection Alerts       │     │
                     │       │         │     • Hospital Analytics           │     │
                     │       │         └─────────────────────────────────────┘     │
                     │       │                          │                          │
                     │       ▼                          ▼                          │
                     │   Real-Time Hub            Activator                        │
                     │   (Discovery)              (Alerts → Email/Teams)           │
                     │                                                             │
                     └─────────────────────────────────────────────────────────────┘
```

### Key Capabilities

| Capability | Description |
|:-----------|:------------|
| **Sub-second Latency** | From claim event to dashboard visualization |
| **Fraud Pattern Detection** | Statistical anomaly detection on claim amounts |
| **Seasonality-Aware** | Automatic volume adjustment for monsoon/winter periods |
| **Real-time KPIs** | Settlement rates, denial patterns, processing times |

---

## Microsoft Fabric Features

| Feature | Purpose | Docs |
|:--------|:--------|:-----|
| **Real-Time Hub** | Central discovery for streaming data | [Learn more →](https://learn.microsoft.com/en-us/fabric/real-time-hub/real-time-hub-overview) |
| **Eventstream** | No-code stream ingestion & transformation | [Learn more →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview) |
| **Eventhouse** | Time-series optimized KQL storage | [Learn more →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse) |
| **Real-Time Dashboard** | Live visualizations (10-sec refresh) | [Learn more →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/dashboard-real-time-create) |
| **Activator** | Event-driven alerts & automation | [Learn more →](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-introduction) |

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

### 2. Configure

```bash
cp config.json.example config.json
# Edit config.json with your Event Hub connection string
```

### 3. Run Simulator

```bash
python simulator.py
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

> **Full setup guide:** See [SETUP.md](SETUP.md) for detailed Fabric configuration steps.

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
| **Seasonality** | Winter (Dec-Jan): 1.4x · Monsoon (Jun-Sep): 1.6x |
| **Status Distribution** | Settled: 82% · Pending: 13% · Denied: 5% |
| **Claim Types** | Cashless: 65% · Reimbursement: 35% |
| **Fraud Indicators** | High amount + Low admissibility + Reimbursement |

---

## Sample KQL Queries

### Real-Time Claims Overview

```kql
ClaimsRaw
| where event_time > ago(1h)
| summarize
    TotalClaims = count(),
    TotalAmount = sum(total_amount),
    AvgProcessingDays = avg(processing_days)
```

### Fraud Detection — High Amount Anomalies

```kql
ClaimsRaw
| where event_time > ago(1h)
| where claim_type == "Reimbursement"
| where total_amount > 100000
| where (admissible_amount * 1.0 / total_amount) < 0.7
| project claim_id, policy_id, hospital_id, total_amount, admissible_amount
| order by total_amount desc
```

### Hospital Claims Trend

```kql
ClaimsRaw
| where event_time > ago(7d)
| summarize ClaimCount = count(), TotalAmount = sum(total_amount) by hospital_id
| top 10 by TotalAmount desc
| render barchart
```

> **More queries:** See [`kql/`](kql/) folder for fraud detection, claims overview, and hospital analytics queries.

---

## Activator Alerts

| Alert | Trigger | Action |
|:------|:--------|:-------|
| **Fraud Suspected** | `denial_reason == "Fraud Suspected"` | Email to fraud team |
| **High Volume Spike** | Claims/minute > 2000 | Teams notification |
| **Settlement Delay** | Processing days > 30 | Email to operations |
| **High Amount Claim** | Total amount > 500,000 | Manager approval |

---

## Project Structure

```
fabric-hackathon-rti/
├── simulator.py           # Python event simulator
├── config.json.example    # Configuration template
├── README.md              # This file
├── SETUP.md               # Detailed setup guide
├── LICENSE                # MIT License
└── kql/
    ├── claims-overview.kql
    ├── fraud-detection.kql
    └── hospital-analytics.kql
```

---

## Impact & Business Value

| Metric | Before | After | Improvement |
|:-------|:-------|:------|:------------|
| Fraud Detection | 15-30 days | < 1 minute | **99.9% faster** |
| Dashboard Refresh | Daily batch | 10 seconds | **Real-time** |
| Anomaly Response | Manual review | Automated | **Instant** |
| Processing Visibility | End-of-day | Live stream | **24/7** |

---

## References

**Microsoft Fabric Documentation:**
- [Real-Time Intelligence Overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview)
- [Eventstream Documentation](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview)
- [Eventhouse Documentation](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse)
- [Activator Documentation](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-introduction)
- [Azure Event Hubs Python SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/eventhub-readme)

**Training:**
- [Explore Real-Time Analytics in Microsoft Fabric](https://learn.microsoft.com/en-us/training/paths/explore-real-time-analytics-microsoft-fabric/)

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built for Microsoft Fabric Hackathon 2025</strong><br/>
  <sub>Real-Time Intelligence Category</sub>
</p>
