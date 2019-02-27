'''
    Unit tests for the workflow that test:
    * process_sample()
    * correct formatting and values in WORKFLOW_CONFIG
    * correct foramtting and values in workflow.parameters
'''
from os import getcwd
from os.path import join, isfile
from shutil import copyfile
import json
import subprocess
import tempfile

from helpers import fake_args, check_group_format


def test_workflow_singularity_url():
    '''
        Confirm singularity image url is in the config
    '''
    from process import WORKFLOW_CONFIG
    assert WORKFLOW_CONFIG['singularity_url'] != None

def test_workflow_output_type():
    '''
        Confirm output type exists in config and is supported
    '''
    from process import WORKFLOW_CONFIG
    assert WORKFLOW_CONFIG['output_type'] in ['csv','file']

def test_workflow_api_version():
    '''
        config api version is in config and is a supported value
    '''
    from process import WORKFLOW_CONFIG
    assert WORKFLOW_CONFIG['api_version'] >= 0.1

def test_parameter_formatting():
    from workflow import parameters

    for group in parameters:
        check_group_format(group)

def test_process_sample(tmp_path,fake_args):
    '''
        Test processing a sample. process_sample is run just like it will be
        in production. That is, inside the singularity container
        at WORKFLOW_CONFIG['singularity_url'].

        This test passes if:
         * process_sample completes with a run code of 0
         * A results file is created
    '''
    from process import process_sample, WORKFLOW_CONFIG

    sample_name = 'Fake'
    sample_path = join(tmp_path,'fake_sample')

    #Copy a file into fake_sample to get a better test
    copyfile(join(getcwd(),'tests','sample','R13-2-tubers.jpg'),sample_path)

    with open(join(tmp_path,'params.json'),'w') as fout:
        args = {
            'sample_path': sample_path,
            'sample_name': sample_name,
            'args': fake_args
        }
        json.dump(args,fout)

    ret = subprocess.run(["singularity",
                          "exec",
                          "--containall",
                          "--home", tmp_path,
                          "--bind", "%s:/user_code/"%(getcwd()),
                          "--bind", "%s:/bootstrap_code/"%(join(getcwd(),'tests')),
                          "--bind", "%s:/results/"%(tmp_path),
                          WORKFLOW_CONFIG['singularity_url'],
                          "python3", "/bootstrap_code/bootstrapper.py"
                         ],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    print(ret.stdout)
    print(ret.stderr)

    assert ret.returncode == 0
    assert isfile(join(tmp_path,'result.file'))
