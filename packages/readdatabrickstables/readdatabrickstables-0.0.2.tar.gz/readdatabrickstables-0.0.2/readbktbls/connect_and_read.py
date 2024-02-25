def query_databricks_tables(query, cluster_type, endpoint, token, warehouse_id, cluster_id):
    ## REST API CONFIG ##
    endpoint_id = endpoint.split("-")[1].split(".")[0]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    # SQL CLUSTER INFOS #
    warehouse_state_api = f"https://{endpoint}/api/2.0/sql/warehouses/{warehouse_id}"
    warehouse_start_api = f"{warehouse_state_api}/start"

    # ALL-PURPOSE CLUSTER INFOS #
    # datarobot-execution-cluster
    cluster_state_api = f"https://{endpoint}/api/2.0/clusters/get"
    cluster_start_api = f"https://{endpoint}/api/2.0/clusters/start"
    params = {
        "cluster_id": cluster_id
    }

    if cluster_type.upper() == "ALL-PURPOSE":
        # All-Purpose Cluster
        http_path = f"sql/protocolv1/o/{endpoint_id}/{cluster_id}"
    elif cluster_type.upper() == "SQL":
        # SQL Warehouse Cluster
        http_path = f"/sql/1.0/warehouses/{warehouse_id}"
    else:
        raise Exception("Cluster type needs to be 'ALL-PURPOSE' or 'SQL'!")

    ## BUILD QUERY STRING ##
    # JSON / DICTIONARY TYPE INPUT
    if isinstance(query, dict):
        select_clause = query.get("select", "")
        from_clause = query.get("from", "")
        where_clause = query.get("where", "1=1")
        group_by_clause = query.get("group_by", "")
        having_clause = query.get("having", "")
        order_by_clause = query.get("order_by", "")

        query_string = f"SELECT {select_clause}\n FROM {from_clause}\n WHERE {where_clause}"

        if group_by_clause:
            query_string += f" \nGROUP BY {group_by_clause}"

        if having_clause:
            query_string += f" \nHAVING {having_clause}"

        if order_by_clause:
            query_string += f" \nORDER BY {order_by_clause}"

    # STRING TYPE INPUT
    elif isinstance(query, str):
        query_string = query

    # QUERY EXCEPTION
    else:
        raise Exception("Query needs to be a String or a Dictionary!")

    ## GET COLUMNS NAMES FROM QUERY ##
    pattern = re.compile(r'\bSELECT\b(.*?)\bFROM\b', re.DOTALL | re.IGNORECASE)
    splited_string = [n.strip() for n in re.search(pattern, query_string).group(1).strip().split(",")]
    columns = []
    new_pattern = re.compile(r'\bAS\s+(.*?)$', re.IGNORECASE)
    for n in splited_string:
        columns.append(re.search(new_pattern, n).group(1).strip()) if re.search(new_pattern, n) else columns.append(n)
    print(columns)

    select_star = False
    # IF THE QUERY IS SELECT *, NEED TO GET METADATA FROM TABLE
    if len(columns) == 1 and columns[0] == '*':
        select_star = True
        match = re.search(r'FROM (\S+)', query_string, re.IGNORECASE)
        if match:
            full_table_name = match.group(1)
            parts = full_table_name.split('.')
            if len(parts) == 2:
                schema, table = parts
            elif len(parts) == 3:
                _, schema, table = parts

    ## CHECK CLUSTERS TO START IF NEEDED ##
    if cluster_type.upper() == "SQL":
        # START SQL CLUSTER ##
        response = requests.get(warehouse_state_api, headers=headers)
        if response.json()["state"] != 'RUNNING':
            response = requests.post(warehouse_start_api, headers=headers, json={})
            if response.status_code == 200:
                print('Waiting cluster to start!')
                warehouse_starting = True
                while warehouse_starting:
                    time.sleep(120)
                    response = requests.get(warehouse_state_api, headers=headers)
                    warehouse_starting = response.json()["state"] != 'RUNNING'
                    print('Waiting, cluster still starting!')
            else:
                print("Warehouse cluster not started, trying again!")
                query_databricks_tables(query_string)
        else:
            print("Warehouse cluster is running!")

    else:
        # START ALL-PURPOSE CLUSTER ##
        response = requests.get(cluster_state_api, headers=headers, params=params)
        if response.json()["state"] != 'RUNNING':
            response = requests.post(cluster_start_api, headers=headers, json=params)
            if response.status_code == 200:
                print(f'Waiting cluster to start!')
                cluster_starting = True
                while cluster_starting:
                    time.sleep(120)
                    response = requests.get(cluster_state_api, headers=headers, params=params)
                    cluster_starting = response.json()["state"] != 'RUNNING'
                    print('Waiting, cluster still starting!')
            else:
                print("All-purpose cluster not started, trying again!")
                query_databricks_tables(query_string)
        else:
            print("All-purpose cluster is running!")

    ## RUN QUERY AND BUILD PANDAS DATA FRAME TO RETURN ##
    try:
        with sql.connect(
                # DATABRICKS CONNECTION DETAILS
                server_hostname=endpoint,
                http_path=http_path,
                access_token=token
        ) as conn:

            with conn.cursor() as cursor:
                # GET COLUMN NAMES FROM TABLE METADATA IF THE QUERY IS SELECT *
                if select_star:
                    columns = [row["COLUMN_NAME"] for row in
                               cursor.columns(schema_name=schema, table_name=table).fetchall()]

                # BUILD PANDAS DATAFRAME AND RETURN
                print("Return dataframe!")
                return pd.DataFrame(data=cursor.execute(query_string).fetchall(), columns=columns)

    ## HANDLE EXCEPTIONS ##
    except Exception as e:
        raise Exception(e)


