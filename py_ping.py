from subprocess import check_call, CalledProcessError,PIPE
import socket
import time
from logging.handlers import TimedRotatingFileHandler
import os
import logging

def setup_logging():
   
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    log_handler = TimedRotatingFileHandler('py_ping_test.log', when='D', backupCount=30)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    return logger

logger = setup_logging()
ip = input("Lökj egy IP-t vagy host nevet pingeléshez: ")

print("\nIde fog logolni: {}\py_ping_test.log".format(os.path.dirname(os.path.realpath(__file__))))
print("Ping tesztelés fut...")
while True:
    try:
        check_call(['ping', '-n', '3', ip],stdout=PIPE)
        logger.info('ok ping test {}'.format(ip))
    except CalledProcessError as e:
        logger.error('failed ping test {}'.format(ip))

    try:
        socket.gethostbyname(ip)
        logger.info('ok DNS test {}'.format(ip))
    except:
        logger.error('failed DNS test {}'.format(ip))

    time.sleep(3)