def add_blank_vertice(local_client):
    _COMMAND = f"g.addV('gene').property('id', 'blank_node').property('name', 'blank_node').property('entity_type', 'blank_node').property('pk', 'pk')"
    callback = local_client.submitAsync(_COMMAND)
    return callback
