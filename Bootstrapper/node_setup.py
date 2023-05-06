import os


def setup_node_env(vm_list):

    for node_info in vm_list:
        
        print(f'Starting env setup for {node_info["ip"]}')

        os.system(f'ssh-keyscan -H {node_info["ip"]} >> ~/.ssh/known_hosts')

        os.system(f"sshpass -p {node_info['password']} scp -r ./node_env_setup.sh {node_info['user_name']}@{node_info['ip']}:~/.")

        os.system(f"sshpass -p {node_info['password']} ssh {node_info['user_name']}@{node_info['ip']} 'chmod 777 ./node_env_setup.sh'")

        os.system(f"sshpass -p {node_info['password']} ssh {node_info['user_name']}@{node_info['ip']} bash -s < ./node_env_setup.sh {node_info['ip']}")

        print(f'Env setup completed for {node_info["ip"]}')

