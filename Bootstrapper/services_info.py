import node_info 


acr_info = {
    "login_server" : "testimages01.azurecr.io", 
    "username" : "testimages01", 
    "password" : "EnQFZBylKmDFlOEPuf1LQ3ZYvKxxlbb1Qd8uYdXGQw+ACRBcl3xB"
}

platform_services = {
    "logger" : {
        "port" : 8002,
        "node_info" : node_info.node_1
    },
    "api-gateway": {
        "port": 8003,
        "node_info": node_info.node_1
    },
    "node-manager" : {
        "port" : 8004,
        "node_info" : node_info.node_1

    },
    "load-balancer" : {
        "port" : 8005,
        "node_info" : node_info.node_1

    },
    "deployer" : {
        "port" : 8006,
        "node_info" : node_info.node_1

    },
    "validator-workflow" : {
        "port" : 8007,
        "node_info" : node_info.node_1
    },
    "scheduler" : {
        "port" : 8008,
        "node_info" : node_info.node_1
    },
    "monitoring-fault-tolerance": {
        "port" : 8009,
        "node_info": node_info.node_1
    },
    "sensor-manager": {
        "port" : 8010,
        "node_info": node_info.node_1
    }
}



