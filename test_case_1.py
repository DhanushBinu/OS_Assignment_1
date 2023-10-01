import subprocess
import time
import logging

logging.basicConfig(filename="test_case_1.log", level=logging.INFO, format='%(asctime)s - %(message)s')

server_command = "python socket_server.py -client_ids 1,2,3 -port 50051"
server_process = subprocess.Popen(server_command, shell=True)

time.sleep(2)

client1_command = "python socket_client.py -client_id 1 -server_ip 127.0.0.1 -port 50051 -log_path test_case_1.log"
client2_command = "python socket_client.py -client_id 2 -server_ip 127.0.0.1 -port 50051 -log_path test_case_1.log"
client3_command = "python socket_client.py -client_id 3 -server_ip 127.0.0.1 -port 50051 -log_path test_case_1.log"
client4_command = "python socket_client.py -client_id 4 -server_ip 127.0.0.1 -port 50051 -log_path test_case_1.log"

client1_process = subprocess.Popen(client1_command, shell=True, stdin=subprocess.PIPE)

logging.info("Test Case 1: Where Alice sends a meesage and Bob and Chad downlaod the messages after they come online\n")

client1_process.stdin.write(b"Alice\n")
client1_process.stdin.flush()

message = "Hello, Guys!"
client1_process.stdin.write(message.encode() + b"\n")
client1_process.stdin.flush()

time.sleep(5)



client2_process = subprocess.Popen(client2_command, shell=True, stdin=subprocess.PIPE)
client2_process.stdin.write(b"Bob\n")
client2_process.stdin.flush()


client3_process = subprocess.Popen(client3_command, shell=True, stdin=subprocess.PIPE)
client3_process.stdin.write(b"Chad\n")
client3_process.stdin.flush()

time.sleep(2)


logging.info("\nTest Case 2: Where Bob, and Alice sends a meesage and Dave, who is not part of the server does not receive the messages\n")

message = "Nice to finally meet you guys, how u guys doing?"
client2_process.stdin.write(message.encode() + b"\n")
client2_process.stdin.flush()

time.sleep(2)

message_1 = "I am going fine btw.wbu?"
client1_process.stdin.write(message_1.encode() + b"\n")
client1_process.stdin.flush()

time.sleep(2)

client4_process = subprocess.Popen(client4_command, shell=True, stdin=subprocess.PIPE)
client4_process.stdin.write(b"Dave\n")
client4_process.stdin.flush()

client1_process.wait()
client2_process.wait()

server_process.terminate()

