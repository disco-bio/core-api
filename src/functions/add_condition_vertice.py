def add_gene_vertice(local_client, condition_name):
    _COMMAND = f"g.addV('condition').property('id', '{condition_name}').property('name', '{condition_name}').property('entity_type', 'condition').property('pk', 'pk')"
    callback = local_client.submitAsync(_COMMAND)
    return callback
