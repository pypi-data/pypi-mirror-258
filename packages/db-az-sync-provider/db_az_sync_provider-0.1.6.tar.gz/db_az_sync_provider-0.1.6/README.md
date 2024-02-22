# databricks-azure-ad-sync-provider

## Prerequisites: Authentication

There are multiple options to authenticate to Microsoft Entra ID and Azure Databricks, we used the following two and you could choose in between.

**Option 1: If you have Azure CLI installed**
+ Run 'az login' on your machine to authenticate yourself as an Azure user.
+ Setup environment variables for DATABRICKS_HOST and DATABRICKS_ACCOUNT_ID, or create a .databrickscfg file (~ for Linux or macOS, and %USERPROFILE% for Windows) containing the following info:
```
[DEFAULT]
host = https://accounts.azuredatabricks.net/
account_id = <Databricks account id>
```

**Option 2: Use Microsoft Entra ID service principal:**
+ Create a service principal in Microsoft Entra ID and add it to Azure Databricks and grant it target permissions (see [reference documentation](https://learn.microsoft.com/en-gb/azure/databricks/dev-tools/service-principals))

+ Add the following environment varialbes:

- For Azure: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET (see [Microsoft Entra ID authentication](https://learn.microsoft.com/en-us/azure/communication-services/quickstarts/identity/service-principal?pivots=platform-azcli))
- For Databricks: DATABRICKS_HOST, DATABRICKS_ACCOUNT_ID, DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET (see [Databricks authentication](https://docs.databricks.com/en/dev-tools/auth/oauth-m2m.html#language-Environment))

+ Alternatively, you can setup databricks environment varialbes in a .databrickscfg file (~ for Linux or macOS, and %USERPROFILE% for Windows) containing the following info:
```
[DEFAULT]
host = https://accounts.azuredatabricks.net/
account_id = <Databricks account id>
azure_tenant_id = <Azure tenant id>
azure_client_id = <Azure service principal application ID>
azure_client_secret = <Azure service principal secret>
```


## Install
Run the following to install this package:
```
pip install db_az_sync_provider
```

## Usage
**Yaml file**
To use the package, it's required to provide:
+ Object ID(s) of Azure groups and (optionally) exclude object ID(s) in a yaml file (see syncgroups.yaml for example).
+ Existing relations between Azure and Databricks objects in a json file (see syncstates.json from example).

**Executions**
The following two arguments are asked when you execute the sync:
+ -f/--file <path to your yaml file>
+ -j/--json <path to your json file>
+ -d/--delete (if this option provided, you enable to delete identities in Databricks, it's recommended to not use this option though)
