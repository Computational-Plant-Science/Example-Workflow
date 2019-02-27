'''
    The code to run the workflow code on a sample
'''

'''
    WORKFLOW_CONFIG: Configuration information used to run process_sample

    singularity_url: the url to the singularity container in which to run
        process_sample(). The provided singularity container must have
        python3 installed. And it must be executable using the
        'python3' command.

    output_type: the type of output returned by process_sample. Supported types
        are csv and file. See the "Returns" section of process_sample for
        more details.

        if set to csv:
            A csv file containing the values from each process_sample runs
            is returned as the workflow result

        if set to file:
            The files return by each process_sample run
            are zipped and returned as the workflow result.

    api_version: The cluster side api version that this workflow requires.
        Provided for future compatibility. Currently, the only valid version
        is 0.1.
'''
WORKFLOW_CONFIG = {
    'singularity_url': "shub://frederic-michaud/python3",
    'output_type': 'csv',
    'api_version': 0.1,
}

def process_sample(name,path,args):
    from skimage.measure import regionprops
    from skimage import io
    from skimage.morphology import closing, square
    from skimage.filters import threshold_otsu
    from skimage.segmentation import clear_border
    from skimage.measure import label
    
    '''
        Process a sample within the collection.

        This function is run within the singularity container defined in
        the WORKFLOW_CONFIG using the python3 interpreter.

        Args:
            name (str): name of the sample
            path (str): path to the sample file(s)
            args (dict): workflow parameters

        Returns:
            If  WORKFLOW_CONFIG['output_type'] == 'file'
                then a path to the file to include in the results should
                be returned.

            If WORKFLOW_CONFIG['output_type'] == 'csv"
                a python dictionary should be returned with the key being the
                csv column header and the value being the value being the csv
                row value.
                All process_samples calls must return the same key set.
                (i.e. the same csv rows.).
    '''
    settings = args['settings']['params']

    image = io.imread(path,as_gray=True)

    # apply threshold
    thresh = threshold_otsu(image)
    bw = closing(image > (thresh * settings['thresh_multiplier']), square(3))

    # remove artifacts connected to image border
    cleared = bw.copy()
    clear_border(cleared)

    # label image regions
    label_image = label(cleared)
    regions = regionprops(label_image)

    valid_regions = [region for region in regions if region.area > settings['size_threshold']]

    return {
        'regions': len(valid_regions)
    }
