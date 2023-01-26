def gremlin_list_conditions(local_client):
    _COMMAND = f"g.V().hasLabel('condition').path()"
    callback = local_client.submitAsync(_COMMAND)
    return callback
