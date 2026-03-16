from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

TEMPLATE_PATH = 'src/metadata_handler/workflow_creator/resources/templates/template-template.yaml'
TASK_PATH = 'src/metadata_handler/workflow_creator/resources/templates/task-template.yaml'
WORKFLOW_PATH = 'src/metadata_handler/workflow_creator/resources/templates/workflow-template.yaml'
MAIN_TEMPLATE_NAME = 'main'
DEFAULT_COMMAND = 'python'
DEFAULT_ARGS = 'main.py'

yaml = YAML()

def get_template(input_artifacts: dict[str, str] | None,
                 name: str,
                 image: str,
                 env_variables: dict[str, str],
                 output_artifacts: dict[str, str] | None,
                 command: str = DEFAULT_COMMAND,
                 args: str = DEFAULT_ARGS,
                ) -> dict:

    with open(TEMPLATE_PATH, "r") as template_file:
        content = yaml.load(template_file)

    if input_artifacts:
        content['inputs'] = {}
        content['inputs']['artifacts'] = [{'name': key, 'path': value} for key, value in input_artifacts.items()]

    content['name'] = name
    content['container']['image'] = image
    content['container']['command'] = [command]
    content['container']['args'] = [DoubleQuotedScalarString(args)]

    if env_variables:
        content['container']['env'] = [{'name': key, 'value': DoubleQuotedScalarString(value)} for key, value in env_variables.items()]

    if output_artifacts:
        content['outputs'] = {}
        content['outputs']['artifacts'] = [{'name': key, 'path': value} for key, value in output_artifacts.items()]

    return content

def get_task(name: str, template: str, dependencies: list[str], artifacts: dict[str, str] | None, when: str | None) -> dict:
    with open(TASK_PATH, "r") as task_file:
        content = yaml.load(task_file)

    content['name'] = name
    content['template'] = template
    content['dependencies'] = [DoubleQuotedScalarString(dependency) for dependency in dependencies]

    if artifacts:
        content['arguments'] = {}
        content['arguments']['artifacts'] = [{'name': key, 'from': DoubleQuotedScalarString('{{' + value + '}}')} for key, value in artifacts.items()]

    if when:
        content['when'] = DoubleQuotedScalarString(when)

    return content

def get_workflow(name: str, tasks: list[dict], templates: list[dict]) -> dict:
    with open(WORKFLOW_PATH, "r") as workflow_file:
        content = yaml.load(workflow_file)

    content['metadata']['generateName'] = name + '-'
    for template in templates:
        content['spec']['templates'].append(template)

    for template in content['spec']['templates']:
        if template['name'] == MAIN_TEMPLATE_NAME:
            for task in tasks:
                template['dag']['tasks'].append(task)
            break

    return content

def dump_yaml(content: dict[str, str], path: str):
    with open(path, "w") as yaml_file:
        yaml.dump(content, yaml_file)