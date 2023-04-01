// get the schema,property-constraint map from the backend
//      done in html file


// get the parent element that contains all the cards
const cardsContainer = document.getElementById('cards-container');
// add event listener to the parent element
cardsContainer.addEventListener('change', function (event) {
    const targetE = event.target;
    if (targetE.classList.value == "properties"){
        manageConstraint(targetE.id);
    }
});


// get the select elements from the DOM
let nodesSelect = document.getElementById('nodes')
let propertiesSelect = document.getElementById('properties')


// populate the nodes dropdown
for (let nodeType in schema.Nodes) {
    let option = document.createElement('option')
    option.value = nodeType
    option.text = nodeType
    nodesSelect.add(option)
}

// populate the properties dropdown based on the selected node type
nodesSelect.addEventListener('change', function () {
    //remove the default option from nodes
    const defaultToRemove = nodesSelect.querySelector(`option[value="${"null"}"]`);
    if (defaultToRemove) {
        nodesSelect.removeChild(defaultToRemove);
    }
    //new constraint can be formed now
    add_constr_btn = document.getElementById('add-constraint-btn')
    add_constr_btn.disabled = false

    let nodeType = nodesSelect.value
    propertiesSelect.innerHTML = ''  // clear the existing options
    indicator = document.createElement('option') //add indicator asking to select a property
    indicator.value = null
    indicator.text = "---Select a property---"
    propertiesSelect.add(indicator)
    let properties = schema.Nodes[nodeType]
    for (let prop in properties) {
        let option = document.createElement('option')
        option.value = prop
        option.text = " <" + schema.Nodes[nodeType][prop]['type'] + "> " + prop
        propertiesSelect.add(option)
    }
})
function addProperties(compID, nodeType) {
    console.log(nodeType)
    comp = document.getElementById(compID)
    comp.innerHTML = ''
    indicator = document.createElement('option')
    indicator.value = null
    indicator.text = "---Select a property---"
    comp.add(indicator)
    let properties = schema.Nodes[nodeType]
    for (let prop in properties) {
        let option = document.createElement('option')
        option.value = prop
        option.text = " <" + schema.Nodes[nodeType][prop]['type'] + "> " + prop
        comp.add(option)
    }
}

function toggleDisplay(id) {
    var x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
//to display the propType input
propertiesSelect.addEventListener('change', function () {
    //remove the default option from nodes
    const defaultToRemove = propertiesSelect.querySelector(`option[value="${"null"}"]`);
    if (defaultToRemove) {
        propertiesSelect.removeChild(defaultToRemove);
    }

    let property = propertiesSelect.value;
    let nodeType = nodesSelect.value;
    let inputType = schema.Nodes[nodeType][property]['type'];
    let constraintType = propType[inputType]['constraint'];

    //putting appropriate constraint prefix
    prefixField = document.getElementById('constraint-prefix')
    prefixField.style.display = 'block'
    prefixField.innerHTML = ''// clear the existing options
    let prefixes = propType[inputType]['prefixes']
    for (let idx in prefixes) {
        let option = document.createElement('option')
        option.value = prefixes[idx]
        option.text = prefixes[idx]
        prefixField.add(option)
    }
    //put appropriate constraint
    for (let typ in propType) {
        docElement = document.getElementById(propType[typ]['constraint'] + '-constraint')
        docElement.style.display = (constraintType === propType[typ]['constraint']) ? 'block' : 'none'
    }
});
function manageConstraint(propID) {
    comp = document.getElementById(propID)
    propValue = comp.value
    console.log(propValue)

}

//adding constraints
constrCount = 0;
let addConstraintBtn = document.getElementById("add-constraint-btn");
addConstraintBtn.addEventListener("click", function (event) {
    event.preventDefault(); // prevent default form submission behavior
    addConstraintCard();
});
function addConstraintCard() {
    nodeType = document.getElementById('nodes').value
    let form = document.getElementById("query-form");
    let newCard = document.createElement("div");
    newCard.classList.add("constraint-card");
    let i = constrCount;
    let id = "constraint-card-" + i
    newCard.setAttribute('id', id)
    newCard.innerHTML = `
        <label for="properties-${i}">Property:</label>
        <select name="properties-${i}" id="properties-${i}" class="properties">
            <option value="null">-- Select a property --</option>
        </select>
        <div id="constraint-input-${i}" class="constraint-input">
            <div class="constraint-prefix-container">
                <select name="constraint-prefix-${i}" id="constraint-prefix-${i}" class="constraint-prefix">
                </select>
            </div>
            <div id="regex-constraint-${i}" class="constraint-field">
                <label for="regex-${i}">Regex:</label>
                <input type="text" name="regex-${i}" id="regex-${i}">
            </div>

            <div id="range-constraint-${i}" class="constraint-field">
                <label for="min-${i}">Min:</label>
                <input type="number" name="min-${i}" id="min-${i}">

                <label for="max-${i}">Max:</label>
                <input type="number" name="max-${i}" id="max-${i}">
            </div>

            <div id="list-constraint-${i}" class="constraint-field">
                <label for="list-${i}">List:</label>
                <input type="text" name="list-${i}" id="list-${i}">
            </div>
        </div>
      `
    form.insertBefore(newCard, form.lastElementChild);
    addProperties('properties-' + i, nodeType)

    constrCount++;
}


//handle submission
cardInput = document.getElementById('query-form')
cardInput.addEventListener('submit', function (event) {
    event.preventDefault()
    let formData = new FormData(cardInput)
    //extract data from form
    let data = {}
    for (const [key, value] of formData.entries()) {
        data[key] = value
    }
    console.log(data)
    //process in backend and show result at frontend
    fetch('/create_query', {
        method: 'POST',
        body: data
    })
        .then(response => response.json())
        .then(data => {
            //show in frontend
            console.log(data)
        })
        .catch(error => console.error(error))
})

//code for visualization
var cy = cytoscape({
    container: document.getElementById('cy'),
    elements: {
        nodes: [
            { 'data': { 'id': 'a', 'label': 'Node A' } },
            { 'data': { 'id': 'b', 'label': 'Node B' } },
            { 'data': { 'id': 'c', 'label': 'Node C' } },
        ],
        edges: [
            { 'data': { 'source': 'a', 'target': 'b' } },
            { 'data': { 'source': 'b', 'target': 'c' } },
            { 'data': { 'source': 'c', 'target': 'a' } },
        ]
    },
    style: [
        {
            selector: 'node',
            style: {
                'background-color': '#666',
                'label': 'data(label)'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 3,
                'line-color': '#ccc'
            }
        }
    ],
    layout: {
        name: 'cose'
    }
});