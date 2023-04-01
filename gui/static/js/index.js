// get the schema,property-constraint map from the backend
//      done in html file


// get the parent element that contains all the cards
const masterContainer = document.getElementById('master-container');
// add event listener to the parent element
masterContainer.addEventListener('change', function (event) {
    const targetE = event.target;
    if (targetE.classList.contains("node-options")) {
        nodeSelected(targetE.id)
    }
    else if (targetE.classList.contains("property-options")) {
        propertySelected(targetE)
        //put generate cypher button if not already present.
        addGenerateBtn()
    }
});
//for clicks on buttons
masterContainer.addEventListener('click', function (event) {
    let targetB = event.target
    if (targetB.classList.contains("add-constraint-btn")) {
        addConstraint(targetB)
    }
    else if (targetB.id === "generate") {
        generate()
    }
})

function addGenerateBtn(){
    //adds generate CYPHER query button if not already present
    let btnId = "generate"
    let btn = document.getElementById(btnId)
    if (btn){
        return
    }
    btn = document.createElement("button")
    btn.setAttribute('id',btnId)
    btn.classList.add("generate-btn")
    btn.textContent = "Generate CYPHER"
    let masterContainer=document.getElementById("master-container")
    masterContainer.appendChild(btn)
}

//ADD QUERY-CARD
cardCount = 0;
let addQueryBtn = document.getElementById('add-query-btn');
addQueryBtn.addEventListener('click', function (event) {
    //get the field
    let field = document.getElementById('cards-container')
    //create a card
    let card = document.createElement('div')
    card.classList.add('query-card')
    let id = "query-card-" + cardCount
    card.setAttribute('id', id)
    //1. add the card
    //2. add entity meta specs
    let meta = document.createElement("div")
    meta.classList.add("entity-meta-container")
    meta.setAttribute('id',"entity-meta-container-"+cardCount)
    //3.    add node options to the card-meta
    addNodesOptions(meta)
    card.appendChild(meta)
    field.appendChild(card);
    //4. add constraints-container
    let constrContainer = document.createElement("div")
    constrContainer.classList.add("constraints-container")
    constrContainer.setAttribute("id", "constraints-container-" + cardCount)
    thisCard = document.getElementById(id)
    thisCard.appendChild(constrContainer)
    cardCount++;
});

function addNodesOptions(entityMeta) {
    let id = "node-options-" + cardCount
    //get card component
    // let card = document.getElementById(cardId)
    //  add label first
    let label = document.createElement("label")
    label.setAttribute('for', id)
    label.innerHTML = "Node"
    entityMeta.appendChild(label)
    //create select list
    let seList = document.createElement('select')
    seList.classList.add('node-options')
    seList.setAttribute('id', id)
    seList.setAttribute('name', id)
    //populate node options
    //put indicator default option first
    let option = document.createElement('option')
    option.value = "null"
    option.text = "--select nodeType--"
    seList.add(option)
    for (let nodeType in schema.Nodes) {
        let option = document.createElement('option')
        option.value = nodeType
        option.text = nodeType
        seList.add(option)
    }
    //add the select list in card
    entityMeta.appendChild(seList)
}

function nodeSelected(nodeId) {
    let n = nodeId.split("-").pop()
    let qId = n;
    let cardId = "query-card-" + n
    let card = document.getElementById(cardId)
    //add reference for the node if not exists
    addReference(qId)
    //put the (+)constraint button if this is the first time changed
    //  get the card first.
    let btnId = "add-constraint-btn-" + n
    let addBtn = document.getElementById(btnId)
    if (addBtn === null) {
        let newBtn = document.createElement("button")
        newBtn.classList.add("add-constraint-btn", "add-btn")
        newBtn.setAttribute('id', "add-constraint-btn-" + n)
        newBtn.setAttribute('type', "button")
        newBtn.textContent = "+ Constraint"
        card.appendChild(newBtn)
    }
    //empty the constraints-container
    let constrContId = "constraints-container-" + n
    let constrCont = document.getElementById(constrContId)
    constrCont.innerHTML = ''
    //remove the default --select node-- option if exists
    let selNodes = document.getElementById(nodeId)
    let toRemove = selNodes.querySelector(`option[value="${"null"}"]`);
    if (toRemove) {
        selNodes.removeChild(toRemove)
    }
}
function addReference(qId) {
    //adds entiry reference used for CYPHER query to entity-meta-container
    //if it doesnt exist already
    let refId = "reference-" + qId
    let ref = document.getElementById(refId)
    if (ref) {
        return
    }
    let metaField = document.getElementById("entity-meta-container-"+qId) 
    //create label
    let label = document.createElement("label")
    label.setAttribute('for',refId)
    label.innerText = 'Reference:'
    metaField.appendChild(label)
    //create newRef
    let newRef = document.createElement('input')
    newRef.setAttribute('type','text')
    newRef.setAttribute('id',refId)
    newRef.setAttribute('name',refId)
    let value = "e"+qId
    newRef.setAttribute('value',value)
    metaField.appendChild(newRef)
}

