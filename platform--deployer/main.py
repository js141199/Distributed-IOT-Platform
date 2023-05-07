#THIS WILL EXECUTE ALL THE CODES NEED TO DEPLOY AN APPLICATION.
from kafka_talks import send_using_kafka
from kafka_talks import receive_using_kafka
import threading
import global_variables
import image_deployer
import os
import image_builder
from dbinteraction import getAppData, setAppdata
from datetime import datetime
import logger as log
import global_setup
import heartbeatGenerator as heartbeat

global_setup.setup_global_env()


print("[+] Deployer server listening....")
log.log_message('DEBUG', "[+] Deployer server listening....")

def initiating_deployer_process(scheduler_request):    

    app_id = scheduler_request['appId']
    app_name = scheduler_request['appName']
    service_names = scheduler_request['serviceName']
    schedule_type = scheduler_request['scheduleType']

    print(f"Starting deployer process for app[{app_name}] app_id[{app_id}]")
    log.log_message('DEBUG', f"Starting deployer process for app[{app_name}] app_id[{app_id}]")

    for service_name in service_names:
        
        # code for just building an docker image if already not built
        if schedule_type == 'build':

            print(f"Start building image for app[{app_name}] service[{service_name}]")
            log.log_message('DEBUG', f"Start building image for app[{app_name}] service[{service_name}]")

            # first check that is image already built for the given app and service
            app_data, image_status = getAppData(app_id, service_name)

            if image_status == False:

                # build the image store to ACR, and get image_path and app_port
                acr_image_path, contanarized_app_port = image_builder.build_and_store_image(app_id, app_name, service_name)

                if acr_image_path != None and contanarized_app_port != None:
                    # sid has to store these info into mongo-db
                    dataInserted = setAppdata(app_id, app_name, service_name, acr_image_path, contanarized_app_port)

                print(f"Building image completed for app[{app_name}] service[{service_name}]")
                log.log_message('DEBUG', f"Building image completed for app[{app_name}] service[{service_name}]")

            else:
                print(f'Image already built and stored in ACR for app[{app_name}] service[{service_name}]')
                log.log_message('DEBUG', f'Image already built and stored in ACR for app[{app_name}] service[{service_name}]')

        # run the image of given app_name, service_name which is already stored in ACR
        elif schedule_type == 'run':

            print(f"Request came for deploying app[{app_name}] service[{service_name}]")
            log.log_message('DEBUG', f"Request came for deploying app[{app_name}] service[{service_name}]")

            # producing request to load-balancer for best node
            # change these request formats ask to advait bhai
            message = {"message":"Node Required"} 
            send_using_kafka("getNodeRequest",message)

            print("Message produced to load-balancer.....")
            log.log_message('INFO', "Message produced to load-balancer.....")

            print("Waiting for reply from load-balancer.....")
            log.log_message('INFO', "Waiting for reply from load-balancer.....")

            # consuming the response from load-balancer
            node_info = receive_using_kafka("bestNodeResponse")
            print("Reply from load-balancer = ", node_info)
            log.log_message('DEBUG', f"Reply from loab-balancer = {node_info}")

            # sid has to write query to fetch port and acr_image_path form mongo-db
            # first check that do we have image or not
            app_data, image_status = getAppData(app_id, service_name)

            if image_status == True:

                contanarized_app_port = app_data['port']
                acr_image_path = app_data['acr_img_path']

                deployment_status, container_name, container_id = image_deployer.run_docker_image(global_variables.acr_info, node_info, contanarized_app_port, acr_image_path, app_name, service_name)

                if deployment_status == True:
                    # send success message to node-manager => jeet
                    success_msg_node_manager =  {
                        "app_name" : app_name,
                        "service_name": service_name,
                        "app_id": app_id,
                        "port": node_info["port"],
                        # format of container_up_time = 'dd-mm-yyyy-H-M-S-MS'
                        "container_up_time": datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f"),
                        "container_name": container_name,
                        "node_name": node_info["node_name"],
                        "ip": node_info["ip"],
                        "container_id": container_id
                    }

                    print(f"sending response to node-manager : \n{success_msg_node_manager}")
                    send_using_kafka("getServiceDetailsRequest", success_msg_node_manager)
                    print(f"message sent sucessfully!! to node-manager")

                else:
                    # do something when failure happens
                    # we can say to app-developer that some error is present in the code, service
                    # cannot be deployed
                    pass
            else:
                print(f'Image not found for app[{app_name}] service[{service_name}]')
                log.log_message('DEBUG', f'Image not found for app[{app_name}] service[{service_name}]')

        # build the image if already not built and then run the image stored in ACR
        elif schedule_type == 'build-run':

            print(f"Start build and run process image for app[{app_name}] service[{service_name}]")
            log.log_message('DEBUG', f"Start build and run process for app[{app_name}] service[{service_name}]")

            # first check that is image already built for the given app and service
            app_data, image_status = getAppData(app_id, service_name)

            print(f'app-data:  {app_data} image_status: {image_status}')

            acr_image_path, contanarized_app_port = None, None

            if image_status == False:
                # build the image store to ACR, and get image_path and app_port
                acr_image_path, contanarized_app_port = image_builder.build_and_store_image(app_id, app_name, service_name)
            
            else:
                acr_image_path, contanarized_app_port = app_data['acr_img_path'], app_data['port']
            
            if acr_image_path != None and contanarized_app_port != None:
                
                # sid has to store these info into mongo-db
                dataInserted = setAppdata(app_id, app_name, service_name, acr_image_path, contanarized_app_port)
                print('Appservice data inserted in db(inside build-run): ', dataInserted)

                # producing request to load-balancer for best node
                message = {"message":"Node Required"} 
                send_using_kafka("getNodeRequest",message)

                print("Message produced to load-balancer.....")

                print("Waiting for reply from load-balancer.....")

                # consuming the response from load-balancer
                node_info = receive_using_kafka("bestNodeResponse")
                '''
                    node_info = {
                        "node_name" : "",
                        "user_name" : "",
                        "password" : "",
                        "ip" : ""
                    }
                '''
                print(f"Reply from load-balancer = {node_info}")

                deployment_status, container_name, container_id  = image_deployer.run_docker_image(global_variables.acr_info, node_info, contanarized_app_port, acr_image_path, app_name, service_name)

                if deployment_status == True:
                    # send success message to node-manager => jeet
                    success_msg_node_manager =  {
                        "app_name" : app_name,
                        "service_name": service_name,
                        "app_id": app_id,
                        "port": node_info["port"],
                        # format of container_up_time = 'dd-mm-yyyy-H-M-S-MS'
                        "container_up_time": datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f"),
                        "container_name": container_name,
                        "node_name": node_info["node_name"],
                        "ip": node_info["ip"],
                        "container_id": container_id
                    }

                    print(f"sending response to node-manager : \n{success_msg_node_manager}")
                    send_using_kafka("getServiceDetailsRequest", success_msg_node_manager)
                    print(f"message sent sucessfully!! to node-manager")
                else:
                    # do something when failure happens
                    # we can say to app-developer that some error is present in the code, service
                    # cannot be deployed
                    pass

        # start the container after doing proper validation of container existence
        elif schedule_type == 'start':
            # integrate advait code 
            pass

        # start the container after doing proper validation of container existence
        elif schedule_type == 'stop':
            # integrate advait code
            # doc_handler.request_to_stop_the_service(node_info,container_name)
            pass


    # send failure message seperately for each service

    print(f"sending response to scheduler : \n {scheduler_request}")
    send_using_kafka("deployerToScheduler", scheduler_request)
    print(f"message sent sucessfully!! to scheduler")




# Thread is created for heartbeat monitoring
t1 = threading.Thread(target=heartbeat.sendheartBeat, args=("heartbeat-deployer", global_variables.container_name, global_variables.node_name, ))
t1.start()


# start point of the code listening to the scheduler request

while True:
    print("Waiting for scheduler request")
    log.log_message('DEBUG', "Waiting for scheduler request")
    scheduler_request = receive_using_kafka("schedulerToDeployer")

    '''
        scheduler_request = {
            'appId' : unique application id
            'appName' : application-name given by app-developer
            'serviceName' : list of service-name of applicaion,
            'scheduleType' : 'build', 'build-run', 'start', 'stop', 'run'
            'accessToken' : token coming from the requester which I will send in response back
            'kafkaTopic' : 'response-scheduler' requester will send the kafka-topic name
            'cron' : true/false
        }
    '''

    # zip name = appId--serviceName.zip

    print(f"Request consumed from scheduler => {scheduler_request}")
    log.log_message('DEBUG', f"Request consumed from scheduler => {scheduler_request}")

    # initiating_deployer_process(scheduler_request)
    threading.Thread(target = initiating_deployer_process, args = (scheduler_request, )).start()
