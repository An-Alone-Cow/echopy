import socket
import logging.config
from datetime import datetime
from multiprocessing import Process
from signal import signal, SIGTERM


LISTEN_PORT = 8000
ECHO_LOG_PATH = './logs/sessions/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)3.3s [%(name)s:%(funcName)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'filename': './logs/echo_server_log.log',
            'formatter': 'simple',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file'],
        'propagate': True,
    }
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('')


def keep_alive(sk, addr, callback):
    signal(SIGTERM, callback)
    log_filename = datetime.now().strftime('%Y-%m-%d_%H:%M:%S_{}').format(addr)
    with open(ECHO_LOG_PATH + log_filename, 'w') as log_file:
        while True:
            data = sk.recv(2048)

            if not data:
                callback()
                return

            sk.send(data)
            log_file.write(str(data)[2:-1])


def get_termination_callback(sk):
    def callback():
        sk.shutdown(1)
        sk.close()

    return callback


def setup():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', LISTEN_PORT))
    connection.listen(0)

    thread_list = []
    try:
        while True:
            new_socket, address = connection.accept()

            addr, port = address
            logger.info('connection from {}:{}'.format(addr, port))

            callback = get_termination_callback(new_socket)
            p = Process(target=keep_alive, args=(new_socket, addr, callback))
            p.start()
            thread_list.append(p)

    except KeyboardInterrupt:
        for p in thread_list:
            p.terminate()


if __name__ == "__main__":
    try:
        setup()
    except:
        logger.exception('Something went wrong')

