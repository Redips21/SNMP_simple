from dataclasses import dataclass

@dataclass
class Parameter_Node:
    name: str
    oid: str
    max_value: int
    min_value: int
    target_value: any
    value: any = None




class Node:

    def __init__(self, name, ip, port, community, parameters: list[Parameter_Node]):
        self.name = name
        self.ip = ip
        self.port = port
        self.community = community
        self.parameters = parameters

    
    def getOids(self) -> dict[int, str]:
        #index_oid_pairs = {}
        #for index, parameter in enumerate(self.parameters):
        #   index_oid_pairs[index] = parameter.oid
        index_oid_pairs = []
        for parameter in self.parameters:
           index_oid_pairs.append(parameter.oid)
        return index_oid_pairs
