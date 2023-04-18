import json

def verifyLabel(label):
    '''The label should be string. This is the nodeLabel/nodeType
    returns label with modifications if required.'''
    if not isinstance(label, str):
        raise TypeError("label should be of type str")
    return label

def verifyAttributeProperties(properties):
    '''properties of attribute should be of type list.
    returns properties with modifications if required.'''
    if not isinstance(properties, list):
        raise TypeError("properties of attribute should be of type list.")
    #TODO
    return properties

def verifyAttributes(attributes):
    '''attributes should be of type dict. These are the node attributes.
        {
            "nameOfAttribute" : list(properties of attribute)
        }
        returns: attributes with modifications if needed.
    '''
    if not isinstance(attributes, list):
        raise TypeError("attributes should be of type list")
    result = []
    for attribute in attributes:
        result.append(verifyAttributeProperties(attribute))
    return result

def verifyNodeProperties(nodeProps):
    '''NodeProperties should be of type dict.
    These are the meta properties of the node like degree, neighbours, etc'''
    if not isinstance(nodeProps, dict):
        raise TypeError('NodeProperties should be of type dict')
    #TODO: check if valid
    return nodeProps


def verifyNode(node):
    '''node: a dict type.
    node dict should have:
        nodeLabel:<str>;
        <dict>: Attributes;
        <dict>: NodeProperties;
        <dict>: AttributeRelations;
    in the same order.
    returns: verified node, with minor modifications if needed.'''
    if not isinstance(node, dict):
        raise TypeError("node should be of type python dict.")
    NodeLabel = verifyLabel(node['NodeLabel'])
    Attributes= verifyAttributes(node['Attributes'])
    NodeProperties = verifyNodeProperties(node['NodeProperties'])

    return {"NodeLabel":NodeLabel, 'Attributes':Attributes, "NodeProperties":NodeProperties}


def verifySchema(nodesList):
    '''
    nodesList: A list of json dict, where each dict represents a node schema.
    returns: verified nodeList, with minor modifications in it if needed.
    '''
    if not isinstance(nodesList, list):
        raise TypeError("nodesList should be of type python list.")

    rectifiedList = []
    for node in nodesList:
        rectifiedList.append( verifyNode(node))
    return rectifiedList



def extractSchema(jsonString, verify=True):
    '''Given a jsonString, extracts schema for PyNe.
    jsonString should confirm to standard json format.
    Returns: A list of nodes schemas as dicts.
    '''
    #TODO: Check if jsonString is tooo large or smth. Vulnerability: might stall/crash program.
    parsedJson = json.loads(jsonString)
    if verify:
        parsedJson = verifySchema(parsedJson)
    return parsedJson
