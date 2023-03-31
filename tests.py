import PyNeFrauds.PyNe as PyNe
# from PyNeFrauds.Constructor import testFun
# from PyNeFrauds.extractor import verifyAttributeProperties

json_text = '''
[{
  "NodeLabel" : "Patient",
  "Attributes" : {
    "Name" : ["IS NOT OF", "w"],
    "Contact" : ["IS", {">" : 9999999999}],
    "Age" : ["IS NOT", {"<=":130}],
    "asdf" : ["IS", {"<":23, ">=":14}],
    "ID" : ["IS", {"<":0}],
    "Gender" : ["NOT IN", ["Male","Female","Others"]]
  },
  "NodeProperties" : {
    "OutDegree" : ["IS",{">":7}],
    "Neighbours" : ["IS", {"<":3}]
  },  
  "AttributeRelations" : {
  }
},
{
  "NodeLabel" : "Treatment",
  "Attributes" : {
    "Name" : ["IS OF", "w"],
    "Cost" : ["IS", {"=":5000}],
    "asdf" : ["IS", {"<":23, ">=":14}],
    "ID" : ["IS", {"<":0}],
    "Category" : ["IN", ["Oncology","Pediatrics"]]
  },
  "NodeProperties" : {
    "OutDegree" : ["IS",{">":7}],
    "Neighbours" : ["IS", {"<":3}]
  },  
  "AttributeRelations" : {
  }
}
]
'''

cone = PyNe(json_text)
# print(cone.queries)
# print(cone.queries['Patient'][1])
cone.showQueries()
