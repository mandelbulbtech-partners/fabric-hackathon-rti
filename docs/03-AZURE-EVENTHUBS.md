# Azure Event Hubs Setup Guide

Complete guide for setting up Azure Event Hubs as the streaming ingestion layer.

---

## Prerequisites

- Azure subscription (free tier works for testing)
- Azure Portal access

---

## 1. Create Event Hub Namespace

### Steps

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **+ Create a resource**
3. Search for **Event Hubs** and select it
4. Click **Create**
5. Configure:

| Setting | Value |
|:--------|:------|
| **Subscription** | Your subscription |
| **Resource group** | Create new: `fabric-hackathon-rg` |
| **Namespace name** | `claims-streaming-ns` (must be unique) |
| **Location** | Select nearest region |
| **Pricing tier** | **Standard** (recommended) |
| **Throughput Units** | 1 (auto-inflate enabled) |

6. Click **Review + create** > **Create**

> **Reference**: [Create Event Hubs namespace](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-create)

---

## 2. Create Event Hub Instance

### Steps

1. Open your Event Hub namespace
2. Click **+ Event Hub**
3. Configure:

| Setting | Value |
|:--------|:------|
| **Name** | `claims-stream` |
| **Partition count** | 4 |
| **Message retention** | 7 days |
| **Capture** | Disabled (optional) |

4. Click **Create**

---

## 3. Get Connection Credentials

### Shared Access Policy (Connection String)

1. In namespace, go to **Shared access policies**
2. Click **RootManageSharedAccessKey** (or create a new policy)
3. Copy **Connection string-primary key**

### Format
```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyname>;SharedAccessKey=<key>;EntityPath=<eventhub>
```

---

## 4. Data Lake Storage Integration (Optional)

For archiving streaming data to Azure Data Lake Storage Gen2.

### Storage Account Configuration

| Setting | Example Value |
|:--------|:--------------|
| **Storage URL** | `https://<account>.dfs.core.windows.net/` |
| **Container** | `claims-archive` |
| **Authentication** | SAS Token or Account Key |

### SAS Token Format
```
sv=2024-11-04&ss=bf&srt=sc&sp=rwdlaciytfx&se=<expiry>&st=<start>&spr=https&sig=<signature>
```

### Account Key
- Found in Storage Account > Access Keys
- Use Key1 or Key2

> **Important**: Store credentials securely. Never commit to version control.

---

## 5. Configuration Templates

### config/eventhub.json.example
```json
{
  "eventhub": {
    "namespace": "YOUR_NAMESPACE.servicebus.windows.net",
    "name": "claims-stream",
    "connection_string": "Endpoint=sb://YOUR_NAMESPACE.servicebus.windows.net/;SharedAccessKeyName=YOUR_KEY_NAME;SharedAccessKey=YOUR_KEY;EntityPath=claims-stream"
  }
}
```

### config/datalake.json.example
```json
{
  "datalake": {
    "url": "https://YOUR_STORAGE_ACCOUNT.dfs.core.windows.net/",
    "container": "claims-archive",
    "sas_token": "YOUR_SAS_TOKEN",
    "account_key": "YOUR_ACCOUNT_KEY"
  }
}
```

---

## 6. Network Configuration

### Public Access (Default)
- Event Hub accessible from internet
- Suitable for development/testing

### Private Endpoint (Production)
- Create private endpoint in your VNet
- Configure Fabric Managed Private Endpoint

> **Reference**: [Event Hubs networking](https://learn.microsoft.com/en-us/azure/event-hubs/network-security)

---

## 7. Monitoring

### Key Metrics
- **Incoming Messages**: Events received
- **Outgoing Messages**: Events consumed
- **Throttled Requests**: Capacity exceeded
- **Active Connections**: Current connections

### Azure Monitor
1. Go to Event Hub namespace
2. Click **Metrics**
3. Add metrics to dashboard

---

## Pricing (Standard Tier)

| Component | Cost |
|:----------|:-----|
| Throughput Unit | ~$22/month per unit |
| Ingress Events | $0.028 per million |
| Capture (optional) | Storage costs only |

> **Reference**: [Event Hubs pricing](https://azure.microsoft.com/pricing/details/event-hubs/)

---

## References

- [Event Hubs documentation](https://learn.microsoft.com/en-us/azure/event-hubs/)
- [Create Event Hub](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-create)
- [Python SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/eventhub-readme)
- [Authentication](https://learn.microsoft.com/en-us/azure/event-hubs/authenticate-shared-access-signature)
