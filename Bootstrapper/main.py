import services_info as platform_info
import blob_handler
import unzipping_file as unzip
import image_builder
import image_deployer
import node_info
import redpanda_kafka as kafka
import global_variables
from datetime import datetime
import logger as logger
import service_registry

platform_services = platform_info.platform_services

# do call function for redpanda-server start
kafka.start_kafka_server(node_info.node_1)

global_variables.CONTAINER_UP_TIME = datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")

print(global_variables.CONTAINER_UP_TIME)

service_entry = {
        "app_name" : "platform",
        "service_name": 'bootstrapper',
        "app_id": datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f"),
        "port": 8000,
        "container_up_time": global_variables.CONTAINER_UP_TIME,
        "container_name": '',
        "node_name": '',
        "ip": ''
}

insert_status = service_registry.add_service_info(service_entry)                
                

for service_name, service_info in platform_services.items():

    if service_name in ['deployer', 'logger', 'sensor-manager']:

        print(service_name)

        print("==============================================================")

        print(f"\nStarting deployment for {service_name}\n")
        logger.log_message('DEBUG', f'Starting deployment for {service_name}')

        print("==============================================================\n")

        # download the code from blob storage
        file_name = blob_handler.download_the_zip_file({"app_name" : "platform", "service_name" : service_name})

        if file_name != None:

            # generate docker file and inject it to the service code
            service_folder_name, contanarized_app_port = unzip.generate_dockerfile(file_name)

            # build the docker image
            image_name = image_builder.build_image(service_name, service_folder_name)

            # store docker image
            acr_image_path = image_builder.push_docker_image(image_name, platform_info.acr_info, service_name)

            # run the image on docker container
            deployment_status, container_name, container_up_time = image_deployer.run_docker_image(platform_info.acr_info, service_info, contanarized_app_port ,acr_image_path, service_name)

            if deployment_status == True:

                print("==============================================================")

                print(f"\nCompleted deployment for {service_name}\n")
                logger.log_message('DEBUG', f"Completed deployment for {service_name}")

                print("==============================================================\n")

                # store info into app-registry
                service_entry = {
                    "app_name" : "platform",
                    "service_name": service_name,
                    "app_id": datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f"),
                    "port": service_info['port'],
                    "container_up_time": container_up_time,
                    "container_name": container_name,
                    "node_name": service_info['node_info']['node_name'],
                    "ip": service_info['node_info']['ip']
                }
                insert_status = service_registry.add_service_info(service_entry)                
                
            else:
                print("==============================================================")

                print(f"\nError in deployment for {service_name}\n")
                logger.log_message('ERROR', f'Error in deployment for {service_name}')

                print("==============================================================\n")
        