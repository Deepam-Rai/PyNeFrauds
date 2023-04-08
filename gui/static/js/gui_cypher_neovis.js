// in gui_cypher specifically handles the visualization part.

//instantiating neovis viz object with credentials; has security issues
var viz;
var config = {
    containerId: "viz",
    neo4j: neoCreds,
    visConfig: {
        nodes: {
            color: 'red',
            font: {
                strokeWidth : 0,
                color: '#ffffff',
                size: 20,
                face: 'Open Sans'
            }
        },
        edges: {
            arrows: {
                to: { enabled: true }
            }
        },
    },
    labels: {},
    relationships: {}
};
var options = {
    width: (window.innerWidth - 25) + "px",
    height: (window.innerHeight - 75) + "px"
};



function createGraph(cypher) {
    //append graph field if not already done
    appendGraphField()
    config.labels = getLabelsConfig()
    console.log(config)
    viz = new NeoVis.default(config);
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
console.log(schema)

function getLabelsConfig() {
    //set the size of nodes
    let labelsConfig = {}
    for (let ent in schema){
        if (schema[ent]['type']==='node'){
            nodeConfig = {'label': 'project_name'}
            nodeConfig["[NeoVis.NEOVIS_ADVANCED_CONFIG]"] = {
                cypher : {
                    size : "MATCH (n) WHERE id(n) = $id RETURN n.size"
                }
            }
            labelsConfig[ent] = nodeConfig

        }
    }
    return labelsConfig
}