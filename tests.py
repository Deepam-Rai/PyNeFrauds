# from PyNeFrauds.Globals import neo4jHandler
import PyNeFrauds
import PyNeFrauds.QueryConstructor as QueryConstructor
from PyNeFrauds.nn import EmbedFetcher
from PyNeFrauds.nn import PyGData
# from PyNeFrauds.Constructor import testFun
# from PyNeFrauds.extractor import verifyAttributeProperties


# does not allow duplicate keys - attributes
# change to array of dicts.
json_text = '''
[{
  "NodeLabel" : "Patient",
  "ref" : "n0",
  "type" : "node",
  "Attributes" : [
    ["Name", "IS NOT OF", "w"],
    ["Contact", "IS", {">" : 9999999999}],
    ["Age", "IS NOT", {"<=":130}],
    ["asdf", "IS", {"<":23, ">=":"n1.Cost"}],
    ["ID", "IS NOT", {"<":0}],
    ["Gender", "NOT IN", ["Male","Female","Others"]]
  ],
  "NodeProperties" : {}
},
{
  "NodeLabel" : "Treatment",
  "ref" : "n1",
  "type" : "node",
  "Attributes" : [
    ["Name", "IS OF", "w"],
    ["Cost", "IS", {"=":5000}],
    ["asdf", "IS", {"<":23, ">=":14}],
    ["ID", "IS", {"<":0}],
    ["Category", "IN", ["Oncology","Pediatrics"]]
  ],
  "NodeProperties" : {}
}]
'''


# print(PyNeFrauds.Globals.neo4jHandler.get_credentials())

# cone = QueryConstructor(json_text)
# print(cone.queries)
# print(cone.queries['Patient'][1])
# cone.constructQueries(mode='MERGED')
# cone.showQueries()

PyNeFrauds.Globals.neo4jHandler.set_credentials("bolt://localhost:11003", "neo4j","password")
x = PyNeFrauds.nn.EmbedFetcher(embedProperty="fastRP", uniqueID=None, target="fraud")
REF_INDEX, featureMatrix, edge_index, targets = x.fetchData()
# print(x.fetch_node_embeddings()[0])
pd = PyGData()
pd.fromEmbedFetcher(x)
pd.showDataInfo()
# print(edge_index)