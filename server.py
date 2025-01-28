import socket
import json
import argparse
import logging
import select
import struct
import time



def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', 
        dest="port", 
        type=int, 
        default='9999',
        help='port number to listen on')
    parser.add_argument('--loglevel', '-l', 
        dest="loglevel",
        choices=['DEBUG','INFO','WARN','ERROR', 'CRITICAL'], 
        default='INFO',
        help='log level')
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()      # parse the command-line arguments

    # set up logging
    log = logging.getLogger("myLogger")
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    level = logging.getLevelName(args.loglevel)
    log.setLevel(level)
    log.info(f"running with {args}")
    
    log.debug("waiting for new clients...")
    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSock.bind(("",args.port))
    serverSock.listen()

    clientList = [serverSock]

    while True:

        # HERE'S WHERE YOU NEED TO FILL IN STUFF
        # Use select to monitor server socket and client sockets
        readable, _, _ = select.select(client_list, [], [])

        for sock in readable:
            if sock is serverSock:  # New client connection
                try:
                    client_sock, client_addr = serverSock.accept()
                    client_list.append(client_sock)
                    log.info(f"New client connected: {client_addr}")
                except Exception as e:
                    log.error(f"Error accepting new client: {e}")
            else:  # Data from an existing client
                try:
                    # Read the length prefix (4 bytes)
                    packed_size = sock.recv(4)
                    if not packed_size:  # Client disconnected
                        log.info(f"Client {sock.getpeername()} disconnected.")
                        client_list.remove(sock)
                        sock.close()
                        continue

                    # Unpack the size and read the message
                    message_length = struct.unpack("!L", packed_size)[0]
                    message_data = sock.recv(message_length)
                    if not message_data:
                        log.error(f"Failed to receive message data from {sock.getpeername()}.")
                        continue

                    # Log the received message
                    log.info(f"Received message: {message_data.decode('utf-8')}")

                except Exception as e:
                    log.error(f"Error handling client: {e}")
                    client_list.remove(sock)
                    sock.close()
        # DELETE THE NEXT TWO LINES. It's here now to prevent busy-waiting.
      
                            
    

if __name__ == "__main__":
    exit(main())

