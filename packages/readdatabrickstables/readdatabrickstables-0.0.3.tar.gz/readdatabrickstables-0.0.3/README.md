# Summary
## Library infos 
### Name
* readdatabrickstables
### Description
* The goal of this library is to provide two functions to connect to Databricks and query tables
### Functions
* **query_databricks_tables**(query, cluster_type, endpoint, token, warehouse_id, cluster_id)
  * This function can 
* **query_databricks_tables_api**(query, endpoint, token, warehouse_id)
  * This function ...
## Usage
### Install required libraries
* pip install readdatabrickstables==0.0.2
* pip install databricks-sql-connector==2.9.4
### Import the functions needed
*
* from readbktbls.connect_and_read import *

* Now you are 
* query_databricks_tables(query, cluster_type, endpoint, token, warehouse_id, cluster_id)
* 