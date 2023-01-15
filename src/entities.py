"""
Order from parent -> child:
[CONDITION] -> [GENE] -> ... -> [GENE] -> [DRUG]
"""


class BioEntity():

    def __init__(self, name, children, entity_type):
        self.name = name
        self.children = children
        self.entity_type = entity_type

    def return_children(self):
        return self.children

class Gene(BioEntity):

    def __init__(self, name, children):
        super().__init__(name, children, "GENE")

class Drug(BioEntity):
    
    def __init__(self, name, children):
        super().__init__(name, children, "DRUG")

class Condition(BioEntity):

    def __init__(self, name, children):
        super().__init__(name, children, "CONDITION")
