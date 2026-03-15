from src.metadata_handler.workflow_interpreter.components import Component, Extract, Load, Transform
from src.routes.route import Destination
from src.metadata_handler.workflow_creator.yaml_parser import *
from uuid import uuid4

ENV_IN_FOLDER = "INPUT_FOLDER"
ENV_OUT_FOLDER = "OUTPUT_FOLDER"
IN_PATH = "/tmp/input/"
OUT_PATH = "/tmp/output/"
IMAGE_PREFIX = "dorfa/aw-{name}:latest"

def value_in_dict(d: dict, value) -> bool:
    for k, v in d.items():
        if value == v or value == k:
            return True
    return False

class Workflow:
    components: list[Component]
    dependencies: dict[str, str]

    def __init__(self, name: str,
                 provider: str,
                 data_format: str,
                 schema_mapping: dict,
                 frequency: int,
                 file_size: int,
                 is_one_time_route: bool,
                 source_type: str,
                 source_connection_details: dict,
                 destinations: list[Destination]):
        self.name = name
        self.provider = provider
        self.data_format = data_format
        self.schema_mapping = schema_mapping
        self.is_one_time_route = is_one_time_route

        self.components = []
        self.dependencies = {}

        extract = Extract(str(uuid4()), source_type, source_connection_details)
        self.components.append(extract)

        for destination in destinations:
            load = Load(str(uuid4()), destination.destination_type, destination.destination_connection_details)
            self.components.append(load)

            self.dependencies[extract.id] = load.id


    def add_transformation_before_component(self, current_component_id: str, transformation: Transform) -> None:
        self.components.append(transformation)

        if not value_in_dict(self.dependencies, current_component_id):
            raise Exception(f"component {current_component_id} not found in dependencies")

        for key, value in self.dependencies.items():
            if value == current_component_id:
                del self.dependencies[key]

                self.dependencies[key] = transformation.id
                self.dependencies[transformation.id] = value


    def add_transformation_after_component(self, current_component_id: str, transformation: Transform) -> None:
        self.components.append(transformation)

        if not value_in_dict(self.dependencies, current_component_id):
            raise Exception(f"component {current_component_id} not found in dependencies")

        self.dependencies[current_component_id] = transformation.id

        for key, value in self.dependencies.items():
            if key == current_component_id:
                del self.dependencies[key]

                self.dependencies[transformation.id] = value

    def to_yaml(self, path: str) -> None:
        templates: list[dict] = []
        tasks: list[dict] = []

        for component in self.components:
            if isinstance(component, Load):
                image = IMAGE_PREFIX.format(name=component.type)
                component.connection_details[ENV_OUT_FOLDER] = OUT_PATH
                templates.append(get_template(None, component.type + component.id, image, component.connection_details, {'output': OUT_PATH}))