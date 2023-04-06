import PyNeFrauds.PyNe as PyNe
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
    ["asdf", "IS", {"<":23, ">=":14}],
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


cone = PyNe(json_text)
# print(cone.queries)
# print(cone.queries['Patient'][1])
cone.constructQueries(mode='MERGED')
cone.showQueries()
