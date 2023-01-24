def clear_database(local_client):
    _COMMAND = "g.V().drop()"
    callback = local_client.submitAsync(_COMMAND)
    return callback
