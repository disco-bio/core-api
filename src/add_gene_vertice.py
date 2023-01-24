def add_gene_vertice(local_client, gene_name):
    _COMMAND = f"g.addV('gene').property('id', '{gene_name}').property('name', '{gene_name}').property('entity_type', 'gene').property('pk', 'pk')"
    callback = local_client.submitAsync(_COMMAND)
    return callback
