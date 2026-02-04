# Microsoft Fabric Fundamentals Setup Guide

This guide covers the foundational setup steps for Microsoft Fabric before implementing Real-Time Intelligence.

---

## Prerequisites

- Microsoft 365 account with Fabric access
- Fabric capacity (Trial, F64+, or Power BI Premium P1)
- Admin permissions for workspace creation

---

## 1. Create a Fabric Workspace

### Steps

1. Sign in to [Microsoft Fabric](https://app.fabric.microsoft.com)
2. In the left navigation, select **Workspaces**
3. Click **+ New workspace** at the bottom
4. Configure:
   - **Name**: `claims-intelligence-workspace`
   - **Description**: Real-Time Insurance Claims Analytics
5. Expand **Advanced** settings:
   - **License mode**: Select your capacity (Trial/Fabric/Premium)
   - **Contact list**: Add team members for notifications
6. Click **Apply**

> **Reference**: [Create a workspace](https://learn.microsoft.com/en-us/fabric/fundamentals/create-workspaces)

---

## 2. Create a Lakehouse (Optional - for batch data)

### Steps

1. In your workspace, click **+ New item**
2. Select **Lakehouse**
3. Name: `claims-lakehouse`
4. Click **Create**

### What Gets Created
- Lakehouse storage (Files + Tables)
- SQL analytics endpoint (T-SQL access)
- Default semantic model

> **Reference**: [Create a lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse)

---

## 3. OneLake Storage Fundamentals

OneLake is automatically provisioned for your tenant. Key concepts:

### Storage Hierarchy
```
Tenant
  └── Workspaces
       └── Items (Lakehouse, Warehouse, Eventhouse)
            └── Files and Tables
```

### Connection URLs

| Type | Format |
|:-----|:-------|
| **HTTPS** | `https://onelake.dfs.fabric.microsoft.com/<workspace>/<item>` |
| **ABFS** | `abfs://<workspace>@onelake.dfs.fabric.microsoft.com/<item>` |

### Authentication
- Uses Microsoft Entra ID (Azure AD)
- Bearer tokens with Storage audience

> **Reference**: [OneLake overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview)

---

## 4. Data Factory Pipelines (Optional)

For batch data ingestion alongside real-time streaming:

### Create Pipeline

1. In workspace, click **+ New item** > **Data pipeline**
2. Name: `claims-batch-pipeline`
3. Add activities:
   - **Copy data**: Move data from sources to Lakehouse
   - **Dataflow**: Transform data with Power Query

### Common Sources
- Azure Blob Storage
- Azure SQL Database
- REST APIs
- Files (CSV, Parquet, JSON)

> **Reference**: [Data Factory overview](https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-overview)

---

## 5. Capacity Planning

### SKU Recommendations

| Workload | Minimum SKU | Recommended |
|:---------|:------------|:------------|
| Testing/POC | F4 (Trial) | F4 |
| Development | F8 | F16 |
| Production | F32 | F64+ |

### Key Limits
- Eventstream: Minimum 4 capacity units (F4)
- Real-Time Dashboard: 10-second minimum refresh
- Activator: 5-minute default evaluation interval

---

## Next Steps

After completing fundamentals setup:
1. Proceed to [02-RTI-SETUP.md](02-RTI-SETUP.md) for Real-Time Intelligence configuration
2. Set up Azure Event Hubs (see [03-AZURE-EVENTHUBS.md](03-AZURE-EVENTHUBS.md))

---

## References

- [Microsoft Fabric documentation](https://learn.microsoft.com/en-us/fabric/)
- [Create workspaces](https://learn.microsoft.com/en-us/fabric/fundamentals/create-workspaces)
- [Lakehouse overview](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview)
- [OneLake documentation](https://learn.microsoft.com/en-us/fabric/onelake/)
- [Data Factory overview](https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-overview)
