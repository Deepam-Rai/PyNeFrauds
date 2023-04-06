// in gui_cypher specifically handles the visualization part.

//instantiating neovis viz object with credentials; has security issues
var viz;
console.log(neoCreds)
var config = {
    containerId: "viz",
    neo4j: neoCreds,
    labels: {},
    relationships: {},
    initialCypher: ""
};
console.log(config)
var options = {
    width: (window.innerWidth - 25) + "px",
    height: (window.innerHeight - 75) + "px"
};
viz = new NeoVis.default(config);


function createGraph(cypher) {
    //append graph field if not already done
    appendGraphField()
    setConfig()
    viz.renderWithCypher(cypher, { initial: true }, 800, 600);
}

function appendGraphField() {
    let graphField = document.getElementById('graph-field')
    if (graphField === null) {
        let metaCont = document.getElementById('master-container')
        let graphField = document.createElement("div")
        graphField.classList.add('graph-field') //general area for graphing
        graphField.setAttribute('id', 'graph-field')
        let viz = document.createElement("div") //core area for graphing
        viz.setAttribute('id', 'viz')
        graphField.appendChild(viz)
        metaCont.appendChild(graphField)
    }
}

function setConfig() {
    //set some config
}