from enum import Enum


class ConstrType(Enum):
    NONE = None
    LIST = 0
    RANGE = 1
    REGEX = 2


# START functions for constructing conditions

def mergeNodeConditions(queries, nRef, nLabel):
    '''queries: dict { priority level : list of sub-queries}
    nRef: node reference to use in query
    nLabel: node label
    Merges for each level and 
    returns a query for each priority level
    '''
    merged = {}
    for level in queries:
        query = ' OR '.join(queries[level])
        merged[level] = query
    return merged


def constrType(restraint):
    '''Identify its type: range, regex, list, etc
    Accepted types:
    list -> list
    dict -> numerical range
    str -> regex
    #TODO more detailed checks: range has min,max?
    '''
    if isinstance(restraint, list):
        return ConstrType.LIST
    if isinstance(restraint, dict):
        return ConstrType.RANGE
    if isinstance(restraint, str):
        return ConstrType.REGEX
    return ConstrType.NONE


def constrQuery(preCondition, restraint, nRef, aRef):
    '''
    preCondition: "IS", "IS NOT", "IN", "NOT IN".
    restraint: constraint
    nRef: Node reference to use in query
    aRef: attribute name
    Identifies what kind of restraint it is.
    Constructs query for it.
    Returns: CYPHER query for this restraint.'''
    typ = constrType(restraint)
    if 'NOT' in preCondition.split():
        query = " NOT "
    else:
        query = ""
    query += "("+nRef+"."+aRef
    if typ == ConstrType.LIST:
        query += " IN " + str(restraint)
    elif typ == ConstrType.RANGE:
        query += f' {list(restraint.keys())[0]} {list(restraint.values())[0]} '
        if len(restraint) > 1:
            query += f' AND {nRef}.{aRef} '
            query += f'{list(restraint.keys())[1]} {list(restraint.values())[1]} '
    elif typ == ConstrType.REGEX:
        query += " =~ '" + restraint + "'"
    else:
        query = ""
    query += ')'
    return query


def constrNodeCond(node, nRef='n'):
    '''node: a node's schema
    nRef: node reference to use in queries
    Construct queries for a node.
    Returns:
    {
        level : [list of queries],
        .
        .
    }'''
    queries = {}

    def addQuery(query, level):
        if level in queries:
            queries[level].append(query)
        else:
            queries[level] = [query]
    # Construct queries for attributes
    for idx in node['Attributes']:
        attr, preCondition, restraint = idx[:3]
        # set default value of 1
        restrLevel = 1 if len(idx) < 4 else idx[-1]
        query = constrQuery(preCondition, restraint, nRef, attr)
        addQuery(query, restrLevel)

    # TODO Construct queries for nodeProperties

    query = mergeNodeConditions(
        queries=queries, nRef=nRef, nLabel=node['NodeLabel'])
    return query

################################ END condition Constructing functions #########################


def constrNodeQueries(nodeTests, nRef):
    '''<dict> nodeTests: tests on the node attributes
    <str> nRef: node reference to use in query
    returns: {level : query} for every level in dict nodeTests'''
    queries = {}
    for level in nodeTests:
        query = f'MATCH ({nRef}) \n WHERE '
        query += nodeTests[level]
        query += f' \nRETURN {nRef} \n'
        queries[level] = query
    return queries


def constructQueries(jsonSchema, mode='STREAM'):
    '''
    jsonSchema: node schema for whole graph.
    mode: #TODO
        STREAM = displays the nodes who fail conditions on the browser,
        WRITE = Sets a node property according to the evaluation of condition
    returns queries for nodes.
    '''
    queries = {}
    for node in jsonSchema:
        nRef = 'n'
        nodeTests = constrNodeCond(node, nRef=nRef)
        nodeQueries = constrNodeQueries(nodeTests, nRef=nRef)
        queries[node['NodeLabel']] = nodeQueries
    return queries


def all_in_one_query(entityList):
    if len(entityList) == 0:
        return ""
    # json input to queries
    finalQuery = ''
    for ent in entityList:
        # match the entity
        if ent['type'] == 'node':
            query = f'\nMATCH ({ent["ref"]}:{ent["NodeLabel"]})'
        elif ent['type'] == 'relationship':
            query = f'\nMATCH ({ent["source"]})-[{ent["ref"]}:{ent["NodeLabel"]}]-({ent["dest"]})'
        # where properties : conditions
        if len(ent['Attributes']) > 0:
            entTests = constrNodeCond(ent, nRef=ent['ref'])
            query += "\n  WHERE " + entTests[1]
        finalQuery += "\n"+query
    finalQuery = finalQuery[2:] + f'\n\nRETURN {entityList[0]["ref"]}'
    for ent in entityList[1:]:
        finalQuery += f', {ent["ref"]}'
    # return all refs
    return finalQuery