//user clicked on +constraint button
let constraintCount = 0
function addConstraint(targetB) {
    //constraints-field-<query-card-id>-<constraint-id>
    let qId = targetB.id.split("-").pop()
    let n = constraintCount
    //get the constraints container
    let constrContId = "constraints-container-" + qId
    let constrCont = document.getElementById(constrContId)
    //create a constraint field
    let constrField = document.createElement("div")
    let constrFieldId = "constraint-field-" + qId + "-" + n
    constrField.classList.add("constraint-field")
    constrField.setAttribute('id', constrFieldId)
    //add contraint field to constraint container
    constrCont.appendChild(constrField)
    constraintCount++;
    //populate the constrField with properties
    populateProperties(constrFieldId)
}

function populateProperties(constrFieldId) {
    //first get which nodeType was selected
    let qId = constrFieldId.split('-').slice(-2, -1)[0]
    let nodeType = document.getElementById("node-options-" + qId).value
    //get the constraint-field
    let n = constrFieldId.split('-').pop()
    let constrField = document.getElementById(constrFieldId)
    //add select component
    let id = "property-options-" + qId + "-" + n
    //  1. first add label
    let label = document.createElement("label")
    label.setAttribute('for', id)
    label.innerHTML = "Property"
    constrField.appendChild(label)
    //2. add select component
    let seList = document.createElement("select")
    seList.classList.add('property-options')
    seList.setAttribute('id', id)
    seList.setAttribute('name', id)
    //3. populate prop options in the select
    //  add default indicator value
    let indicator = document.createElement('option') //add indicator asking to select a property
    indicator.value = null
    indicator.text = "---Select a property---"
    seList.add(indicator)
    for (let prop in schema.Nodes[nodeType]) {
        let option = document.createElement('option')
        option.value = prop
        option.text = " <" + schema.Nodes[nodeType][prop]['type'] + "> " + prop
        seList.add(option)
    }
    constrField.appendChild(seList)
    //add core-constraint-field
    let coreConstrField = document.createElement("div")
    coreConstrField.classList.add("core-constraint-field")
    coreConstrField.setAttribute('id', "core-constraint-field-" + qId + "-" + n)
    constrField.appendChild(coreConstrField)
}



//HANDLING core constraints-----------------------

function propertySelected(propSel) {
    let qId = propSel.id.split('-').slice(-2, -1)[0]
    let n = propSel.id.split('-').pop()
    //get the property type
    let propVal = propSel.value
    //   get the node
    let nodeType = document.getElementById("node-options-" + qId).value
    let propType = schema.Nodes[nodeType][propVal]['type']
    //  constraint type for that propType
    let constrType = propConstrMap[propType]['constraint']
    //get core-constraint-field
    let coreField = document.getElementById("core-constraint-field-" + qId + "-" + n)
    coreField.innerHTML = ''
    //1.add constraint prefix
    //  add label first
    let label = document.createElement("label")
    label.setAttribute('for', "constraint-prefix-" + qId + "-" + n)
    label.innerHTML = "Prefix"
    coreField.appendChild(label)

    let constrPrefix = document.createElement("select")
    constrPrefix.classList.add('constraint-prefix')
    constrPrefix.setAttribute('id', "constraint-prefix-" + qId + "-" + n)
    let prefixes = propConstrMap[propType]['prefixes']
    for (let idx in prefixes) {
        let option = document.createElement('option')
        option.value = prefixes[idx]
        option.text = prefixes[idx]
        constrPrefix.add(option)
    }
    coreField.appendChild(constrPrefix)


    //add constraints
    appendAppropConstr(coreField, propType, qId, n)

    //remove the default option --select property-- if it exists
    let toRemove = propSel.querySelector(`option[value="${"null"}"]`);
    if (toRemove) {
        propSel.removeChild(toRemove)
    }
}
function appendAppropConstr(coreField, propType, qId, n) {
    let combId = qId + "-" + n
    let constr = document.createElement("div")
    constr.classList.add("constraint-specs")
    constr.setAttribute("id", "constraint-specs-" + combId)
    let constrType = propConstrMap[propType]['constraint']
    constr.setAttribute("constraintType", constrType)
    innerHTML = ""
    switch (constrType) {
        case "range":
            innerHTML = `
                <label for="min-${combId}">Min:</label>
                <input type="number" name="min-${combId}" id="min-${combId}">

                <label for="max-${combId}">Max:</label>
                <input type="number" name="max-${combId}" id="max-${combId}">
            `;
            break;
        case "list":
            innerHTML = `
                <label for="list-${combId}">List:</label>
                <input type="text" name="list-${combId}" id="list-${combId}">`;
            break;
        case "regex":
            innerHTML = `
                <label for="regex-${combId}">Regex:</label>
                <input type="text" name="regex-${combId}" id="regex-${combId}">
            `;
            break;
    }
    constr.innerHTML = innerHTML
    coreField.appendChild(constr)
}


//HANDLING submission----------------------
function generate(){
    //takes all the input
    //passes to back-end
    //waits for the response
    //visualizes the response
    console.info("time to work on the backend")
}