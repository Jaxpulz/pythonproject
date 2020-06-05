from subprocess import check_call, CalledProcessError,PIPE, Popen
import socket
import time
from logging.handlers import TimedRotatingFileHandler
import os
import logging

logging.basicConfig(filename='py_ping_test.log',level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

def setup_logging():
    logger = logging.getLogger()
    logger.propagate = False
    logging.getLogger().setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    log_handler = TimedRotatingFileHandler('py_ping_test.log', when='D', backupCount=30)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(log_handler)
    return logger

logger = setup_logging()
ip = input("Lökj egy IP-t vagy host nevet pingeléshez: ")

print("\nIde fog logolni: {}/py_ping_test.log".format(os.path.dirname(os.path.realpath(__file__))))
print("Ping tesztelés fut...")
while True:
    ping_response = (Popen(["ping", ip, "-c", '60','-W','1'], stdout=PIPE).stdout.read()).decode()
    rm_empty_lines = ping_response.split('\n')
    ping_response = [line for line in rm_empty_lines if line.strip() != ""]

    for line in ping_response:
        line = line.split('\r')
        line = [r for r in line if r.strip() != ""]
        for res in line:
            logger.info(res)

    time.sleep(2)