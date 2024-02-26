# Summary

## Library infos 

### Name
* readdatabrickstables

### Description
* The goal of this library is to provide two functions to connect to Databricks and query tables

### Functions
* **query_databricks_tables**(query, cluster_type, endpoint, token, cluster_id)
  * This function is able to use both SQL Warehouse and All-Purpose clusters to query tables and retrieve data as a Pandas Dataframe using **databricks-sql-connector** Library.
* **query_databricks_tables_api**(query, endpoint, token, warehouse_id)
  * This function is able to use SQL Warehouse Cluster to query tables and retrieve data as a Pandas Dataframe using [Databricks SQL Statement execution Rest API](https://docs.databricks.com/api/workspace/statementexecution/executestatement).  

## Usage

### Install the library
By installing this library, all the others required will be installed together.
* pip install readdatabrickstables==0.0.5

### Import the functions ( for Sql Connector and for Rest API ) needed
* from readbktbls.connect_and_read import *
* from readbktbls.connect_and_read_api import *

### Use the functions
Both functions returns a Pandas Data Frame
* **query_databricks_tables**(query, cluster_type, endpoint, token, cluster_id)
  * **query**        = SQL Query in Dict or String format 
  * **cluster_type** = "SQL" or "ALL-PURPOSE"
  * **endpoint**     = Databricks endpoint, ex.: 
  * **token**        = Your personal access token generated in the Databricks Workspace
  * **cluster_id**   = "SQL" Warehouse Cluster ID or "All-Purpose" Cluster ID according with what was passed in the **cluster_type** argument, find in the cluster detail page
* query_databricks_tables_api(query, endpoint, token, warehouse_id)
  * **query**        = SQL Query in Dict or String format 
  * **endpoint**     = Databricks endpoint, ex.: 
  * **token**        = Your personal access token generated in the Databricks Workspace
  * **cluster_id**   = "SQL" Warehouse Cluster ID, find in the cluster detail page