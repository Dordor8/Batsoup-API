from abc import ABC


class Component(ABC):
    id: str
    type: str
    env_details: dict

class Extract(Component):
    def __init__(self, component_id: str, source_type: str, connection_details: dict):
        self.id = component_id
        self.type = source_type
        self.env_details = connection_details


class Transform(Component):
    def __init__(self, component_id: str, transformation_type: str, configuration_details: dict):
        self.id = component_id
        self.type = transformation_type
        self.env_details = configuration_details


class Load(Component):
    def __init__(self, component_id: str, destination_type: str, connection_details: dict):
        self.id = component_id
        self.type = destination_type
        self.env_details = connection_details

