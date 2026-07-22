from dataclasses import dataclass


@dataclass
class Parameter_Node:
    name: str
    oid: str
    max_value: int
    min_value: int
    target_value: any
    value: any = None
    db_id: int = None

@dataclass
class Location_Node:
    building: str
    cabinet: str

class Node:
    def __init__(self, name, ip, port, community, location, parameters: list[Parameter_Node]):
        self.name = name
        self.ip = ip
        self.port = port
        self.community = community
        self.location = location
        self.parameters = parameters
        self.db_id: int = None

    def getOids(self) -> list[str]:
        return [parameter.oid for parameter in self.parameters]