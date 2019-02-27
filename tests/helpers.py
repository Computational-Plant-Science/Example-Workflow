'''
    Functions that support the unit tests
'''
import pytest

def parse_group(group):
    '''
        Convert workflow.parameters to a dictionary of arguments for
        process_sample

        Args:
            group (dict): one group from the workflow.parameter list
    '''
    dict = {}

    if 'params' in group.keys():
        p = {}
        for param in group['params']:
            p[param['id']] = param['initial']
        dict['params'] = p
    if 'groups' in group.keys():
        dict['groups'] = {}
        for g in group['groups']:
            dict['groups'][g['id']] = parse_group(g)

    return dict

@pytest.fixture
def fake_args():
    '''
        Generate a default set of parameters to pass to process_sample
    '''
    from workflow import parameters

    args = {}
    for group in parameters:
        args[group['id']] = parse_group(group)

    return args

def check_param_format(p):
    '''
        Checks the formatting of a parameter within the workflow.parameter groups

        Args:
            p (dict): one parameter
    '''
    assert 'name' in p.keys(), "parameter %s must include a name"%(p['name'])
    assert isinstance(p['name'],str), "%s: name must be a string"%(p['name'])

    assert 'description' in p.keys(), 'parameter %s must include a description'%(p['name'])
    assert isinstance(p['description'],str), "%s: description must be a string"%(p['name'])

    assert 'id' in p.keys(), '%s: parameter must include an id'%(p['name'])
    assert isinstance(p['id'],str), "%s: id must be a string"%(p['name'])
    assert p['id'].isidentifier(), "%s: id must be valid python variable name"%(p['name'])

    assert 'type' in p.keys(), "parameter %s must include a type"%(p['name'])
    assert isinstance(p['type'],str), "%s type must be a string"%(p['name'])
    assert p['type'] in ['bool','float','int'], "%s type must be float, bool, or int"%(p['name'])

    assert 'initial' in p.keys(), "parameter must include an initial value"
    if p['type'] == 'float':
        assert isinstance(p['initial'],float), "%s initial value must be a float"%(p['name'])
    if p['type'] == 'int':
        assert isinstance(p['initial'],int), "%s initial value must be an int"%(p['name'])
    if p['type'] == 'bool':
        assert isinstance(p['initial'],bool), "%s initial value  must be a bool"%(p['name'])

def check_group_format(group):
    '''
        Checks for correct formatting of workflow.parameter groups

        Args:
            group (dict): one group from the workflow.parameter list
    '''
    assert 'id' in group.keys()
    assert 'name' in group.keys()

    if 'params' in group.keys():
        for param in group['params']:
            check_param_format(param)

    if 'groups' in group.keys():
        for g in group['groups']:
            check_group_format(g)
