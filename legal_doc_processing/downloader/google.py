from google.cloud import storage


def get_client(file_path="source/amiable-dynamo-245709-9dcfa045897a.json"):
    """ """

    client = storage.Client.from_service_account_json(file_path)
    return client


def get_buckets(client) -> list:
    """ """

    buckets = list(i for i in client.list_buckets())

    return buckets


def get_blobs(client, bucket="theolex_documents_processing") -> list:
    """ """

    blobs = list(client.list_blobs(bucket))
    return blobs


def get_file_names(client, bucket="theolex_documents_processing") -> list:
    """ """

    blobs = list(client.list_blobs(bucket))
    files = [i.name for i in blobs]

    return files


client = get_client()
# buckets = get_buckets(client)
# blobs = get_blobs(client)
files = get_file_names(client)
