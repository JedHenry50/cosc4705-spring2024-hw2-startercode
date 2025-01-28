"""
A skeleton from which you should write your client.
"""


import socket
import json
import argparse
import logging
import select
import sys
import time
import datetime
import struct

from message import UnencryptedIMMessage


def parseArgs():
    """
    parse the command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', 
        dest="port", 
        type=int, 
        default='9999',
        help='port number to connect to')
    parser.add_argument('--server', '-s', 
        dest="server", 
        required=True,
        help='server to connect to')       
    parser.add_argument('--nickname', '-n', 
        dest="nickname", 
        required=True,
        help='nickname')                
    parser.add_argument('--loglevel', '-l', 
        dest="loglevel",
        choices=['DEBUG','INFO','WARN','ERROR', 'CRITICAL'], 
        default='INFO',
        help='log level')
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()

    # set up the logger
    log = logging.getLogger("myLogger")
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    level = logging.getLevelName(args.loglevel)
    
    log.setLevel(level)
    log.info(f"running with {args}")
    
    log.debug(f"connecting to server {args.server}")
    try:
        s = socket.create_connection((args.server,args.port))
        log.info("connected to server")
    except:
        log.error("cannot connect")
        exit(1)

    # here's a nice hint for you...
    readSet = [s, sys.stdin]

    while True:
        # HERE'S WHERE YOU NEED TO FILL IN STUFF

        readable, _, _ = select.select(readSet, [], [])

        for r in readable:
            if r is s:  # Data from the server
                try:
                    # Read the length prefix (4 bytes)
                    packedSize = s.recv(4)
                    if not packedSize:
                        log.info("Server disconnected.")
                        exit(0)

                    # Unpack the size and read the full message
                    messageLength = struct.unpack('!L', packedSize)[0]
                    messageData = s.recv(messageLength)
                    if not messageData:
                        log.error("Failed to receive message data.")
                        continue

                    # Parse and display the message
                    message = UnencryptedIMMessage()
                    message.parseJSON(messageData)
                    print(message)
                except Exception as e:
                    log.error(f"Error receiving message: {e}")
                    exit(1)

            elif r is sys.stdin:  # User typed something
                # Read the input and send it to the server
                userInput = sys.stdin.readline().strip()
                if not userInput:
                    continue

                # Create a new message and serialize it
                message = UnencryptedIMMessage(nickname=args.nickname, msg=userInput)
                packedSize, jsonData = message.serialize()

                try:
                    s.sendall(packedSize + jsonData)
                except Exception as e:
                    log.error(f"Error sending message: {e}")
                    exit(1)
        for r in r
        # DELETE THE NEXT TWO LINES. It's here now to prevent busy-waiting.

        

if __name__ == "__main__":
    exit(main())

