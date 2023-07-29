import re
import pandas as pd
from .Globals import neo4jHandler


def type_mapper(pandasTypes):
    """
    Parameter:
        pandasType: list datatype in pandas.
    Returns:
        neoTypes: list of corresponding suitable neo4j datatypes parser when creating entities.
        ['toString, toInteger, datetime,...']
    """
    typeMap = {
        'object':'toString',
        'datetime':'datetime',
        'M8': 'datetime',
        'int': 'toInteger',
        'float':'toFloat',
        'O':'toString',
    }
    neoTypes = []
    for e in pandasTypes:
        for PType in typeMap:
            if PType.lower() in e.lower():
                neoTypes.append(typeMap[PType])
                break
    return neoTypes


def node(identifier, nodeType, attributes, values, attrTypes=None, typeParser=True):
    """
    Parameters:
        identifier: Temporary unique name given to each node during creation; easier to refer it later(in the same command).
        nodeType: NodeLabel
        attributes: Node attribute names
        values: values for the corresponding node attributes
        attrTypes: toFloat, toInteger, toString, toBoolean; for corresponding attributes,
        typeParser: If True then adds toInteger(), toString(), etc to property values
            Keep True for creating nodes, False for matching nodes
    Returns:
        (identifier:nodeType {attribute: attrType(values)...}) - a node in CYPHER query
    NULL/nan/.. properties are not considered.
    **Creates copy of dataframe.**
    """
    if attrTypes is None:
        attrTypes = [None]*len(attributes)
    cmd = '(' + str(identifier) + ':' + str(nodeType) + '  { '
    for attr, val, typ in zip(attributes, values, attrTypes):
        if not pd.isnull(val):
            cmd += ' , ' + str(attr) + ':'
            if typeParser and typ:
                cmd += str(typ)
            cmd +='('
            if typ in ['toString','datetime','quote']:
                cmd += '"'
            cmd += str(val)
            if typ in ['toString','datetime','quote']:
                cmd += '"'
            cmd +=') '
    cmd += ' })'
    return cmd


def create_nodes(df, cols, nodeLabel, unique=False, execute=False, cmds=True):
    """
    Parameters:
        df: dataframe,
        cols: list of cols that are attributes of this node label,
        <str> nodeLabel: NodeLabel,
        <bool> unique: default: False; If true then df[cols].drop_duplicates(),
        <bool> execute: If True, then cypher queries run on neo4j database,
        <bool> cmds: If True then returns list of commands.
    Returns:
        If cmds=True then returns list of cypher commands else None.
    """
    tmp = df[cols].copy()
    if unique:
        tmp = tmp.drop_duplicates(ignore_index=True)

    # column types in pandas; attribute type in neo4j
    colTypes = [dtyp.name for dtyp in tmp.dtypes.tolist()]
    neoTypes = type_mapper(colTypes)
    # if there is datetime column; extract just the date
    for i in range(len(cols)):
        if neoTypes[i] == 'datetime':
            tmp[cols[i]] = pd.to_datetime(df[cols[i]]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    cypher_cmds = []
    for idx, row in tmp.iterrows():
        cmd = 'CREATE ' + node(
            identifier='',
            nodeType=nodeLabel,
            attributes=[re.sub(r'[^a-zA-Z0-9]', '_', col).lower() for col in cols],
            values=[row[col] for col in cols],
            attrTypes=neoTypes
        )
        if execute:
            neo4jHandler.query(query=cmd)
        if cmds:
            cypher_cmds.append(cmd)
    return cypher_cmds if cmds else None


def __rels_validate(nodes, rels):
    """Checks if all the end node types of rels actually exists in nodes or not."""
    for rel, endVs in rels.items():
        for endV in endVs:
            if endV not in nodes:
                raise TypeError(f'"{endV}" NodeLabel is not present in given nodes, for relationship "{rel}".')


def create_relations(df, nodes, rels, execute=False, cmds=True):
    """
    Parameters:
        df: pandas dataframe,
        nodes: a dict of format: { 'NodeLabel':[list of primary key columns for this nodeLabel in df],...},
        rels: a dict of format: {'RelationName': [sourceNodeLabel, destNodeLabel], ...}
        execute: <boolean> default False; if true then commands are executed on neo4j database,
        cmds: <boolean> default True; returns list of create relationship CYPHER commands.
    Returns:
        returns list of create relationship CYPHER commands if 'cmds' is True else None.
    """
    __rels_validate(nodes, rels)
    tmp = df
    # column types in pandas; attribute type in neo4j
    colTypes = [dtyp.name for dtyp in tmp.dtypes.tolist()]
    neoTypes = type_mapper(colTypes)
    neoTypes = {df.columns[i]: neoTypes[i] for i in range(len(neoTypes))}

    cypher_cmds=[]
    for idx, row in tmp.iterrows(): #for each row of df
        cmd = 'MATCH '
        # Match all node types
        for nodeLabel, keys in nodes.items():
            attrTypes = [neoTypes[col] for col  in keys]
            cmd += '\n\t' + node(
                    identifier = nodeLabel+str(idx),
                    nodeType = nodeLabel,
                    attributes= [re.sub(r'[^a-zA-Z0-9]', '_', col).lower() for col in keys],
                    values = [row[col] for col in keys],
                    attrTypes = attrTypes, #['quote']*len(keys),
                    typeParser = False
            )+","
        cmd = cmd[:-1] #remove last comma
        #set all relations
        for rel, ends in rels.items():
            cmd += f'\nCREATE ({ends[0]+str(idx)})-[:{rel.upper()}]->({ends[1]+str(idx)})'
        if execute:
            neo4jHandler.query(query=cmd)
        if cmds:
            cypher_cmds.append(cmd)
    return cypher_cmds if cmds else None

def create_nodes_and_relations(df,nodes=None, rels=None, rel_execute=True, rel_cmds=False):
    """
    Parameters:
        df: dataframe,
        nodes: a dictionary of nodes as dictionary of format:
        {
            nodeLabel:{
                'cols':[relevant columns from df],       #forms attributes of the nodes
                'primary_key':[relevant columns from df],
                'unique':boolean,  #whether each node should be unique or not
                'execute':boolean, #whether to execute the commands or not
                'cmds':boolean     #to return the commands(as list) or not
        },
        ...}
        rels: relations to be created of format:
        {
            relationName : [startingNodeLabel, endingNodeLabel],
            ...
        }
        rel_execute: boolean: whether to execute relation commands or not
        rel_cmds: boolean: whether to return relation commands as list or not
    """
    node_cmds = []
    rel_cmds_exe = []
    if nodes is not None:
        for nodeLabel, specs in nodes.items():
            cmds = create_nodes(
                df = df,
                cols = specs["cols"],
                nodeLabel= nodeLabel,
                unique = specs["unique"],
                execute= specs["execute"],
                cmds = specs["cmds"]
            )
            node_cmds.append(cmds)
    if rels is not None:
        nodes_used=[]
        for rel, specs in rels.items():
            # nodes_used.extend(specs['ends'])
            nodes_used.extend(specs)
        nodes_used = set(nodes_used)
        rel_nodes = {}
        for x in nodes_used:
            rel_nodes[x] = nodes[x]['primary_key']
        # rel_nodes
        rel_cmds_exe = create_relations(df, rel_nodes, rels, execute=rel_execute, cmds=rel_cmds)
    return node_cmds, rel_cmds_exe