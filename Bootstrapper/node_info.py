'''

node_1 = kafka, logger(8002)
node_2 = validator-workflow(8007), scheduler(8008)
node_4 = node-manager(8004), load-balancer(8005)
node_5 = monitoring-fault-tolerance(8009), api-gateway(8003)
node_6 = deployer(8006), paltform-ui(8005), platform-backend(8003)

'''


# done
#sshpass -p Jeet@deployer ssh jeetdeployer@20.2.81.4
node_1 =  {
        "ip" : "20.2.81.4",
        "password" : "Jeet@deployer",
        "user_name" : "jeetdeployer",
        "node_name": "node_1"
}

#done
#sshpass -p Abcdefgh@1234 ssh prannema@20.127.0.89
node_2 = {
    "ip" : "20.127.0.89",
    "password" : "Abcdefgh@1234",
    "user_name" : "prannema",
    "node_name" : "node_2"
}
    
#sshpass -p Abcdefgh@1234 ssh samvm@20.168.11.105
# node_3 = {
#     "ip" : "20.168.11.105",
#     "password" : "Abcdefgh@1234",
#     "user_name" : "samvm",
#     "node_name" : "node_3"
# }
    
# done
#sshpass -p Madhusree#007 ssh Madhusree@20.150.215.156
node_4 = {
    "ip" : "20.150.215.156",
    "password" : "Madhusree#007",
    "user_name" : "Madhusree",
    "node_name" : "node_4"
}
    
# done
#sshpass -p siddhant@123 ssh Siddhant@20.197.0.112
node_5 = {
    "ip" : "20.197.0.112",
    "password" : "siddhant@123",
    "user_name" : "Siddhant",
    "node_name" : "node_5"
}
    
# done
#sshpass -p Meet@12345678 ssh Meet@20.163.50.237
node_6 = {
    'ip' : '20.163.50.237',
    'user_name': 'Meet',
    'password' : 'Meet@12345678',
    'node_name' : "node_6"
}
    
# done
#sshpass -p L@2gjSubecbbcwi ssh myVM@13.72.70.97
node_7 = {
    "ip" : "13.72.70.97",
    "user_name" : "myVM",
    "password" : "L@2gjSubecbbcwi",
    "node_name": "node_7"
}


node_list = [node_1, node_2, node_4, node_5, node_6]
