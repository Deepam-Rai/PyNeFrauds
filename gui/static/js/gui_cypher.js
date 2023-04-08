//relations are also denoted/handled as "nodes" only
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
        addGetGraphBtn()
    }
    else if (targetE.classList.contains("relation-end")) {
        //need to check if the end-vertex reference added to relationship is valid
        relEndValidate(targetE)
    }
});
//for clicks on buttons
masterContainer.addEventListener('click', function (event) {
    let targetB = event.target
    if (targetB.classList.contains("add-constraint-btn")) {
        addConstraint(targetB)
    }
    else if (targetB.id === "get-graph-btn") {
        getGraph()
    }
    else if (targetB.id === "generate") {
        generate()
    }
    else if (targetB.classList.contains("del-btn")) {
        handleDelete(targetB)
    }
})

function addGenerateBtn() {
    //adds generate CYPHER query button if not already present
    let btnId = "generate"
    let btn = document.getElementById(btnId)
    if (btn) {
        return
    }
    btn = document.createElement("button")
    btn.setAttribute('id', btnId)
    btn.classList.add("generate-btn")
    btn.textContent = "Get CYPHER"
    let masterContainer = document.getElementById("master-container")
    masterContainer.appendChild(btn)
}
function addGetGraphBtn() {
    //adds generate CYPHER query button if not already present
    let btnId = "get-graph-btn"
    let btn = document.getElementById(btnId)
    if (btn) {
        return
    }
    btn = document.createElement("button")
    btn.setAttribute('id', btnId)
    btn.classList.add("get-graph-btn")
    btn.textContent = "Visualize"
    let masterContainer = document.getElementById("master-container")
    masterContainer.appendChild(btn)
}

