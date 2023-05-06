import node_info 
import os

acr_info = {
    "login_server" : "testimages01.azurecr.io", 
    "username" : "testimages01", 
    "password" : "EnQFZBylKmDFlOEPuf1LQ3ZYvKxxlbb1Qd8uYdXGQw+ACRBcl3xB"
}

platform_services = {

    "platform-ui" : {
        "port" : 8005,
        "node_info" : node_info.node_1
    },
    "platform-backend" : {
        "port" : 8011,
        "node_info" : node_info.node_1
    },
    "deployer" : {
        "port" : 8006,
        "node_info" : node_info.node_1
    },
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

def setup_ssh(nodes):
    for node in nodes:
        os.system(f"ssh-keyscan -H {node['ip']} >> ~/.ssh/known_hosts")