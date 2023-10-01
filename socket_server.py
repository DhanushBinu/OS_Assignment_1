import grpc
import asyncio
from Proto_Gen_Code import service_pb2
from Proto_Gen_Code import service_pb2_grpc
from concurrent import futures
import threading
import argparse
import time

class ServerServicer(service_pb2_grpc.Server_ServiceServicer):
    
    def __init__(self,client_ids) -> None:
        self.connected_clients = []
        self.client_messages = []
        self.message_history = {}
        self.client_ids = client_ids
        self.client_Dict = {}
        

    async def Connect(self,request,context):
        user_name = request.user_name
        if(str(request.user_id) in self.client_ids):
            self.client_Dict[request.user_id] = user_name
            self.connected_clients.append(user_name)
            for client,message in self.message_history.items():
                response = service_pb2.Response(
                    user_name = user_name,
                    user_response = f"{client} : {message}"
                )
                yield response
        else:
            yield service_pb2.Response(
                    user_name = "Server",
                    user_response = f"Sorry your are not allowed to access this chat!!"
                )
    
    async def Disconnect(self,request,context):
        if(context in self.connected_clients):
            self.connected_clients.remove(context)

        user_name = request.user_name
        response = service_pb2.Response(
            user_name = user_name,
            user_response = f"Disconnect Request from {user_name} received"
        )
        return response


    async def Send_message(self, request, context):
        user_name = request.user_name
        if(user_name in self.client_Dict.values()):
            user_message = request.user_message
            
            message_dict = {
                'sender': user_name,
                'message': user_message,
                'recipients': self.connected_clients.copy() 
            }
            self.client_messages.append(message_dict)

            if(user_name not in self.message_history):
                self.message_history[user_name] = []
            self.message_history[user_name].append(user_message)


        return service_pb2.Empty()
    
    async def Send_Message_to_all(self, request, context):
        user_name = request.user_name


        for message_dict in self.client_messages:
            sender = message_dict["sender"]
            message =message_dict["message"]
            if sender != user_name and user_name in message_dict["recipients"]:
                response = service_pb2.Response(
                    user_name=sender,
                    user_response=f"{sender}: {message}"
                    )
                yield response
                message_dict['recipients'].remove(user_name)

    
async def serve(port, client_ids):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=len(client_ids)))
    service_pb2_grpc.add_Server_ServiceServicer_to_server(ServerServicer(client_ids), server)
    server.add_insecure_port(f'127.0.0.1:{port}')
    await server.start()
    print(f'Server listening on port {port}')
    await server.wait_for_termination()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server for chat application')
    parser.add_argument('-port', type=int, required=True, help='Server port')
    parser.add_argument('-client_ids', type=str, required=True, help='Comma-separated list of client IDs')
    args = parser.parse_args()

    client_ids = set(args.client_ids.split(','))
    asyncio.run(serve(args.port,client_ids))
