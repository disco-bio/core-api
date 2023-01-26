def traverse_from_condition_until_drug(local_client, condition_name=None):
    _COMMAND = f"g.V().hasLabel('condition').has('id', '{condition_name}').repeat(out()).until(hasLabel('drug')).path()"
    callback = local_client.submitAsync(_COMMAND)
    return callback
