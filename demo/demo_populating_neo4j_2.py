############# to remove
import os
import sys
lib_path = os.path.join(os.getcwd(), "../PyNeFrauds")
sys.path.append(lib_path)
#############

import pandas as pd
# from PyNeFrauds.Neo4jHandler import Neo4jHandler
from PyNeFrauds.PyNeFrauds.Globals import neo4jHandler
from PyNeFrauds.PyNeFrauds.neo4j_populator import create_nodes, create_relations, create_nodes_and_relations

print("Setting up the neo4j handler...")
host = 'bolt://localhost:7687'
user = "neo4j"
password = "password"
querer = neo4jHandler.set_credentials(host, user, password)

# example data
df = pd.read_excel('./demo_data_medical.xlsx')
print("Data Read.")

# populating neo4j
execute = True
cmds = True

nodes = { #nodes to be created
    'Patient':{   #node label
        'cols':['Patient Name','Patient Age'],  #columns from df, that will become attributes of the node
        'primary_key':['Patient Name'],
        'unique':True,   # is each instance unique?
        'execute':execute,  #boolean, whether to execute the commands or not
        'cmds':cmds      #boolean, whetehr to return the commands as list or not
    },
    'Doctor':{
        'cols':['Doctor Name','Doctor ID'],
        'primary_key':['Doctor ID'],
        'unique':True,
        'execute':execute,
        'cmds':cmds
    },
    'Problem':{
        'cols':['Problem'],
        'primary_key':['Problem'],
        'unique':True,
        'execute':execute,
        'cmds':cmds
    }
}

rels = { #relations to be created
    'VISITS': ['Patient','Doctor'],   #relation label : [startNode, endNode]
    'TREATS': ['Doctor','Problem'],
    'HAS': ['Patient', 'Problem']
}

commands_executed = create_nodes_and_relations(
    df=df,       # dataframe
    nodes=nodes, # nodes to be created
    rels=rels,    # relations to be created
    rel_execute=True, #to execute the relation commands?
    rel_cmds= True  #to return the relation commands?
)

print("Completed.")