//ADD QUERY-CARD
cardCount = 0;
let addQueryBtn = document.getElementById('add-query-btn');
addQueryBtn.addEventListener('click', function (event) {
    //get the field
    let field = document.getElementById('cards-container')
    //add the output LIMIT div if not present
    addOutputLimit(field)
    //create a card
    let card = document.createElement('div')
    card.classList.add('query-card')
    let id = "query-card-" + cardCount
    card.setAttribute('id', id)
    //1. add the card
    //2. add entity meta specs
    let meta = document.createElement("div")
    meta.classList.add("entity-meta-container")
    meta.setAttribute('id', "entity-meta-container-" + cardCount)
    //Add delete button
    addDeleteButton(meta, cardCount, cardOrConstr = "card")
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
function addOutputLimit(cont) {
    let opDiv = document.getElementById('output-limit')
    if (opDiv === null) {
        let opDiv = document.createElement("div")
        opDiv.classList.add("output-limit")
        opDiv.setAttribute('id', 'output-limit')
        
        let id = 'output-limit-field'
        //create label
        let label = document.createElement("label")
        label.setAttribute('for', id)
        label.innerText = 'LIMIT '
        opDiv.appendChild(label)
        //create input field
        let limIp = document.createElement('input')
        limIp.setAttribute('type', 'number')
        limIp.setAttribute('id', id)
        limIp.setAttribute('name', id)
        limIp.classList.add('output-limit-field')
        limIp.setAttribute('value', 25)
        opDiv.appendChild(limIp)
        cont.appendChild(opDiv)
    }
}

function addNodesOptions(entityMeta) {
    //check if schema is empty
    if (!loggedIn['value']) {
        let errDiv = document.createElement("div")
        errDiv.classList.add("error")
        errDiv.setAttribute("id", 'not-logged-in-error')
        errDiv.innerHTML = "Please log into neo4j first." + '<br><a href="/neo4j_login" style="color: blue;">Go to login page</a>'
        errDiv.style.display = 'block'
        entityMeta.appendChild(errDiv)
        return
    }
    else {
        let errDiv = document.getElementById('not-logged-in-error')
        if (errDiv) {
            errDiv.remove()
        }
    }

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
    for (let nodeType in schema) {
        let option = document.createElement('option')
        option.value = nodeType
        let nodeOrRel = schema[nodeType]['type'] === 'node' ? '<node> ' : '<rel> '
        option.text = nodeOrRel + nodeType
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
    //add reference for the node if not exists; also add source, destination field if its relation
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
    //if relation then adds source and destination field also
    let refId = "reference-" + qId
    let ref = document.getElementById(refId)
    if (ref) {
        return
    }
    let metaField = document.getElementById("entity-meta-container-" + qId)
    //create label
    let label = document.createElement("label")
    label.setAttribute('for', refId)
    label.innerText = 'Reference:'
    metaField.appendChild(label)
    //create newRef
    let newRef = document.createElement('input')
    newRef.setAttribute('type', 'text')
    newRef.setAttribute('id', refId)
    newRef.setAttribute('name', refId)
    newRef.classList.add('reference')
    let value = "e" + qId
    newRef.setAttribute('value', value)
    metaField.appendChild(newRef)
    //if it is relationship add source and destination field also
    let isRel = schema[document.getElementById('node-options-' + qId).value]['type'] === 'relationship'
    if (isRel) {
        let fields = ['source', 'dest']
        fields.forEach(field => {
            //create label
            let label = document.createElement("label")
            label.setAttribute('for', field)
            label.innerText = field + ':'
            metaField.appendChild(label)
            let inpt = document.createElement('input')
            inpt.setAttribute('type', 'text')
            inpt.setAttribute('id', field + '-' + qId)
            inpt.classList.add('relation-end')
            metaField.appendChild(inpt)
        });
    }
}

function addDeleteButton(cont, id, cardOrConstr) {
    let newBtn = document.createElement("button")
    newBtn.classList.add("del-btn")
    newBtn.setAttribute('type', "button")
    if (cardOrConstr === "card") {
        newBtn.classList.add('delete-query-card-btn')
        newBtn.setAttribute('id', "del-query-card-btn-" + id)
        newBtn.textContent = "Delete"
    }
    else if (cardOrConstr === 'constr') {
        newBtn.classList.add('delete-constr-btn')
        newBtn.setAttribute('id', "del-constr-btn-" + id)
        newBtn.textContent = "Delete"
    }
    cont.appendChild(newBtn)
}
function handleDelete(btn) {
    let toDel = null
    if (btn.classList.contains('delete-query-card-btn')) {
        let id = btn.id.split('-').pop()
        toDel = document.getElementById('query-card-' + id)
    }
    else if (btn.classList.contains('delete-constr-btn')) {
        let id = btn.id.split('-').slice(-2).join('-')
        toDel = document.getElementById('constraint-field-' + id)
    }
    toDel.remove()
}


function relEndValidate(field) {
    //checks if the end-vertex reference added for relationship is proper or not
    //get valid references first
    let refs = document.querySelectorAll('.reference')
    let valRefs = []
    refs.forEach(ref => {
        let isNotRel = schema[ref.parentElement.querySelector('.node-options').value]['type'] !== 'relationship'
        if (isNotRel) {
            valRefs.push(ref.value)
        }
    })
    if (!valRefs.includes(field.value)) {
        //empty it
        field.value = ''
        //change color to red
        field.style.backgroundColor = '#ffcece'
        field.style.border = '2px solid #ff9b9b'
    }
    else {
        field.style.backgroundColor = '#ffffff'
        field.style.border = ''
    }
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
    addDeleteButton(constrField, qId = qId + '-' + n, cardOrConstr = 'constr')
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
    for (let prop in schema[nodeType]['properties']) {
        let option = document.createElement('option')
        option.value = prop
        option.text = " <" + schema[nodeType]['properties'][prop]['type'] + "> " + prop
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
    let propType = schema[nodeType]['properties'][propVal]['type']
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
    constr.setAttribute("constraint-type", constrType)
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
function generate() {
    //Generates the CYPHER query
    //takes all the input
    let queryCards = document.getElementById("master-container").querySelectorAll('.query-card')
    let entities = []
    queryCards.forEach(queryCard => {
        let flag = false; //to add the entity or not
        let entity = {};
        //get entity label
        let label = getLabel(queryCard)
        if (label !== "null") {
            entity.label = label
            //get entity type
            entity.type = schema[label]['type']
            //if it is relationship then get source and destination too
            let qId = queryCard.id.split('-').pop()
            if (entity.type === 'relationship') {
                entity.source = document.getElementById('source-' + qId).value
                entity.dest = document.getElementById('dest-' + qId).value
            }
            //get entity references
            entity.ref = getReference(queryCard)
            //loop and get the constraints
            entity['Attributes'] = []
            let constrs = queryCard.querySelectorAll('.constraint-field')
            constrs.forEach(constr => {
                let value = constr.querySelector('.property-options').value
                if (value !== "null") {
                    let constrPrefix = constr.querySelector('.constraint-prefix').value
                    let constrSpecs = getConstraintSpecs(constr)
                    let constraint = [constrPrefix, constrSpecs]
                    entity['Attributes'].push([[value], constraint])
                    flag = true;
                }
            })
            entities.push(entity)
        }
    });
    //put CYPHER display if it doesnt exists
    putCYPHERDisplay()
    console.log("Sending Data:", entities)
    fetch('/create_query', {
        // passes to back-end
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(entities)
    })
        .then(response => response.json())
        .then(data => {
            console.log("Got the data!", data)
            let limit = " LIMIT " + document.getElementById('output-limit-field').value
            updateCYPHERdisplay(data['CYPHER'] + limit)
            //visualizes the response
        })
        .catch(error => {
            console.error(error)
        })
}
function getLabel(queryCardP) {
    //queryCardP should be either queryCard or its id
    let queryCard = typeof (queryCardP) === 'string' ? document.getElementById(queryCardP) : queryCardP
    let nodeType = queryCard.querySelector('.node-options').value
    return nodeType
}
function getReference(queryCardP) {
    //queryCardP should be either queryCard or its id
    let queryCard = typeof (queryCardP) === 'string' ? document.getElementById(queryCardP) : queryCardP
    let ref = queryCard.querySelector('.reference').value
    return ref
}
function getConstraintSpecs(constrFieldP) {
    //constrFieldP is either dom object or id
    //returns constraint type, dict/str/list of constraint-specs
    let constrField = typeof (constrFieldP) === 'string' ? document.getElementById(constrFieldP) : constrFieldP
    let suffixId = constrField.id.split('-').slice(-2).join('-')
    //determine type of constraint
    let constrType = constrField.querySelector('.constraint-specs').getAttribute('constraint-type')
    //get the constraint dict
    let spec = null
    switch (constrType) {
        case 'range':
            let max = constrField.querySelector('#max-' + suffixId).value
            let min = constrField.querySelector('#min-' + suffixId).value
            spec = { '>=': min, '<=': max }
            break;
        case 'regex':
            spec = constrField.querySelector('#regex-' + suffixId).value
            break;
        case 'list':
            spec = parseStringToArray(constrField.querySelector('#list-' + suffixId).value)
            //#TODO change type if required
            break;
    }
    return spec
}
function parseStringToArray(str) {
    const delimiter = /(?<!\\),/; // match comma not preceded by backslash
    let parts = str.split(delimiter).map(part => part.replace(/\\,/g, ',')); // replace escaped commas with comma
    parts = parts.map(part => part.trim());
    return parts;
}

function putCYPHERDisplay() {
    let id = "cypher-display"
    let cypherDis = document.getElementById(id)
    if (cypherDis === null) {
        let cypherDis = document.createElement("div")
        cypherDis.setAttribute('id', id)
        cypherDis.setAttribute('name', id)
        cypherDis.classList.add("cypher-display")
        let cypherField = document.createElement("div") //holds cypher
        cypherField.classList.add("cypher-field")
        cypherField.setAttribute('id', 'cypher-field')
        cypherDis.appendChild(cypherField)
        let masterCont = document.getElementById("master-container")
        masterCont.appendChild(cypherDis)
    }
}
function updateCYPHERdisplay(txt) {
    let cypherDis = document.getElementById("cypher-field")
    cypherDis.innerHTML = txt
}

//Visualizing the graph
// there is a separate .js file to handle this. below function is just a connector
function getGraph() {
    //takes the CYPHER; gets the graph
    //create the cypher first
    generate()
    //get the cypher from the cypher field; it may take sometime to generate cypher
    let cypher = ""
    waitForCypher()
        .then((cypher) => {
            createGraph(cypher)
        })
        .catch((err) => {
            console.error("Some error occurred:", err);
        });
}

function waitForCypher() {
    return new Promise((resolve, reject) => {
        let cypherField = document.getElementById('cypher-field');
        let cypher = cypherField.textContent.trim();
        if (cypher === "") {
            let intervalId = setInterval(function () {
                cypher = cypherField.textContent.trim();
                if (cypher !== "") {
                    clearInterval(intervalId);
                    resolve(cypher);
                }
            }, 100);

            setTimeout(function () {
                clearInterval(intervalId);
                reject(new Error("Timeout expired"));
            }, 3000);
        } else {
            resolve(cypher);
        }
    });
}

