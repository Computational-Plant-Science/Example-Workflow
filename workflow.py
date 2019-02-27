from workflows import registrar

# Registers the workflow with the webserver
# These values should not need changed.
name = "Count Objects"
description = "Counts the objects in the image that are above a size threshold"
icon_loc = "workflows/count_objects/icon.png"
registrar.register(name,description,"count_objects",icon_loc)

#Defines the arguments that are passed to process_sample.
#See docs for more details
parameters = [
    {
        #unique group name, must be a valid python variable name
        'id': 'settings',

        #Human readable name, shown in website UI
        'name': 'Workflow Settings',

        #A list of parameters within this group. These are converted to
        # fields in the website UI. Each parameter is represented by a
        # python dictionary.
        'params':[
            {
                #unique parameter name, must be a valid python variable name
                'id': 'size_threshold',

                #Type of value this field will handle
                #Valid types are: bool, float, and int
                'type': 'int',

                #Initial value the field will have.
                #Must be compatible with the type of field
                'initial': 1200,

                #Human readable name, shown in website UI
                'name': 'Size Threshold',

                #A human readable description of what this parameter does
                #shown to the users in the website UI
                'description': 'Only objects above this threshold (in pixels) will be counted.'
            },
            {
                #A second parameter
                'id': 'thresh_multiplier',
                'type': 'float',
                'initial': 1.0,
                'name': 'Threshold Level',
                'description': 'Adjust the background threshold'
            }
        ]
    }
]
