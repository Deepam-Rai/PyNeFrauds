# connects gui with the PyNe codes

# receives gui input; creates queries using codes; returns to gui

import json

#TODO pip install PyNeFrauds and then import
import sys
import os
PyNe = os.path.dirname(os.path.realpath('../PyNeFrauds'))
sys.path.append(PyNe)
from PyNeFrauds.Constructor import all_in_one_query


def rectifyConstraint(constr):
    # returns constr modified if required
    print(type(constr))
    if isinstance(constr, str): #regex
        if len(constr)>0:
            return constr
    if isinstance(constr, list): #list
        constr = [e for e in constr if e!='']
        if len(constr)>0:
            return constr
    if isinstance(constr, dict): #range
        constr = {k:v for k,v in constr.items() if v.isdecimal()}
        if bool(constr):
            print(constr)
            return constr
    return None

def gui_input_to_schema(input):
    # transform to accepted form
    tlist = []
    for entity in input:
        tent = {}
        tent['NodeLabel'] = entity['label']
        tent['ref'] = entity['ref']
        tent['type'] = entity['type']
        tattrs = {}
        for attr in entity['Attributes']:
            specs = entity['Attributes'][attr]
            prefix = specs[0]
            constr = rectifyConstraint(specs[1])
            if constr is not None:
                tattrs[attr] = [prefix,constr]
        tent['Attributes'] = tattrs
        tent['NodeProperties']={}
        if (len(tent['Attributes'])>0):
            # append only if some constraint really exists
            tlist.append(tent)
    query = all_in_one_query(tlist) 
    return {'CYPHER':query}
