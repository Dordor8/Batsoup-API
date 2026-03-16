from src.metadata_handler.workflow_interpreter.interpreter import Workflow
from src.routes.route import Destination


w = Workflow('my-channel', 'idk', 'json', {}, 0, 0, False,
             'kafka-reader', {'SERVERS': 'kafka.com'},
             [Destination(destination_type='s3-writer', destination_connection_details={'SERVERS': 's3.com'})], True)


w.to_yaml('test.yaml')