#!/usr/bin/python2.7

import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    
    # create the server object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # lets see if we can stand up the server
    try:
        server.bind((local_host,local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions"
        sys.exit(0)
    
    # listen with 5 backlogged--queued--connections
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # print out the local connection information 
        print"[+] Received incomming connections from %s:%d" % (addr[0],addr[1])
        
        # start a new thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        
        proxy_thread.start()
        
def main():
    # cursory check of command line args
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [reveive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.11.132.1 9000 True"
        sys.exit(0)
    
    # set up listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    
    # set up remote targets
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    # this tells our proxy to connect and receive data before sending to the remote host
    receive_first = sys.argv[5]
    
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
        
    # now spin up our listening socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)
    
if __name__ == "__main__":
    main()