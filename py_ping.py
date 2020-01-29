
from subprocess import check_call, CalledProcessError,PIPE
import socket
import time
from logging.handlers import TimedRotatingFileHandler
import os
import logging



logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
#Creating an object 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

ip = input("Lökj egy IP-t vagy host nevet pingeléshez: ")

print("\nIde fog logolni: {}\py_ping_test.log".format(os.path.dirname(os.path.realpath(__file__))))
print("Ping tesztelés fut...")

while True:
    try:
        check_call(['ping', '-n', '3', ip])
        logger.info('ok ping test {}'.format(ip))
    
    except CalledProcessError as e:
        logger.error('failed ping test {}'.format(ip))
    
    try:
        socket.gethostbyname(ip)
        logger.info('ok DNS test {}'.format(ip))
    except:
        logger.error('failed DNS test {}'.format(ip))

    time.sleep(3)