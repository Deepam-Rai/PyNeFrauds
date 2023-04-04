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
    if isinstance(constr, str): #regex
        constr = ''.join([e for e in constr if e!=''])
        if len(constr)>0:
            return constr
    if isinstance(constr, list): #list
        constr = [e for e in constr if e!='']
        if len(constr)>0:
            return constr
    if isinstance(constr, dict): #range
        constr = {k:v for k,v in constr.items() if v.isdecimal()}
        if bool(constr):
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
        if tent['type']=="relationship":
            tent['source']=entity['source']
            tent['dest']=entity['dest']
        tattrs = []
        for specs in entity['Attributes']:
            # specs = entity['Attributes'][attr]
            attr = specs[0][0]
            prefix = specs[1][0]
            constr = rectifyConstraint(specs[1][1])
            if constr is not None:
                tattrs.append([attr,prefix,constr])
        tent['Attributes'] = tattrs
        tent['NodeProperties']={}
        tlist.append(tent)
    query = all_in_one_query(tlist) 
    return {'CYPHER':query}
