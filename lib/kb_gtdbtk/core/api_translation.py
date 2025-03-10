'''
Functions to translate values between the SDK API and core app logic.
'''

from typing import Dict, NamedTuple as _NamedTuple, cast as _cast


class GTDBTKParams(_NamedTuple):
    '''
    Parameters for running GTDB-tk in the KBase environment.
    '''

    ref: str
    ''' The workspace object reference in the x/y/z form. '''

    workspace_id: int
    ''' The ID of the KBase workspace where the report should be saved. '''

    min_perc_aa: float
    ''' The mimimum sequence alignment in percent. '''

    overwrite_tax: int
    ''' Boolean to decode wheter to overwrite an existing Taxonomy field in input Genome. '''


def get_gtdbtk_params(input_params: Dict[str, object]) -> GTDBTKParams:
    '''
    Process input parameters supplied to the GTDB-tk run method and parse them into
    a named tuple. The expected fields are:

    input_object_ref: a workspace reference to the input object that will be processed in the
        x/y/z form.
    workspace_id: the integer ID of the workspace where the results will be saved.
    min_perc_aa: the minimum sequence alignment as a percent.

    :param input_params: the input parameters passed to the method.
    :returns: the parsed parameters.
    :raises ValueError: if any of the parameters are invalid.
    '''
    ref = input_params.get('input_object_ref')
    if not ref:
        # for backwards compatibility
        ref = input_params.get('inputObjectRef')
    if type(ref) != str:
        raise ValueError('input_object_ref is required and must be a string')
    # could check ref format, but the ws will do that for us. YAGNI.

    min_perc_aa = input_params.get('min_perc_aa', 10)
    if type(min_perc_aa) != float and type(min_perc_aa) != int:
        raise ValueError('min_perc_aa must be a float')
    # TODO check 0 <= min_perc_aa <= 1

    wsid = input_params.get('workspace_id')
    if type(wsid) != int or _cast(int, wsid) < 1:
        raise ValueError('workspace_id is required and must be an integer > 0')

    overwrite_tax = int (input_params.get('overwrite_tax', 0))
    if type(overwrite_tax) != int or (overwrite_tax != 0 and overwrite_tax != 1):
        raise ValueError('overwrite_tax is required and must be an integer [0,1]')

    
    return GTDBTKParams(_cast(str, ref), _cast(int, wsid), _cast(float, min_perc_aa) * 1.0, _cast(int, overwrite_tax))
