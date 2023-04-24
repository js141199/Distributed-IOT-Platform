import os


def start_kafka_server(node_info):

    os.system(f"sshpass -p {node_info['password']} ssh {node_info['user_name']}@{node_info['ip']} 'mkdir kafka;exit'")

    os.system(f"sshpass -p {node_info['password']} scp -r /home/jeetshah141199/Desktop/IIITH_SEM_2/IAS_Project/Platform_initializer/Bootstrapper/docker-compose.yml {node_info['user_name']}@{node_info['ip']}:~/kafka")

    os.system(f"sshpass -p {node_info['password']} ssh {node_info['user_name']}@{node_info['ip']} 'cd kafka;docker compose up -d;docker ps;exit'")

    print("Kafka server started")

