def add_drug_vertice(local_client, drug_name):
    _COMMAND = f"g.addV('drug').property('id', '{drug_name}').property('name', '{drug_name}').property('entity_type', 'drug').property('pk', 'pk')"
    callback = local_client.submitAsync(_COMMAND)
    return callback
