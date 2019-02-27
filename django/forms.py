from workflows.forms import CreateJob
from .. import workflow

class CreateJobForm(CreateJob):
    parameters = workflow.parameters
