function load_graph() {
    url = `/tasktiger/${task_data["queue"]}/${task_data["state"]}/${task_data["id"]}/graph`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(async response => {
        load_graph_data(await response.json());
    }).catch(error => {
        console.error('Error:', error);
    });
}

function load_graph_data(data) {
    console.log(data);
    nodes = new vis.DataSet(data.nodes);
    edges = new vis.DataSet(data.edges);
    var visData = {
        nodes: nodes,
        edges: edges,
    };
    var container = document.getElementById("graph");
    var options = {
        nodes: {
            mass: 4,
            font: {
                face: 'monospace',
                size: 14,
                color: 'black',
                align: 'left'
            }
        },
        edges: {
            physics: false,
        },
        layout: {
            randomSeed: 0,
            improvedLayout: true,
            hierarchical: getTreeLayout()
        },
        physics: {
            enabled: false
        },
        groups: {
            completed: {
                color: { background: "#8ed1f0" },
                borderWidth: 2,
                shape: 'box',
                mass: 2
            },
            active: {
                color: { background: "#8ef0a3" },
                borderWidth: 2,
                shape: 'box',
                mass: 2
            },
            waiting: {
                color: { background: "#d3e473" },
                borderWidth: 2,
                shape: 'box',
                mass: 2
            },
            scheduled: {
                color: { background: "#b173e4" },
                borderWidth: 2,
                shape: 'box',
                mass: 2
            },
            queued: {
                color: { background: "#73e4de" },
                borderWidth: 2,
                shape: 'box',
                mass: 2
            },
            error: {
                color: { background: "#f07272" },
                borderWidth: 2,
                shape: 'box',
                mass: 2
            },
            unknown: {
                color: { background: "#d43b3b" },
                borderWidth: 2,
                shape: 'box',
                mass: 2
            }
        }
    };
    var network = new vis.Network(container, visData, options);

    network.once('afterDrawing', (ctx) => {
        // workaround for resizing
        container.style.height = '300px';
    });
}

function getTreeLayout() {
    return {
        direction: "RL",
        sortMethod: 'directed',
        parentCentralization: true,
        edgeMinimization: true,
        levelSeparation: 600,
        nodeSpacing: 300,
        treeSpacing: 600,
        blockShifting: true,
        shakeTowards: 'leaves'
    };
}

window.addEventListener("load", event => {
    load_graph();
});