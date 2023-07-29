############# to remove
import os
import sys
lib_path = os.path.join(os.getcwd(), "../PyNeFrauds")
sys.path.append(lib_path)
#############

import pandas as pd
from ..PyNeFrauds.PyNeFrauds.Globals import neo4jHandler
from ..PyNeFrauds.PyNeFrauds.neo4j_populator import create_nodes, create_relations

print("Setting up the neo4j handler...")
host = 'bolt://localhost:7687'
user = "neo4j"
password = "password"
querer = neo4jHandler.set_credentials(host, user, password)

# example data
df = pd.read_excel('./demo_data_medical.xlsx')
print("Data Read.")

# populating neo4j
print("Creating Patient nodes.")
cols = ["Patient Name","Patient Age"] #taking only selected columns
commands_executed = create_nodes(
    df = df,
    cols = cols,
    nodeLabel= "Patient", #node types in neo4j
    unique=True, #duplicate nodes are not made, even if present in df
    execute=True, #execute the commands
    cmds=True #return the commands
)

print("Creating Doctor nodes.")
cols = ["Doctor Name","Doctor ID"] #taking only selected columns
commands_executed = create_nodes(
    df = df,
    cols = cols,
    nodeLabel= "Doctor", #node types in neo4j
    unique=True, #duplicate nodes are not made, even if present in df
    execute=True, #execute the commands
    cmds=True #return the commands
)

print("Creating Problem nodes.")
cols = ["Problem"] #taking only selected columns
commands_executed = create_nodes(
    df = df,
    cols = cols,
    nodeLabel= "Problem", #node types in neo4j
    unique=True, #duplicate nodes are not made, even if present in df
    execute=True, #execute the commands
    cmds=True #return the commands
)

print("Creating relationships.")
rel_nodes = {   #nodes involved in relevant relationships
    "Patient":["Patient Name","Patient Age"],   #nodeLabel : [primary keys]
    "Doctor":["Doctor Name","Doctor ID"],
    "Problem":["Problem"]
}

rels = { #relations to be created
    "VISITS":["Patient","Doctor"],  #relation label : [startingNode, endingNode]
    "TREATS":["Doctor","Problem"],
    "HAS":["Patient","Problem"]
}

commands_executed = create_relations(
    df=df,              # dataframe
    nodes= rel_nodes,   # nodes involved in relationships
    rels = rels,    # the relationships
    execute=True,   # to execute or not
    cmds=False      # to return the executed commands or not
)
print("Completed.")