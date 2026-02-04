# Setup Guide - Real-Time Insurance Claims Intelligence Platform

This guide provides detailed step-by-step instructions for setting up the complete solution.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Microsoft Fabric** capacity (F4 minimum for testing)
- [ ] **Azure subscription** with Event Hubs access
- [ ] **Python 3.9+** installed locally
- [ ] **Git** for version control

---

## Part 1: Azure Event Hubs Setup

### Step 1.1: Create Event Hub Namespace

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **Create a resource** > Search for **Event Hubs**
3. Click **Create**
4. Fill in details:
   - **Subscription**: Select your subscription
   - **Resource group**: Create new or select existing
   - **Namespace name**: `claims-streaming-ns` (must be unique)
   - **Location**: Select nearest region
   - **Pricing tier**: **Standard** (recommended)
5. Click **Review + create** > **Create**

> **Reference**: [Create an Event Hubs namespace](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-create)

### Step 1.2: Create Event Hub Instance

1. Open your Event Hub namespace
2. Click **+ Event Hub**
3. Configure:
   - **Name**: `claims-stream`
   - **Partition count**: `4`
   - **Message retention**: `7` days
4. Click **Create**

### Step 1.3: Get Connection String

1. In your namespace, go to **Shared access policies**
2. Click **RootManageSharedAccessKey**
3. Copy the **Connection string-primary key**
4. Save this securely - you'll need it for configuration

---

## Part 2: Local Simulator Setup

### Step 2.1: Clone Repository

```bash
git clone https://github.com/mandelbulbtech-partners/fabric-hackathon-rti.git
cd fabric-hackathon-rti
```

### Step 2.2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 2.3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2.4: Configure Credentials

```bash
cp config/eventhub.json.example config/eventhub.json
```

Edit `config/eventhub.json` with your Event Hub details:

```json
{
  "simulator": {
    "default_rate": 1000,
    "batch_size": 100
  },
  "eventhub": {
    "namespace": "YOUR_NAMESPACE.servicebus.windows.net",
    "name": "claims-stream",
    "connection_string": "YOUR_CONNECTION_STRING_FROM_STEP_1.3",
    "consumer_group": "$Default"
  }
}
```

### Step 2.5: Test the Simulator

```bash
python src/simulator.py
```

You should see:
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

## Part 3: Microsoft Fabric Setup

### Step 3.1: Create Workspace

1. Go to [Microsoft Fabric](https://app.fabric.microsoft.com)
2. Click **Workspaces** > **New workspace**
3. Name: `Claims-Intelligence-Hackathon`
4. Click **Apply**

### Step 3.2: Create Eventstream

1. In your workspace, click **New** > **Eventstream**
2. Name: `claims-eventstream`
3. Click **Create**

#### Add Event Hub Source:

1. Click **Add source** > **Azure Event Hubs**
2. Configure:
   - **Source name**: `claims-eventhub`
   - **Cloud connection**: Create new
   - **Event Hub namespace**: Your namespace from Part 1
   - **Event Hub**: `claims-stream`
   - **Consumer group**: `$Default`
3. Click **Add**

> **Reference**: [Add Azure Event Hubs source](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-source-azure-event-hubs)

### Step 3.3: Create Eventhouse

1. Click **New** > **Eventhouse**
2. Name: `claims-eventhouse`
3. Click **Create**
4. A KQL Database named `claims-eventhouse` is auto-created

> **Reference**: [Create an Eventhouse](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/create-eventhouse)

### Step 3.4: Connect Eventstream to Eventhouse

1. Open your Eventstream
2. Click **Add destination** > **Eventhouse**
3. Configure:
   - **Destination name**: `claims-kql`
   - **Workspace**: `Claims-Intelligence-Hackathon`
   - **Eventhouse**: `claims-eventhouse`
   - **Database**: `claims-eventhouse`
   - **Table**: `ClaimsRaw` (create new)
4. Click **Add**

> **Reference**: [Add Eventhouse destination](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-destination-kql-database)

### Step 3.5: Create Real-Time Dashboard

1. Click **New** > **Real-Time Dashboard**
2. Name: `Claims Intelligence Dashboard`
3. Click **Create**

#### Add Data Source:

1. Click **New data source**
2. Select **OneLake data hub**
3. Choose `claims-eventhouse` database
4. Click **Connect**

#### Create Dashboard Tiles:

Use the KQL queries from the `src/kql/` folder to create tiles:

1. Click **Add tile**
2. Paste query from `src/kql/claims-overview.kql`
3. Configure visualization
4. Click **Apply changes**

Repeat for fraud detection and hospital analytics queries.

> **Reference**: [Create Real-Time Dashboard](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/dashboard-real-time-create)

### Step 3.6: Configure Activator Alerts (Optional)

1. In your Real-Time Dashboard, click on a tile
2. Click **Set alert**
3. Configure alert conditions:
   - **Condition**: `denial_reason == "Fraud Suspected"`
   - **Action**: Email or Teams notification
4. Click **Create**

> **Reference**: [Create Activator alerts](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/activator-tutorial)

---

## Part 4: Verification

### Verify Data Flow

1. **Start simulator** (if not running):
   ```bash
   python src/simulator.py
   ```

2. **Check Eventstream**:
   - Open your Eventstream
   - Verify events are flowing (green status)

3. **Query Eventhouse**:
   - Open KQL Database
   - Run: `ClaimsRaw | take 10`
   - Verify data appears

4. **View Dashboard**:
   - Open Real-Time Dashboard
   - Verify tiles update every 10 seconds

---

## Troubleshooting

### Simulator won't connect

- Verify connection string is correct
- Check Event Hub namespace is running
- Ensure firewall allows outbound connections

### No data in Eventhouse

- Check Eventstream shows green status
- Verify destination is properly configured
- Check for schema mapping issues

### Dashboard not updating

- Verify data source connection
- Check KQL query syntax
- Ensure auto-refresh is enabled (10 seconds)

---

## Next Steps

1. **Record demo video** (3 minutes max)
2. **Add screenshots** to README
3. **Update team information**
4. **Submit to hackathon**

---

**Need help?** Check the [Microsoft Fabric Documentation](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/)