def query_databricks_tables_api(query, endpoint, token, warehouse_id):
    ## REST API CONFIG ##
    api = "/api/2.0/sql/statements/"
    api_url = f"https://{endpoint}{api}"
    warehouse_state_api = f"https://{endpoint}/api/2.0/sql/warehouses/{warehouse_id}"

    # API REQUEST HEADER
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    ## BUILD QUERY STRING ##
    # JSON / DICTIONARY TYPE INPUT
    if isinstance(query, dict):
        print("Opção 1")
        select_clause = query.get("select", "")
        from_clause = query.get("from", "")
        where_clause = query.get("where", "1=1")
        group_by_clause = query.get("group_by", "")
        having_clause = query.get("having", "")
        order_by_clause = query.get("order_by", "")

        query_string = f"SELECT {select_clause}\n FROM {from_clause}\n WHERE {where_clause}"

        if group_by_clause:
            query_string += f" \nGROUP BY {group_by_clause}"

        if having_clause:
            query_string += f" \nHAVING {having_clause}"

        if order_by_clause:
            query_string += f" \nORDER BY {order_by_clause}"

    # STRING TYPE INPUT
    elif isinstance(query, str):
        print("Opção 2")
        query_string = query

    # EXCEPTION
    else:
        raise Exception("Query needs to be a String or a Dictionary!")
    print(query_string)

    # API BODY
    payload = {
        "warehouse_id": warehouse_id,
        "statement": query_string,
        "disposition": "EXTERNAL_LINKS",
        "format": "JSON_ARRAY"
    }

    ## API POST, RUN QUERY ##
    response = requests.post(api_url, headers=headers, json=payload)

    # CHECK RETURN
    if response.status_code == 200:
        statement_id = response.json()["statement_id"]
        print(f"SQL statement submitted successfully. Statement ID: {statement_id}")
        # print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")
        # raise Exception(f"Error: {response.status_code} - {response.text}")

    # CHECK STATE OF STATEMENT
    wait = True

    while wait:
        print('Waiting api return!')
        statement_current_state = requests.get(f"{api_url}{statement_id}", headers=headers)

        # RAISE EXCEPTION IF SOME ISSUE OCCURED WITH THE STATEMENT
        if statement_current_state.json()["status"]["state"] in ('FAILED', 'CANCELED', 'CLOSED'):
            raise Exception(
                "Statement ended, reason: {exception} | Message: {message}!".format(
                    exception=statement_current_state.json()["status"]["state"],
                    message=statement_current_state.json()["status"]["error"]["message"]
                )
            )
        else:
            # CHECK IF CLUSTER IS RUNNING
            cluster_current_state = requests.get(warehouse_state_api, headers=headers)
            if cluster_current_state.json()["state"] != 'RUNNING':
                time.sleep(120)
            else:
                # CHECK CURRENT STATE OF THE STATEMENT
                # print( statement_current_state.json() )
                wait = statement_current_state.json()["status"]["state"] != 'SUCCEEDED'

    # GET COLUMN NAMES FROM API RETURN
    columns = [col["name"] for col in statement_current_state.json()["manifest"]["schema"]["columns"]]

    # GET DATA FROM EXTERNAL LINKS
    array_to_become_df = []
    print(statement_current_state.json()["manifest"]["total_chunk_count"])
    for n in range(statement_current_state.json()["manifest"]["total_chunk_count"]):
        print(f"Current chunk: {n}!")
        external_link = \
        requests.get(f'{api_url}{statement_id}/result/chunks/{n}', headers=headers).json()["external_links"][0][
            "external_link"]
        for row in requests.get(external_link).json():
            array_to_become_df.append(row)
        # print(requests.get( external_link ).json())

    # RETURN PANDAS DATAFRAME
    print(len(array_to_become_df))
    return pd.DataFrame(data=array_to_become_df, columns=columns)
