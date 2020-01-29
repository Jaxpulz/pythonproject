from subprocess import check_call, CalledProcessError,PIPE
import socket
import time
from logging.handlers import TimedRotatingFileHandler
import os
import logging


logging.basicConfig(filename='py_ping_test.log',level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

ip = input("Lökj egy IP-t vagy host nevet pingeléshez: ")

print("\nIde fog logolni: {}\py_ping_test.log".format(os.path.dirname(os.path.realpath(__file__))))
print("Ping tesztelés fut...")
while True:
    try:
        check_call(['ping', '-n', '3', ip],stdout=PIPE)
        logging.info('ok ping test {}'.format(ip))
    except CalledProcessError as e:
        logging.error('failed ping test {}'.format(ip))

    try:
        socket.gethostbyname(ip)
        logging.info('ok DNS test {}'.format(ip))
    except:
        logging.error('failed DNS test {}'.format(ip))

    time.sleep(3)