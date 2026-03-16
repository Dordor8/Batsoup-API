from src.metadata_handler.workflow_interpreter.components import Component, Extract, Load, Transform
from src.routes.route import Destination
from src.metadata_handler.workflow_creator.yaml_parser import *
from src.metadata_handler.workflow_interpreter.validation_default import DEFAULT_VALIDATION_DETAILS
from uuid import uuid4

ENV_SCHEMA = "SCHEMA"
ENV_IN_FOLDER = "INPUT_FOLDER"
ENV_OUT_FOLDER = "OUTPUT_FOLDER"
ENV_WORKFLOW_NAME = "WORKFLOW_NAME"
IN_PATH = "/tmp/input/"
OUT_PATH = "/tmp/output/"
IMAGE_PREFIX = "dorfa/aw-{name}:latest"
FROM_ARTIFACT_PREFIX = "tasks.{name}.outputs.artifacts.output"
S3_LOAD_TYPE = "s3-writer"



def value_in_dependencies(dependencies: list[tuple[str, str]], value: str) -> bool:
    for dependency in dependencies:
        if value == dependency[0] or value == dependency[1]:
            return True
    return False

def new_id() -> str:
    return 'a' + str(uuid4().hex[:8])

class Workflow:
    components: list[Component]
    dependencies: list[tuple[str, str]]

    def __init__(self, name: str,
                 provider: str,
                 data_format: str,
                 schema_mapping: dict,
                 frequency: int,
                 file_size: int,
                 is_one_time_route: bool,
                 source_type: str,
                 source_connection_details: dict,
                 destinations: list[Destination],
                 add_default_transformations: bool,):
        self.name = name
        self.provider = provider
        self.data_format = data_format
        self.schema_mapping = schema_mapping
        self.is_one_time_route = is_one_time_route

        self.components = []
        self.dependencies = []

        extract = Extract(new_id(), source_type, source_connection_details)
        self.components.append(extract)

        for destination in destinations:
            load = Load(new_id(), destination.destination_type, destination.destination_connection_details)
            self.components.append(load)

            self.dependencies.append((extract.id, load.id))

        if add_default_transformations:
            self.default_transformations(extract.id)

    def default_transformations(self, extract_id) -> None:
        DEFAULT_VALIDATION_DETAILS[ENV_WORKFLOW_NAME] = self.name + '-' + new_id()
        validation = Transform(new_id(), 'data-validation', DEFAULT_VALIDATION_DETAILS)
        self.add_transformation_after_component(extract_id, validation)

        for component in self.components:
            if component.type == S3_LOAD_TYPE:
                optimization = Transform(new_id(), 's3-optimization', {})
                self.add_transformation_before_component(component.id, optimization)


    def add_transformation_before_component(self, current_component_id: str, transformation: Transform) -> None:
        self.components.append(transformation)

        if not value_in_dependencies(self.dependencies, current_component_id):
            raise Exception(f"component {current_component_id} not found in dependencies")

        new_dependencies = []

        for dependency in self.dependencies:
            if dependency[1] == current_component_id:
                new_dependencies.append((dependency[0], transformation.id))
                new_dependencies.append((transformation.id, dependency[1]))
            else:
                new_dependencies.append(dependency)

        self.dependencies = new_dependencies



    def add_transformation_after_component(self, current_component_id: str, transformation: Transform) -> None:
        self.components.append(transformation)

        if not value_in_dependencies(self.dependencies, current_component_id):
            raise Exception(f"component {current_component_id} not found in dependencies")

        new_dependencies = []

        for dependency in self.dependencies:
            if dependency[0] == current_component_id:
                self.dependencies.append((transformation.id, dependency[1]))
            else:
                new_dependencies.append(dependency)

        self.dependencies = new_dependencies

        self.dependencies.append((current_component_id, transformation.id))

    def to_yaml(self, path: str) -> None:
        templates: list[dict] = []
        tasks: list[dict] = []

        for component in self.components:
            image = IMAGE_PREFIX.format(name=component.type)
            component.env_details[ENV_SCHEMA] = str(self.schema_mapping)

            if isinstance(component, Extract):
                component.env_details[ENV_OUT_FOLDER] = OUT_PATH
                templates.append(get_template(None, component.type + component.id, image, component.env_details, {'output': OUT_PATH}))

                tasks.append(get_task(component.id,
                                      component.type + component.id,
                                      [],
                                      None,
                                      None))
                continue

            if isinstance(component, Transform):
                component.env_details[ENV_OUT_FOLDER] = OUT_PATH
                component.env_details[ENV_IN_FOLDER] = IN_PATH
                templates.append(get_template({'input': IN_PATH}, component.type + component.id, image, component.env_details, {'output': OUT_PATH}))

            if isinstance(component, Load):
                component.env_details[ENV_IN_FOLDER] = IN_PATH
                templates.append(get_template({'input': IN_PATH}, component.type + component.id, image, component.env_details, None))


            dependencies: list[str] = []
            for dependency in self.dependencies:
                if dependency[1] == component.id:
                    dependencies.append(dependency[0])

            tasks.append(get_task(component.id,
                                  component.type + component.id,
                                  dependencies,
                                  {'input': FROM_ARTIFACT_PREFIX.format(name=dependencies[0])},
                                  None
                                  ))

        workflow = get_workflow(self.name, tasks, templates)

        dump_yaml(workflow, path)