# Real-Time Intelligence Setup Guide

Complete step-by-step guide for setting up Microsoft Fabric Real-Time Intelligence components.

---

## Architecture Overview

```
Event Hub → Eventstream → Eventhouse (KQL) → Real-Time Dashboard → Activator
```

---

## 1. Create Eventhouse & KQL Database

### Steps

1. In your Fabric workspace, click **+ New item**
2. Search and select **Eventhouse**
3. Name: `claims-eventhouse`
4. Click **Create**

**Result**: Creates both Eventhouse and a default KQL database with the same name.

### Create Additional KQL Database (Optional)

1. In Eventhouse explorer, click **+ New database**
2. Name: `ClaimsDB`
3. Select **New database (default)**
4. Click **Create**

> **Reference**: [Create an Eventhouse](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/create-eventhouse)

---

## 2. Create Eventstream

### Steps

1. In workspace, click **+ New item**
2. Search and select **Eventstream**
3. Name: `claims-eventstream`
4. Click **Create**

### Add Azure Event Hubs Source

1. Click **Add source** > **External sources** > **Azure Event Hubs**
2. Click **New connection**
3. Configure:
   - **Event Hub namespace**: `your-namespace.servicebus.windows.net`
   - **Event Hub**: `claims-stream`
   - **Shared Access Key Name**: Your key name
   - **Shared Access Key**: Your key value
4. Click **Connect**
5. Configure consumer group: `$Default`
6. Data format: **JSON**
7. Click **Add**

> **Reference**: [Add Azure Event Hubs source](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-source-azure-event-hubs)

---

## 3. Connect Eventstream to Eventhouse

### Steps

1. In your Eventstream, click **Add destination**
2. Select **Eventhouse**
3. Configure:
   - **Destination name**: `claims-kql-destination`
   - **Workspace**: Select your workspace
   - **Eventhouse**: `claims-eventhouse`
   - **Database**: `ClaimsDB`
4. Ingestion mode: **Direct ingestion**
5. Click **Add**

### Configure Table

1. Click **Configure** on the Eventhouse destination node
2. Select **+ New table**
3. Name: `ClaimsRaw`
4. Click **Next**
5. Review schema mapping
6. Click **Finish**

> **Reference**: [Add Eventhouse destination](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-destination-kql-database)

---

## 4. Create Real-Time Dashboard

### Steps

1. In workspace, click **+ New item**
2. Select **Real-Time Dashboard**
3. Name: `Claims Intelligence Dashboard`
4. Click **Create**

### Add Data Source

1. Click **New data source**
2. Select **OneLake data hub**
3. Choose `claims-eventhouse` > `ClaimsDB`
4. Click **Connect**

### Add Dashboard Tiles

1. Click **Add tile**
2. Select data source from dropdown
3. Enter KQL query:

```kql
ClaimsRaw
| where event_time > ago(1h)
| summarize TotalClaims = count(), TotalAmount = sum(total_amount)
```

4. Click **Run**
5. Click **+ Add visual**
6. Select visualization type
7. Click **Apply changes**

### Configure Auto-Refresh

1. Go to **Manage** tab
2. Click **Auto refresh**
3. Enable and set to **10 seconds**
4. Click **Apply**

> **Reference**: [Create Real-Time Dashboard](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/dashboard-real-time-create)

---

## 5. Set Up Activator Alerts

### From Real-Time Dashboard

1. Select a tile on your dashboard
2. Click **Set Alert** from tile menu
3. Configure:
   - **Name**: `Fraud Detection Alert`
   - **Monitor frequency**: Every 5 minutes
   - **Condition**: When `denial_reason` equals `Fraud Suspected`
4. Add Action:
   - **Send email** to fraud team, OR
   - **Send Teams message** to channel
5. Click **Create**

### Alert Types

| Alert | Condition | Action |
|:------|:----------|:-------|
| Fraud Detected | `denial_reason == "Fraud Suspected"` | Email fraud team |
| High Volume | `count() > 2000` per minute | Teams notification |
| Large Claim | `total_amount > 500000` | Manager approval |

> **Reference**: [Activator alerts](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-get-data-real-time-dashboard)

---

## 6. Real-Time Hub (Discovery)

Real-Time Hub is automatically available - no setup required.

### Access

1. In Fabric portal, click **Real-Time** in left navigation
2. Browse all available streams and KQL tables
3. Actions available:
   - Preview data
   - Create alerts
   - Build dashboards

> **Reference**: [Real-Time Hub overview](https://learn.microsoft.com/en-us/fabric/real-time-hub/real-time-hub-overview)

---

## Verification Checklist

- [ ] Eventhouse created with KQL database
- [ ] Eventstream connected to Event Hub source
- [ ] Eventstream routing to Eventhouse destination
- [ ] Data flowing into `ClaimsRaw` table
- [ ] Real-Time Dashboard showing live data
- [ ] Auto-refresh enabled (10 seconds)
- [ ] Activator alerts configured

---

## Troubleshooting

| Issue | Solution |
|:------|:---------|
| No data in Eventhouse | Check Eventstream status (green = healthy) |
| Dashboard not updating | Verify auto-refresh is enabled |
| Alert not triggering | Ensure rule is in "Started" state |
| Schema mismatch | Review column mappings in Eventstream |

---

## References

- [Real-Time Intelligence overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview)
- [Eventstream documentation](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview)
- [Eventhouse documentation](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse)
- [Real-Time Dashboard](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/dashboard-real-time-create)
- [Activator documentation](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-introduction)
