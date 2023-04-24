import os


def request_to_stop_the_service(node_info,container_name):

    container_status = os.popen(f"sshpass -p {node_info['password']} ssh {node_info['user_name']}@{node_info['ip']} " +  "'docker inspect -f '{{.State.Status}}' " + container_name + "'", 'r', 1).read()

    container_status = container_status.split('\n')[0]

    if container_status == 'running':
        print("Service deployed successfully!!")

        commands = list()
        commands.append(f"docker stop {container_name}")
        commands.append(f"docker rm {container_name}")
        command = ';'.join(commands)
        os.system(command)

        container_status = os.popen(f"'docker inspect -f '{{.State.Status}}' " + container_name  + ";exit'", 'r', 1).read()

        container_status = container_status.split('\n')[0]

        if container_status == 'running':
            print("Container is not down...Still Running")

        else :
            print("Container stopped successfully")
    
    return

