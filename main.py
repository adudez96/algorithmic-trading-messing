from google.cloud import bigquery, storage

def main() -> None:
    print("Running!")
    run_bigquery_client_test()
    run_storage_client_test()


def run_bigquery_client_test() -> None:
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row)


def run_storage_client_test() -> None:
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


if __name__ == "__main__":
    main()
