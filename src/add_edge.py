def add_edge(local_client, parent_name, child_name):
    _COMMAND = f"g.V('{parent_name}').addE('links').to(g.V('{child_name}'))"
    callback = local_client.submitAsync(_COMMAND)
    return callback
